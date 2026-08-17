"""Active register (active.md) parser, consistency checker, and updater.

Cross-checks active.md entries against the objects directory to detect
stale entries (closed objects still listed) and missing entries (active
objects not listed).
"""

import re
from pathlib import Path
from typing import List, Optional, Set

from .atomic import atomic_write_text
from .schema import parse_frontmatter

# ── Active entry parsing ──────────────────────────────────────────────────────

ACTIVE_ENTRY_RE = re.compile(r"^- `([^`]+)` — (.+)$")


def parse_active_md(content: str) -> List[tuple]:
    """Parse active.md and return list of (id, description) tuples."""
    entries = []
    for line in content.split("\n"):
        match = ACTIVE_ENTRY_RE.match(line.strip())
        if match:
            entries.append((match.group(1), match.group(2).strip()))
    return entries


def get_active_ids(content: str) -> Set[str]:
    """Get the set of IDs listed in active.md."""
    return {entry[0] for entry in parse_active_md(content)}


# ── Consistency checking ──────────────────────────────────────────────────────


def find_stale_entries(
    active_md_path: Path,
    objects_dir: Path,
) -> List[tuple]:
    """Find active.md entries for objects that are closed or missing.

    Returns list of (id, description, problem) tuples.
    """
    if not active_md_path.exists():
        return []

    content = active_md_path.read_text()
    entries = parse_active_md(content)
    stale = []

    for obj_id, desc in entries:
        # Find the object file
        obj_file = _find_object_file(objects_dir, obj_id)
        if obj_file is None:
            stale.append((obj_id, desc, "Object file not found"))
            continue

        try:
            fm = parse_frontmatter(obj_file.read_text())
        except ValueError:
            stale.append((obj_id, desc, "Cannot parse object frontmatter"))
            continue

        status = str(fm.get("status", ""))
        if status == "closed":
            stale.append((obj_id, desc, f"Object has status: closed"))

    return stale


def find_missing_entries(
    active_md_path: Path,
    objects_dir: Path,
) -> List[tuple]:
    """Find active objects not listed in active.md, and unparseable files.

    Returns list of (obj_id, problem) tuples, mirroring find_stale_entries's
    existing (id, desc, problem) pattern. `problem` is None for an ordinary
    missing entry (parses fine, is active, and isn't listed in active.md);
    it is "Cannot parse object frontmatter" for a file that could not be
    parsed at all, using the filename stem as the identifier since the
    object's own declared id may be unreadable. Previously such files were
    silently skipped (`except ValueError: continue`) -- an asymmetry with
    find_stale_entries, which already flags the identical failure for
    entries reached via active.md.
    """
    active_ids = set()
    if active_md_path.exists():
        active_ids = get_active_ids(active_md_path.read_text())

    missing = []
    if not objects_dir.exists():
        return missing

    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if not obj_file.suffix == ".md":
                    continue
                try:
                    fm = parse_frontmatter(obj_file.read_text())
                except ValueError:
                    missing.append((obj_file.stem, "Cannot parse object frontmatter"))
                    continue
                obj_id = str(fm.get("id", ""))
                status = str(fm.get("status", ""))
                if obj_id and status == "active" and obj_id not in active_ids:
                    missing.append((obj_id, None))

    return missing


def check_attention_consistency(
    active_md_path: Path,
    objects_dir: Path,
) -> List[str]:
    """Run full attention register consistency check.

    Returns list of error messages. Empty list = consistent.
    """
    errors = []

    stale = find_stale_entries(active_md_path, objects_dir)
    for obj_id, desc, problem in stale:
        errors.append(f"Stale entry in active.md: {obj_id} — {problem}")

    missing = find_missing_entries(active_md_path, objects_dir)
    for obj_id, problem in missing:
        if problem:
            errors.append(f"Active object not in active.md: {obj_id} — {problem}")
        else:
            errors.append(f"Active object not in active.md: {obj_id}")

    return errors


def repair_missing_active_entries(
    active_md_path: Path,
    objects_dir: Path,
    default_role: str = "supporting",
) -> List[str]:
    """Restore active.md entries for active objects missing from it.

    Reconstructs each entry from the object file's own frontmatter (id,
    title) only -- role is not stored in frontmatter (it only ever lived in
    active.md), so a repaired entry always gets `default_role`, which may not
    match whatever role the object originally had. Idempotent: re-running
    against an already-consistent active.md makes no change. An entry that
    `find_missing_entries` flags with a parse problem is skipped explicitly
    -- it can't be repaired from a file that can't be read -- rather than
    silently dropped; it remains visible via the next `find_missing_entries`
    or `check_attention_consistency` call.

    Returns the list of object IDs actually repaired.
    """
    missing = find_missing_entries(active_md_path, objects_dir)
    repaired = []

    for obj_id, problem in missing:
        if problem:
            continue
        obj_file = _find_object_file(objects_dir, obj_id)
        if obj_file is None:
            continue
        try:
            fm = parse_frontmatter(obj_file.read_text())
        except ValueError:
            continue
        title = str(fm.get("title", obj_id))
        updated = update_active_entry(active_md_path, obj_id, title, default_role)
        atomic_write_text(active_md_path, updated)
        repaired.append(obj_id)

    return repaired


# ── Active.md updates ─────────────────────────────────────────────────────────


def update_active_entry(
    active_md_path: Path,
    obj_id: str,
    title: str,
    role: str,
) -> str:
    """Add or update an entry in active.md.

    If the ID already exists, the description is updated to reflect
    the new role. If not, a new entry is appended.

    Returns the updated content.
    """
    if not active_md_path.exists():
        return f"# Active Work Objects\n\n- `{obj_id}` — {title} ({role})\n"

    content = active_md_path.read_text()
    entry_line = f"- `{obj_id}` — {title} ({role})"

    # Check if ID already exists
    if f"`{obj_id}`" in content:
        # Replace existing entry
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            if f"`{obj_id}`" in line and line.strip().startswith("-"):
                new_lines.append(entry_line)
            else:
                new_lines.append(line)
        return "\n".join(new_lines)

    # Insert new entry in the correct section
    insert_at = _section_insertion_point(content, role)
    return content[:insert_at] + f"{entry_line}\n" + content[insert_at:]


def remove_active_entry(
    active_md_path: Path,
    obj_id: str,
) -> Optional[str]:
    """Remove an entry from active.md.

    Returns the updated content, or None if the entry wasn't found.
    """
    if not active_md_path.exists():
        return None

    content = active_md_path.read_text()
    if f"`{obj_id}`" not in content:
        return None

    lines = content.split("\n")
    new_lines = [l for l in lines if f"`{obj_id}`" not in l or not l.strip().startswith("-")]
    return "\n".join(new_lines)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _section_insertion_point(content: str, role: str) -> int:
    """Find where to insert a new active.md entry based on role.

    Inserts the entry after the target section heading and before the next
    ``## `` heading. For ``paused`` (or when the target section isn't found),
    appends at end-of-file.
    """
    section_heading = {
        "primary": "## Primary",
        "supporting": "## Supporting",
        "paused": "## Paused",
    }.get(role)

    if not section_heading:
        return len(content)

    heading_pos = content.find(section_heading)
    if heading_pos == -1:
        return len(content)

    # Find the next section heading after this one
    next_section = content.find("\n## ", heading_pos + len(section_heading))
    if next_section == -1:
        return len(content)

    # Insert just before the next section (after the preceding newline)
    return next_section + 1


def _find_object_file(objects_dir: Path, obj_id: str) -> Optional[Path]:
    """Find a Work Object file by its ID anywhere under objects_dir."""
    if not objects_dir.exists():
        return None

    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if not obj_file.name.startswith(obj_id):
                    continue
                if obj_file.suffix == ".md":
                    return obj_file

    return None
