"""Claim sidecar register and inspect for Work Objects.

Implements the tracer bullet from 2026-07-27-016: structured claim objects
stored inline in the Work Object body under a ``## Claims`` section.

Two CLI commands:
    - ``ws claim register <wo-id> --text <text> --kind <kind> --scope <scope>``
    - ``ws claim inspect <wo-id> [--state <state>]``

Claim format (YAML-in-Markdown, stdlib-compatible):

.. code-block:: markdown

    ## Claims

      CLM-<wo-id>-001:
        text: "The claim statement"
        kind: observation
        state: captured
        scope: "scope-path"
        created_at: 2026-07-27T12:00:00Z

Valid kinds: observation, inference, decision
Valid states: captured, supported, accepted_for_action
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

# ── Constants ─────────────────────────────────────────────────────────────────

VALID_CLAIM_KINDS = frozenset({"observation", "inference", "decision"})
VALID_CLAIM_STATES = frozenset({"captured", "supported", "accepted_for_action"})
CLAIM_SECTION_NAME = "Claims"


# ── Helpers ───────────────────────────────────────────────────────────────────


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


def _get_consequence(content: str) -> Optional[str]:
    """Extract the consequence field from a Work Object's frontmatter."""
    fm = parse_frontmatter(content)
    return str(fm.get("consequence", "")) if fm.get("consequence") else None


def _allocate_claim_id(body: str, wo_id: str) -> str:
    """Allocate the next CLM-<wo-id>-NNN ID by scanning existing claims."""
    # Normalise the WO ID for use in the CLM prefix
    safe_id = wo_id.replace("-", "_")
    claims_section = get_section(body, CLAIM_SECTION_NAME)
    if not claims_section:
        return f"CLM-{safe_id}-001"

    pattern = re.compile(rf"CLM-{re.escape(safe_id)}-(\d+)")
    existing = pattern.findall(claims_section)
    if not existing:
        return f"CLM-{safe_id}-001"

    max_num = max(int(n) for n in existing)
    return f"CLM-{safe_id}-{max_num + 1:03d}"


def _generate_claim_block(claim_id: str, text: str, kind: str, scope: str) -> str:
    """Generate an indented YAML-like claim block for the Claims section."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Double-quote text and scope to handle special characters in Markdown
    escaped_text = text.replace('"', '\\"').replace("\n", "\\n")
    escaped_scope = scope.replace('"', '\\"').replace("\n", "\\n")
    lines = [
        f"  {claim_id}:",
        f'    text: "{escaped_text}"',
        f"    kind: {kind}",
        f"    state: captured",
        f'    scope: "{escaped_scope}"',
        f"    created_at: {now}",
    ]
    return "\n".join(lines)


def parse_claims(body: str) -> List[Dict[str, str]]:
    """Parse all claim blocks from the ``## Claims`` section.

    Returns a list of dicts, one per claim, each with keys:
    id, text, kind, state, scope, created_at.
    """
    section = get_section(body, CLAIM_SECTION_NAME)
    if not section:
        return []

    claims: List[Dict[str, str]] = []
    current: Optional[Dict[str, str]] = None

    for line in section.split("\n"):
        # Claim ID line: whitespace, then CLM-<id>:
        claim_match = re.match(r"^\s+(CLM-[\w]+-\d+):", line)
        if claim_match:
            if current:
                claims.append(current)
            current = {"id": claim_match.group(1)}
            continue

        # Key: value line within a claim block (indented further)
        if current is not None:
            kv_match = re.match(r"^\s+(text|kind|state|scope|created_at):\s*(.+)", line)
            if kv_match:
                key = kv_match.group(1)
                value = kv_match.group(2).strip()
                # Strip surrounding quotes from text/scope values
                if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                current[key] = value

    if current:
        claims.append(current)

    return claims


# ═══════════════════════════════════════════════════════════════════════════════
# ws claim register
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_claim_register(args: argparse.Namespace) -> int:
    """Register a new claim in a Work Object's ``## Claims`` section.

    Only meaningful/high consequence Work Objects accept claim registration.
    Low-consequence Work Objects are rejected with a clear message.
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

    # Validate kind
    if args.kind not in VALID_CLAIM_KINDS:
        print(
            f"Error: Invalid claim kind '{args.kind}'. "
            f"Must be one of: {', '.join(sorted(VALID_CLAIM_KINDS))}",
            file=sys.stderr,
        )
        return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()

    # Reject low-consequence Work Objects
    consequence = _get_consequence(content)
    if consequence and consequence == "low":
        print(
            f"Error: Claim registration rejected — Work Object {args.id} "
            f"has consequence '{consequence}'. "
            f"Claims are only supported for meaningful or high consequence objects.",
            file=sys.stderr,
        )
        return 1

    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    # Allocate claim ID
    claim_id = _allocate_claim_id(body, args.id)

    # Generate claim block
    claim_block = _generate_claim_block(claim_id, args.text, args.kind, args.scope)

    # Append to Claims section
    new_body = append_to_section(body, CLAIM_SECTION_NAME, claim_block)

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    obj_file.write_text(new_fm + "\n" + new_body)

    print(f"Claim {claim_id} registered in {args.id}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws claim inspect
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_claim_inspect(args: argparse.Namespace) -> int:
    """List claims for a Work Object, optionally filtered by state."""
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

    content = obj_file.read_text()
    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    claims = parse_claims(body)

    # Filter by state if specified
    if args.state:
        claims = [c for c in claims if c.get("state") == args.state]

    if not claims:
        filter_msg = f" with state '{args.state}'" if args.state else ""
        print(f"No claims found for {args.id}{filter_msg}.")
        return 0

    # Print claim summary
    print(f"Claims for {args.id} ({len(claims)} total):")
    print()
    for c in claims:
        cid = c.get("id", "?")
        kind = c.get("kind", "?")
        state = c.get("state", "?")
        scope = c.get("scope", "?")
        text = c.get("text", "?")
        # Truncate text for display
        display_text = text if len(text) <= 72 else text[:69] + "..."
        print(f"  {cid}")
        print(f"    kind:   {kind}")
        print(f"    state:  {state}")
        print(f"    scope:  {scope}")
        print(f"    text:   {display_text}")
        print()

    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# Frontmatter helper (mirrors __main__.py's private helper)
# ═══════════════════════════════════════════════════════════════════════════════


def _update_frontmatter_fields(content: str, updates: dict) -> str:
    """Update ``updated_at`` (and other scalar fields) in a Work Object's frontmatter.

    This mirrors ``__main__.py._update_frontmatter_fields()`` to keep the
    claim module self-contained.
    """
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
