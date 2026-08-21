#!/usr/bin/env python3
"""Regression tests for ws backup / ws restore (WO 2026-08-14-009).

Exit criteria from the accepted tracer bullet (Decision 2): backup -> delete
objects/ -> restore -> file content identical to the pre-deletion baseline.
Plus the three failure-mode guards: empty source, unknown timestamp, and
refusing to overwrite a non-empty destination.

Isolated via a temp HOME (BACKUP_ROOT is Path.home() / ".work-studio-backups")
and a temp workspace root, so this never touches the real corpus or the
real ~/.work-studio-backups/. Dependency-free -- stdlib unittest + mock only.
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.ws import backup as ws_backup


def make_workspace(root: Path, file_count: int = 3) -> Path:
    objects_dir = root / ".work-studio" / "objects" / "2026" / "08"
    objects_dir.mkdir(parents=True, exist_ok=True)
    for i in range(1, file_count + 1):
        (objects_dir / f"2026-08-14-{i:03d}.md").write_text(
            f"---\nid: 2026-08-14-{i:03d}\n---\nbody {i}\n"
        , encoding="utf-8")
    return root


class Args:
    """Minimal argparse.Namespace stand-in."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class WsBackupRestoreTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "workspace"
        self.home = Path(self._tmp.name) / "home"
        self.root.mkdir()
        self.home.mkdir()
        self.backup_root = self.home / ".work-studio-backups"

        self._patches = [
            mock.patch.object(ws_backup, "BACKUP_ROOT", self.backup_root),
            mock.patch.object(ws_backup, "_find_work_studio_root", return_value=self.root),
        ]
        for p in self._patches:
            p.start()
            self.addCleanup(p.stop)

    def test_backup_then_restore_round_trip_is_identical(self):
        make_workspace(self.root, file_count=3)
        source_dir = self.root / ".work-studio" / "objects"
        before = {
            p.relative_to(source_dir): p.read_bytes()
            for p in source_dir.rglob("*") if p.is_file()
        }

        rc = ws_backup.cmd_backup(Args())
        self.assertEqual(rc, 0)

        backups = list(self.backup_root.iterdir())
        self.assertEqual(len(backups), 1)
        timestamp = backups[0].name

        import shutil
        shutil.rmtree(source_dir)
        self.assertFalse(source_dir.exists())

        rc = ws_backup.cmd_restore(Args(timestamp=timestamp))
        self.assertEqual(rc, 0)

        after = {
            p.relative_to(source_dir): p.read_bytes()
            for p in source_dir.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after)

    def test_backup_refuses_empty_source(self):
        (self.root / ".work-studio" / "objects").mkdir(parents=True)
        rc = ws_backup.cmd_backup(Args())
        self.assertEqual(rc, 1)
        self.assertFalse(self.backup_root.exists() and any(self.backup_root.iterdir()))

    def test_restore_refuses_unknown_timestamp(self):
        make_workspace(self.root, file_count=1)
        rc = ws_backup.cmd_restore(Args(timestamp="19990101T000000Z"))
        self.assertEqual(rc, 1)

    def test_restore_refuses_nonempty_destination(self):
        make_workspace(self.root, file_count=2)
        rc = ws_backup.cmd_backup(Args())
        self.assertEqual(rc, 0)
        timestamp = next(self.backup_root.iterdir()).name

        # Destination still has its original 2 files -- restore must refuse.
        rc = ws_backup.cmd_restore(Args(timestamp=timestamp))
        self.assertEqual(rc, 1)
        # Original files must be untouched by the refused restore.
        source_dir = self.root / ".work-studio" / "objects"
        self.assertEqual(
            sum(1 for p in source_dir.rglob("*") if p.is_file()), 2
        )


if __name__ == "__main__":
    unittest.main()
