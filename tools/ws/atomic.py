"""Atomic text writes for tools/ws (WO 2026-08-16-004 Decision 2).

Prevents a killed process from leaving a truncated file: content is written
to a unique temp file in the same directory, then swapped into place with
`os.replace`, which is atomic on the same filesystem. A reader always sees
either the old whole file or the new whole file, never a torn write.

The temp file's `.tmp` suffix deliberately matches one of the extensions
`tools/ws/validate.py::check_interrupted_mutations` already watches for --
if a write is killed before the replace, the orphaned temp file is exactly
the artifact that detector is built to find. On success the temp file never
persists, so nothing is left for that check to flag.

The temp filename must NOT start with a dot: `check_interrupted_mutations`
matches siblings via `sname.startswith(file_path.stem)` (e.g. "active" for
"active.md"), so a leading-dot name like ".active.md.<rand>.tmp" silently
fails to match -- confirmed by a failing test during implementation. The
prefix below starts with the real filename so the match succeeds.

Scope: this module hardens the `active.md` write path only (WO
2026-08-16-004 Decision 1/2). The remaining tools/ws writers are deliberately
untouched here -- see that Work Object's Non-goals.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, content: str) -> None:
    """Write `content` to `path`, atomically.

    On any failure before the swap, the temp file is removed and the
    original `path` is left untouched.
    """
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=parent, prefix=f"{path.name}.", suffix=".tmp")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
