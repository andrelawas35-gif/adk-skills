"""Conflict register for Work Objects.

CLI command:
    - ``ws conflict register <wo-id> --claim-id <claim-id>``
      with paired ``--commit-sha``, ``--file-path``, ``--dirty-hash`` tuples.

Conflict blocks live inline in the ``## Claims`` section, storing version
identity tuples for each side of a disagreement:

.. code-block:: markdown

    ## Claims

      CONF-<wo-id>-001:
        claim_id: CLM-<wo-id>-NNN
        versions:
          - commit_sha: aefd8623...
            file_path: "path/to/file.md"
            dirty_hash: sha256hex
        created_at: 2026-07-28T12:00:00Z
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .concurrency import check_concurrency
from .schema import parse_frontmatter
from .sections import append_to_section, get_section


CONFLICT_SECTION_NAME = "Claims"


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ directory."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _resolve_object_file(objects_dir: Path, obj_id: str) -> Path:
    """Find a Work Object file by its ID anywhere under objects_dir."""
    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if obj_file.name.startswith(obj_id) and obj_file.suffix == ".md":
                    return obj_file
    raise FileNotFoundError(f"Work Object not found for ID: {obj_id}")


def _allocate_conflict_id(body: str, wo_id: str) -> str:
    """Allocate the next CONF-<wo-id>-NNN ID by scanning existing Claims."""
    safe_id = wo_id.replace("-", "_")
    claims_section = get_section(body, CONFLICT_SECTION_NAME)
    if not claims_section:
        return f"CONF-{safe_id}-001"

    pattern = re.compile(rf"CONF-{re.escape(safe_id)}-(\d+)")
    existing = pattern.findall(claims_section)
    if not existing:
        return f"CONF-{safe_id}-001"

    max_num = max(int(n) for n in existing)
    return f"CONF-{safe_id}-{max_num + 1:03d}"


def _generate_conflict_block(
    conflict_id: str,
    claim_id: str,
    versions: List[Dict[str, str]],
) -> str:
    """Generate an indented YAML-like conflict block for the Claims section."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"  {conflict_id}:",
        f"    claim_id: {claim_id}",
        "    versions:",
    ]
    for v in versions:
        escaped_path = v.get("file_path", "?").replace('"', '\\"')
        lines.append(f"      - commit_sha: {v.get('commit_sha', '?')}")
        lines.append(f'        file_path: "{escaped_path}"')
        lines.append(f"        dirty_hash: {v.get('dirty_hash', '?')}")
    lines.append(f"    created_at: {now}")
    return "\n".join(lines)


def _update_frontmatter_fields(content: str, updates: dict) -> str:
    """Update specific fields in the YAML frontmatter block."""
    if not content.startswith("---"):
        return content

    end = content.find("---", 3)
    if end == -1:
        return content

    fm_text = content[4:end]

    lines = fm_text.split("\n")
    new_lines = []
    updated_keys = set()

    for line in lines:
        stripped = line.strip()
        if ":" in stripped and not stripped.startswith("#"):
            key = stripped.split(":", 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}: {updates[key]}")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    for key, val in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}: {val}")

    new_fm = "\n".join(new_lines)
    return "---\n" + new_fm + "\n---"


def cmd_conflict_register(args: argparse.Namespace) -> int:
    """Register a conflict record in a Work Object's ## Claims section.

    A conflict documents that two or more sources disagree on the same claim.
    Each version tuple consists of a commit SHA, file path, and dirty hash.

    Usage::

        ws conflict register <wo-id> \\
            --claim-id <claim-id> \\
            --commit-sha <sha1> --file-path <path1> --dirty-hash <hash1> \\
            --commit-sha <sha2> --file-path <path2> --dirty-hash <hash2>
    """
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"
    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    body = (
        content[content.find("---", 3) + 3:].strip()
        if content.startswith("---")
        else content
    )

    # Build version tuples from paired args
    versions: List[Dict[str, str]] = []
    for cs, fp, dh in zip(args.commit_sha, args.file_path, args.dirty_hash):
        versions.append({
            "commit_sha": cs,
            "file_path": fp,
            "dirty_hash": dh,
        })

    if not versions:
        print("Error: At least one version tuple is required.", file=sys.stderr)
        return 1

    # Allocate conflict ID
    conflict_id = _allocate_conflict_id(body, args.id)

    # Generate conflict block
    conflict_block = _generate_conflict_block(conflict_id, args.claim_id, versions)

    # Append to Claims section
    new_body = append_to_section(body, CONFLICT_SECTION_NAME, conflict_block)

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    obj_file.write_text(new_fm + "\n" + new_body)

    print(f"Conflict {conflict_id} registered in {args.id}")
    print(f"  claim_id: {args.claim_id}")
    print(f"  versions: {len(versions)}")
    return 0
