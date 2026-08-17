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
from typing import Any, Dict, List, Optional

from .concurrency import check_concurrency
from .schema import parse_frontmatter
from .atomic import atomic_write_text
from .sections import append_to_section, compose_object_text, get_section

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


def _get_workspace_name(ws_root: Path) -> str:
    """Read the workspace name from .work-studio/config.md, with fallback."""
    config = ws_root / ".work-studio" / "config.md"
    if config.exists():
        for line in config.read_text().splitlines():
            if "- **Name**" in line:
                name = line.split("**", 2)[-1].split(":", 1)[-1].strip()
                if name:
                    return name
    return "andrelawas-work-studio"


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


def _escape(value: str) -> str:
    """Escape double quotes and newlines for an inline claim value."""
    return value.replace('"', '\\"').replace("\n", "\\n")


def _format_inline_list(values: List[str]) -> str:
    """Format a list as an inline flow list: [\"a\", \"b\"]."""
    parts = [f'"{_escape(v)}"' for v in values]
    return "[" + ", ".join(parts) + "]"


def _generate_claim_block(
    claim_id: str,
    text: str,
    kind: str,
    scope: Optional[Dict[str, Any]] = None,
    scalar_scope: Optional[str] = None,
    revisit_on: Optional[List[str]] = None,
) -> str:
    """Generate an indented YAML-like claim block for the Claims section.

    Emits the structured nested ``scope:`` mapping (with ``paths`` and optional
    ``repository``/``git_commit``/``dirty_tree_fingerprint``) when ``scope`` is
    a dict; otherwise emits the legacy scalar ``scope: "<str>"`` form from
    ``scalar_scope``. ``revisit_on`` adds a sibling ``revisit.on`` list.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"  {claim_id}:",
        f'    text: "{_escape(text)}"',
        f"    kind: {kind}",
        f"    state: captured",
    ]
    if scope is not None:
        lines.append("    scope:")
        for key in ("repository", "git_commit", "dirty_tree_fingerprint"):
            val = scope.get(key)
            if val:
                lines.append(f'      {key}: "{_escape(str(val))}"')
        paths = scope.get("paths") or []
        if paths:
            lines.append(f"      paths: {_format_inline_list(paths)}")
    else:
        lines.append(f'    scope: "{_escape(scalar_scope or "")}"')
    lines.append(f"    created_at: {now}")
    if revisit_on:
        lines.append("    revisit:")
        lines.append(f"      on: {_format_inline_list(revisit_on)}")
    return "\n".join(lines)


def _unquote(value: str) -> str:
    """Strip surrounding double quotes from a value, if present."""
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def _parse_inline_list(value: str) -> List[str]:
    """Parse a bracketed flow list like [\"a\", \"b\"] into a Python list."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
    else:
        inner = value
    return [_unquote(p) for p in inner.split(",") if p.strip()]


def parse_claims(body: str) -> List[Dict[str, Any]]:
    """Parse all claim blocks from the ``## Claims`` section.

    Returns a list of dicts, one per claim. Each claim has keys:
    id, text, kind, state, created_at, and either:
      - ``scope`` as a plain string (legacy scalar form), or
      - ``scope`` as a dict (structured form) with any of repository,
        git_commit, dirty_tree_fingerprint, paths (a list),
        plus ``revisit`` as a dict with an ``on`` list when present.
    A ``scope:`` (or ``revisit:``) line with an empty value starts a nested
    mapping; a non-empty value is the legacy scalar form.
    """
    section = get_section(body, CLAIM_SECTION_NAME)
    if not section:
        return []

    claims: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    key_indent: Optional[int] = None  # indentation of the claim's key lines
    nested: Optional[str] = None      # "scope" or "revisit" when in a mapping

    for line in section.split("\n"):
        # Claim ID line: whitespace, then CLM-<id>:
        claim_match = re.match(r"^\s+(CLM-[\w]+-\d+):", line)
        if claim_match:
            if current:
                claims.append(current)
            current = {"id": claim_match.group(1)}
            key_indent = None
            nested = None
            continue

        if current is None:
            continue

        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip(" "))

        # Claim key line at the claim's key indentation
        kv_match = re.match(
            r"^(text|kind|state|scope|created_at|revisit):\s*(.*)$", stripped
        )
        if kv_match and (key_indent is None or indent == key_indent):
            if key_indent is None:
                key_indent = indent
            key = kv_match.group(1)
            value = kv_match.group(2).strip()
            if key in ("scope", "revisit"):
                if value == "":
                    nested = key
                    current[key] = {}
                else:
                    nested = None
                    current[key] = _unquote(value)
            else:
                nested = None
                current[key] = _unquote(value)
            continue

        # Nested child line (indented deeper than the claim's key lines)
        if nested is not None and (key_indent is None or indent > key_indent):
            child_match = re.match(
                r"^(repository|git_commit|dirty_tree_fingerprint|paths|on):\s*(.*)$",
                stripped,
            )
            if child_match:
                child_key = child_match.group(1)
                child_value = child_match.group(2).strip()
                mapping = current[nested]
                if child_key in ("paths", "on"):
                    mapping[child_key] = _parse_inline_list(child_value)
                else:
                    mapping[child_key] = _unquote(child_value)
            continue

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

    # Scope form: scalar (--scope) or structured (--paths), mutually exclusive
    scalar_scope = args.scope
    structured_scope = None
    if args.paths:
        structured_scope = {"paths": list(args.paths)}
        if getattr(args, "git_commit", None):
            structured_scope["git_commit"] = args.git_commit
        if getattr(args, "dirty_fingerprint", None):
            structured_scope["dirty_tree_fingerprint"] = args.dirty_fingerprint
        repository = _get_workspace_name(ws_root)
        if repository:
            structured_scope["repository"] = repository
        scalar_scope = None
    if args.scope and args.paths:
        print(
            "Error: Use either --scope (scalar) or --paths (structured), not both.",
            file=sys.stderr,
        )
        return 1
    if not args.scope and not args.paths:
        print(
            "Error: Provide --scope (scalar) or --paths (structured).",
            file=sys.stderr,
        )
        return 1

    revisit_on = list(args.revisit_on) if args.revisit_on else None

    # Generate claim block
    claim_block = _generate_claim_block(
        claim_id,
        args.text,
        args.kind,
        scope=structured_scope,
        scalar_scope=scalar_scope,
        revisit_on=revisit_on,
    )

    # Append to Claims section
    new_body = append_to_section(body, CLAIM_SECTION_NAME, claim_block)

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    atomic_write_text(obj_file, compose_object_text(new_fm, new_body))

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
        if isinstance(scope, dict):
            print("    scope:")
            for key, val in scope.items():
                if isinstance(val, list):
                    print(f"      {key}: {_format_inline_list(val)}")
                else:
                    print(f"      {key}: {val}")
        else:
            print(f"    scope:  {scope}")
        revisit = c.get("revisit")
        if isinstance(revisit, dict) and revisit.get("on"):
            print("    revisit:")
            print(f"      on: {_format_inline_list(revisit['on'])}")
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
