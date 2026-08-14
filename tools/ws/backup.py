"""Local filesystem backup and restore for .work-studio/objects/.

Two CLI commands (WO 2026-08-14-009, Decision 2 tracer bullet):
    - ``ws backup`` — copy .work-studio/objects/ to a timestamped directory
      under ~/.work-studio-backups/. No git, no network, no retention.
    - ``ws restore <timestamp>`` — copy a named backup's objects/ back into
      .work-studio/objects/. Refuses to overwrite a non-empty destination.

Scope (Decision 1/2): objects/ only. active.md and inbox.md share the same
.gitignore "private operational records" rationale but are deferred to a
separate follow-up decision, not bundled in here.
"""

import argparse
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


BACKUP_ROOT = Path.home() / ".work-studio-backups"


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


def _count_files(directory: Path) -> int:
    return sum(1 for p in directory.rglob("*") if p.is_file())


def cmd_backup(args: argparse.Namespace) -> int:
    """Copy .work-studio/objects/ to a new timestamped backup directory."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    source = ws_root / ".work-studio" / "objects"
    if not source.is_dir():
        print(
            f"Error: {source} does not exist or is not a directory. "
            "Nothing to back up.",
            file=sys.stderr,
        )
        return 1

    source_file_count = _count_files(source)
    if source_file_count == 0:
        print(f"Error: {source} is empty. Nothing to back up.", file=sys.stderr)
        return 1

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = BACKUP_ROOT / timestamp / "objects"

    # Copy to a temp directory first, then rename into place, so a failed
    # or interrupted copy never leaves a partial backup that looks valid.
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=BACKUP_ROOT) as tmp:
        tmp_dest = Path(tmp) / "objects"
        try:
            shutil.copytree(source, tmp_dest)
        except OSError as e:
            print(f"Error: backup copy failed: {e}", file=sys.stderr)
            return 1

        copied_file_count = _count_files(tmp_dest)
        if copied_file_count != source_file_count:
            print(
                f"Error: backup copy incomplete — source had "
                f"{source_file_count} files, copy has {copied_file_count}. "
                "Backup not finalized.",
                file=sys.stderr,
            )
            return 1

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tmp_dest), str(destination))

    print(f"Backup created: {destination}")
    print(f"  file_count: {copied_file_count}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    """Restore .work-studio/objects/ from a named backup timestamp."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    backup_dir = BACKUP_ROOT / args.timestamp / "objects"
    if not backup_dir.is_dir():
        print(
            f"Error: no backup found at {backup_dir}. "
            f"Run 'ws backup' to list available backups under {BACKUP_ROOT}.",
            file=sys.stderr,
        )
        return 1

    destination = ws_root / ".work-studio" / "objects"
    if destination.is_dir() and _count_files(destination) > 0:
        print(
            f"Error: {destination} is not empty. Refusing to overwrite. "
            "Move or remove it first if you intend to restore over it.",
            file=sys.stderr,
        )
        return 1

    backup_file_count = _count_files(backup_dir)
    try:
        if destination.exists():
            destination.rmdir()
        shutil.copytree(backup_dir, destination)
    except OSError as e:
        print(f"Error: restore copy failed: {e}", file=sys.stderr)
        return 1

    restored_file_count = _count_files(destination)
    if restored_file_count != backup_file_count:
        print(
            f"Error: restore incomplete — backup had {backup_file_count} "
            f"files, restored {restored_file_count}.",
            file=sys.stderr,
        )
        return 1

    print(f"Restored: {destination}")
    print(f"  file_count: {restored_file_count}")
    return 0
