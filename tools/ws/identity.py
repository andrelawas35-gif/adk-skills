"""Immutable ID allocation with collision detection.

Scans objects/YYYY/MM/ for existing IDs on the current date, derives the next
zero-padded sequence number, and verifies no existing file conflicts with the
allocated ID.

Sequences 900-999 are a reserved fixture band. Allocation ignores them when
computing the next sequence, so a synthetic fixture parked at a high number
cannot exhaust the day. Without this, allocation was ``max(existing) + 1`` and
a single ``-999-`` fixture blocked every creation for that date.
"""

import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

ID_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(\d{3})-.+\.md$")

# Sequences at or above this value are reserved for synthetic fixtures and are
# never auto-allocated. Real objects allocate from 001 to RESERVED_FIXTURE_MIN-1.
RESERVED_FIXTURE_MIN = 900


def allocate_id(objects_dir: Path, today: Optional[date] = None) -> str:
    """Allocate the next available immutable ID for today.

    Args:
        objects_dir: Path to .work-studio/objects/ directory
        today: Date for ID prefix (defaults to current date)

    Returns:
        ID string like 2026-07-21-010

    Raises:
        FileExistsError: If the allocated ID already has a file (collision)
    """
    if today is None:
        today = date.today()

    date_prefix = today.strftime("%Y-%m-%d")
    month_dir = objects_dir / str(today.year) / f"{today.month:02d}"

    # Find the highest existing sequence number for this date
    max_seq = 0
    if month_dir.exists():
        for entry in month_dir.iterdir():
            if not entry.is_file():
                continue
            match = ID_PATTERN.match(entry.name)
            if match:
                y, m, d, seq = match.groups()
                if f"{y}-{m}-{d}" == date_prefix:
                    seq_num = int(seq)
                    # Reserved fixture band never participates in allocation.
                    if seq_num >= RESERVED_FIXTURE_MIN:
                        continue
                    if seq_num > max_seq:
                        max_seq = seq_num

    next_seq = max_seq + 1
    if next_seq >= RESERVED_FIXTURE_MIN:
        raise RuntimeError(
            f"Maximum ID sequence ({RESERVED_FIXTURE_MIN - 1}) reached for "
            f"{date_prefix}. Sequences {RESERVED_FIXTURE_MIN}-999 are reserved "
            "for synthetic fixtures and are not auto-allocated."
        )

    obj_id = f"{date_prefix}-{next_seq:03d}"
    return obj_id


def slugify(title: str) -> str:
    """Convert a title to a filesystem-safe slug.

    Lowercases, replaces non-alphanumeric characters with hyphens,
    collapses consecutive hyphens, strips leading/trailing hyphens.
    """
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def build_filename(obj_id: str, title: str) -> str:
    """Build the canonical filename for a Work Object.

    Format: <id>-<slug>.md

    Args:
        obj_id: Allocated ID (e.g. 2026-07-21-010)
        title: Work Object title

    Returns:
        Filename string (e.g. 2026-07-21-010-fix-auth-middleware.md)
    """
    slug = slugify(title)
    return f"{obj_id}-{slug}.md"


def build_path(objects_dir: Path, obj_id: str, title: str) -> Path:
    """Build the full output path for a new Work Object.

    Creates the necessary directories.

    Args:
        objects_dir: Path to .work-studio/objects/
        obj_id: Allocated ID
        title: Work Object title

    Returns:
        Full path where the file should be written

    Raises:
        FileExistsError: If the target file already exists
    """
    filename = build_filename(obj_id, title)
    # objects/YYYY/MM/<filename>
    year = obj_id[:4]
    month = obj_id[5:7]
    target_dir = objects_dir / year / month
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename
