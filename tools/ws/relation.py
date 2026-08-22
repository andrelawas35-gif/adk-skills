"""Typed Relationship edges for Work Objects (tracer bullet, WO 2026-08-22-026).

Implements the smallest write path for the typed-edge vocabulary proposed in
``references/architecture/epistemic-graph-loop-system-improvement-architecture.md``
section 7.3: a single CLI command that appends an append-only, typed edge
record into a Work Object's ``## Relationships`` section. No new node types,
no graph engine, no loop reducer -- see WO 2026-08-22-026 Decision 1 for the
explicit non-goals this tracer stays inside.

One CLI command:
    - ``ws relation add <from-id> --type <type> --to <to-ref> [--basis <ref>]``

Relationship block format (YAML-in-Markdown, stdlib-compatible, mirrors
``claim.py``'s ``## Claims`` block style):

.. code-block:: markdown

    ## Relationships

      REL-<from-id>-001:
        type: responds_to
        from: wo:2026-08-22-026
        to: wo:2026-08-21-006
        basis: "Decision 1"
        created_at: 2026-08-22T15:00:00Z

``to`` (and, in principle, ``from``) may reference a Work Object ID directly
(``2026-08-22-026`` or ``wo:2026-08-22-026``) or an explicitly external
locator (``external:<free text>``). Per graph invariant #1 (architecture
section 3.4), every edge endpoint must resolve or be explicitly marked
external -- ``relation add`` enforces this for ``--to`` at write time.

Valid edge types (architecture section 7.3's initial vocabulary; fixed --
adding a new type requires a domain-modeling decision, not a code change):
    responds_to resulted_in supersedes depends_on blocks
    implements verifies observes revises supports counters
    authorized_by generated_by used invalidates hands_off_to
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .concurrency import check_concurrency
from .atomic import atomic_write_text
from .sections import append_to_section, compose_object_text, get_section

# ── Constants ─────────────────────────────────────────────────────────────────

VALID_EDGE_TYPES = frozenset({
    "responds_to", "resulted_in", "supersedes", "depends_on", "blocks",
    "implements", "verifies", "observes", "revises", "supports", "counters",
    "authorized_by", "generated_by", "used", "invalidates", "hands_off_to",
})
RELATIONSHIPS_SECTION_NAME = "Relationships"

# A bare or "wo:"-prefixed Work Object ID reference, e.g. 2026-08-22-026
_WO_REF_RE = re.compile(r"^(?:wo:)?(\d{4}-\d{2}-\d{2}-\d{3})$")


# ── Helpers (mirror claim.py's self-contained module pattern) ──────────────────


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


def _resolve_object_file(objects_dir: Path, obj_id: str) -> Optional[Path]:
    """Find a Work Object file by its ID anywhere under objects_dir.

    Returns None (rather than raising) when not found, so callers can
    distinguish "must exist" (the object being written to) from "may be
    external" (an edge endpoint) resolution.
    """
    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if obj_file.name.startswith(obj_id) and obj_file.suffix == ".md":
                    return obj_file
    return None


def _escape(value: str) -> str:
    """Escape double quotes and newlines for an inline relationship value."""
    return value.replace('"', '\\"').replace("\n", "\\n")


def _allocate_relation_id(body: str, from_id: str) -> str:
    """Allocate the next REL-<from-id>-NNN ID by scanning existing edges."""
    safe_id = from_id.replace("-", "_")
    section = get_section(body, RELATIONSHIPS_SECTION_NAME)
    if not section:
        return f"REL-{safe_id}-001"

    pattern = re.compile(rf"REL-{re.escape(safe_id)}-(\d+)")
    existing = pattern.findall(section)
    if not existing:
        return f"REL-{safe_id}-001"

    max_num = max(int(n) for n in existing)
    return f"REL-{safe_id}-{max_num + 1:03d}"


def normalize_ref(raw: str) -> Optional[str]:
    """Normalize a --to endpoint into ``wo:<id>`` or ``external:<locator>``.

    Returns None when the ref is neither a resolvable-shaped WO reference
    nor an explicit external locator -- the caller rejects it.
    """
    raw = raw.strip()
    if raw.startswith("external:"):
        return raw
    match = _WO_REF_RE.match(raw)
    if match:
        return f"wo:{match.group(1)}"
    return None


def _generate_relation_block(
    relation_id: str, edge_type: str, from_ref: str, to_ref: str,
    basis: Optional[str],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"  {relation_id}:",
        f"    type: {edge_type}",
        f"    from: {from_ref}",
        f"    to: {to_ref}",
    ]
    if basis:
        lines.append(f'    basis: "{_escape(basis)}"')
    lines.append(f"    created_at: {now}")
    return "\n".join(lines)


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def parse_relationships(body: str) -> List[Dict[str, Any]]:
    """Parse all relationship blocks from the ``## Relationships`` section.

    Returns a list of dicts, one per edge, with keys: id, type, from, to,
    basis (optional), created_at. Mirrors claim.py's ``parse_claims`` flat
    key:value parsing (no nested mappings needed here).
    """
    section = get_section(body, RELATIONSHIPS_SECTION_NAME)
    if not section:
        return []

    edges: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for line in section.split("\n"):
        rel_match = re.match(r"^\s+(REL-[\w]+-\d+):", line)
        if rel_match:
            if current:
                edges.append(current)
            current = {"id": rel_match.group(1)}
            continue

        if current is None:
            continue

        stripped = line.strip()
        if not stripped:
            continue

        kv_match = re.match(r"^(type|from|to|basis|created_at):\s*(.*)$", stripped)
        if kv_match:
            current[kv_match.group(1)] = _unquote(kv_match.group(2))

    if current:
        edges.append(current)

    return edges


def _update_frontmatter_fields(content: str, updates: dict) -> str:
    """Update ``updated_at`` (and other scalar fields) in a Work Object's frontmatter.

    Mirrors ``__main__.py``'s and ``claim.py``'s private helper to keep this
    module self-contained.
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


# ═══════════════════════════════════════════════════════════════════════════════
# ws relation add
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_relation_add(args: argparse.Namespace) -> int:
    """Append a typed Relationship edge into a Work Object's ## Relationships section."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    obj_file = _resolve_object_file(objects_dir, args.id)
    if obj_file is None:
        print(f"Error: Work Object not found for ID: {args.id}", file=sys.stderr)
        return 1

    if args.type not in VALID_EDGE_TYPES:
        print(
            f"Error: Invalid relationship type '{args.type}'. "
            f"Must be one of: {', '.join(sorted(VALID_EDGE_TYPES))}",
            file=sys.stderr,
        )
        return 1

    to_ref = normalize_ref(args.to)
    if to_ref is None:
        print(
            f"Error: --to '{args.to}' does not resolve. "
            "Use a Work Object ID (YYYY-MM-DD-NNN, with or without a 'wo:' "
            "prefix) or an explicit 'external:<locator>' reference "
            "(graph invariant: every edge endpoint resolves or is explicitly "
            "external).",
            file=sys.stderr,
        )
        return 1

    if to_ref.startswith("wo:"):
        to_id = to_ref[3:]
        if _resolve_object_file(objects_dir, to_id) is None:
            print(
                f"Error: --to references Work Object '{to_id}', which does not "
                "exist. Use 'external:<locator>' if the target is intentionally "
                "outside the Work Object corpus.",
                file=sys.stderr,
            )
            return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text(encoding="utf-8")
    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    relation_id = _allocate_relation_id(body, args.id)
    from_ref = f"wo:{args.id}"

    relation_block = _generate_relation_block(
        relation_id, args.type, from_ref, to_ref, args.basis,
    )

    new_body = append_to_section(body, RELATIONSHIPS_SECTION_NAME, relation_block)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    atomic_write_text(obj_file, compose_object_text(new_fm, new_body))

    print(f"Relationship {relation_id} added: {from_ref} --[{args.type}]--> {to_ref}")
    return 0
