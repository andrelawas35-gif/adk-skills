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
from .atomic import atomic_write_text
from .sections import append_to_section, compose_object_text, get_section


CONFLICT_SECTION_NAME = "Claims"
CONFLICT_RESOLUTION_DISPOSITIONS = {"superseded"}


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


def _allocate_conflict_resolution_id(body: str, wo_id: str) -> str:
    """Allocate the next CONFRES-<wo-id>-NNN ID by scanning Claims."""
    safe_id = wo_id.replace("-", "_")
    claims_section = get_section(body, CONFLICT_SECTION_NAME)
    if not claims_section:
        return f"CONFRES-{safe_id}-001"

    pattern = re.compile(rf"CONFRES-{re.escape(safe_id)}-(\d+)")
    existing = pattern.findall(claims_section)
    if not existing:
        return f"CONFRES-{safe_id}-001"

    max_num = max(int(n) for n in existing)
    return f"CONFRES-{safe_id}-{max_num + 1:03d}"


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


def _generate_conflict_resolution_block(
    resolution_id: str,
    conflict_id: str,
    resolver: str,
    disposition: str,
    rationale: str,
    source_object_id: Optional[str] = None,
) -> str:
    """Generate an appended conflict-resolution block for the Claims section."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    escaped_rationale = rationale.replace('"', '\\"')
    lines = [
        f"  {resolution_id}:",
        f"    conflict_id: {conflict_id}",
    ]
    if source_object_id:
        lines.append(f"    source_object_id: {source_object_id}")
    lines.extend([
        f"    resolver: {resolver}",
        f"    disposition: {disposition}",
        f'    rationale: "{escaped_rationale}"',
        f"    timestamp: {now}",
    ])
    return "\n".join(lines)


def _claims_contains_conflict(claims_section: str, conflict_id: str) -> bool:
    """Return whether Claims contains the named conflict heading."""
    return re.search(rf"^  {re.escape(conflict_id)}:$", claims_section, re.MULTILINE) is not None


def _claims_contains_resolution_for(claims_section: str, conflict_id: str) -> bool:
    """Return whether Claims already contains a CONFRES- for conflict_id."""
    pattern = re.compile(
        rf"^  CONFRES-[\w]+-\d+:\n(?:    .+\n)*?    conflict_id: {re.escape(conflict_id)}(?:\n|$)",
        re.MULTILINE,
    )
    return pattern.search(claims_section) is not None


def _any_claims_contains_resolution_for(objects_dir: Path, conflict_id: str) -> bool:
    """Return whether any Work Object has a CONFRES- for conflict_id."""
    for obj_file in objects_dir.rglob("*.md"):
        content = obj_file.read_text()
        body = (
            content[content.find("---", 3) + 3:].strip()
            if content.startswith("---")
            else content
        )
        claims_section = get_section(body, CONFLICT_SECTION_NAME)
        if claims_section and _claims_contains_resolution_for(claims_section, conflict_id):
            return True
    return False


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

    atomic_write_text(obj_file, compose_object_text(new_fm, new_body))

    print(f"Conflict {conflict_id} registered in {args.id}")
    print(f"  claim_id: {args.claim_id}")
    print(f"  versions: {len(versions)}")
    return 0


def cmd_conflict_resolve(args: argparse.Namespace) -> int:
    """Append a CONFRES- record resolving a conflict without editing CONF-."""
    if args.disposition not in CONFLICT_RESOLUTION_DISPOSITIONS:
        allowed = ", ".join(sorted(CONFLICT_RESOLUTION_DISPOSITIONS))
        print(
            f"Error: Unsupported disposition '{args.disposition}'. Allowed: {allowed}.",
            file=sys.stderr,
        )
        return 1

    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"
    try:
        source_file = _resolve_object_file(objects_dir, args.id)
        target_id = getattr(args, "record_in", None) or args.id
        target_file = _resolve_object_file(objects_dir, target_id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    err = check_concurrency(target_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    target_fm = parse_frontmatter(target_file.read_text())
    if str(target_fm.get("status", "")) == "closed":
        print(
            f"Error: Cannot record conflict resolution in closed object {target_id}.",
            file=sys.stderr,
        )
        return 1

    source_content = source_file.read_text()
    source_body = (
        source_content[source_content.find("---", 3) + 3:].strip()
        if source_content.startswith("---")
        else source_content
    )
    source_claims_section = get_section(source_body, CONFLICT_SECTION_NAME)
    if not source_claims_section:
        print(f"Error: Work Object {args.id} has no ## Claims section.", file=sys.stderr)
        return 1

    if not _claims_contains_conflict(source_claims_section, args.conflict_id):
        print(
            f"Error: Conflict {args.conflict_id} not found in {args.id}.",
            file=sys.stderr,
        )
        return 1

    if _any_claims_contains_resolution_for(objects_dir, args.conflict_id):
        print(
            f"Error: Conflict {args.conflict_id} already has a CONFRES- record.",
            file=sys.stderr,
        )
        return 1

    target_content = target_file.read_text()
    target_body = (
        target_content[target_content.find("---", 3) + 3:].strip()
        if target_content.startswith("---")
        else target_content
    )

    resolution_id = _allocate_conflict_resolution_id(target_body, target_id)
    resolution_block = _generate_conflict_resolution_block(
        resolution_id=resolution_id,
        conflict_id=args.conflict_id,
        resolver=args.resolver,
        disposition=args.disposition,
        rationale=args.rationale,
        source_object_id=args.id if target_id != args.id else None,
    )

    new_body = append_to_section(target_body, CONFLICT_SECTION_NAME, resolution_block)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(target_content, {"updated_at": now})

    atomic_write_text(target_file, compose_object_text(new_fm, new_body))

    print(f"Conflict resolution {resolution_id} registered in {target_id}")
    print(f"  conflict_id: {args.conflict_id}")
    if target_id != args.id:
        print(f"  source_object_id: {args.id}")
    print(f"  disposition: {args.disposition}")
    return 0
