"""Optimistic concurrency via updated_at read-compare-reject.

Every write command (except create and init) must pass --expect-updated
matching the file's current updated_at. Mismatch means a concurrent write
happened — reject with both timestamps so the caller can reconcile.
"""

import sys
from pathlib import Path
from typing import Optional

from .schema import parse_frontmatter


def check_concurrency(
    file_path: Path,
    expect_updated: str,
    force: bool = False,
) -> Optional[str]:
    """Read file, extract updated_at, compare against expect_updated.

    Args:
        file_path: Path to the Work Object file.
        expect_updated: Expected updated_at timestamp from the caller.
        force: If True, bypass the comparison with a stderr warning.

    Returns:
        None if the write can proceed (match or force).
        Error string if the check fails (caller should print and exit 1).
    """
    if not file_path.exists():
        return f"File not found: {file_path}"

    content = file_path.read_text(encoding="utf-8")
    try:
        fm = parse_frontmatter(content)
    except ValueError as e:
        return f"Failed to parse frontmatter in {file_path}: {e}"

    current_updated = fm.get("updated_at")
    if current_updated is None:
        return f"No updated_at field found in {file_path}"

    current_updated = str(current_updated)

    if force:
        print(
            f"Warning: --force bypasses --expect-updated check. "
            f"Expected: {expect_updated}, actual: {current_updated}",
            file=sys.stderr,
        )
        return None

    if current_updated != expect_updated:
        return (
            f"Concurrent write detected for {file_path.name}.\n"
            f"  Expected updated_at: {expect_updated}\n"
            f"  Actual updated_at:   {current_updated}\n"
            f"  Use --force to bypass (with warning)."
        )

    return None
