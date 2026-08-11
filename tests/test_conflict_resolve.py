"""Focused checks for appending conflict-resolution records."""

import argparse
import io
import os
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path

from tools.ws.conflict import cmd_conflict_resolve
from tools.ws.dashboard_signals import count_unresolved_conflicts
from tools.ws.schema import parse_frontmatter


@contextmanager
def workspace_with_conflict():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        objects = root / ".work-studio" / "objects" / "2026" / "07"
        objects.mkdir(parents=True)
        obj = objects / "2026-07-28-999-fixture.md"
        obj.write_text(
            "---\n"
            "schema_version: 1\n"
            "id: 2026-07-28-999\n"
            "updated_at: 2026-07-27T17:39:01Z\n"
            "---\n"
            "## Claims\n\n"
            "  CONF-2026_07_28_999-001:\n"
            "    claim_id: CLM-2026_07_28_999-001\n"
            "    versions:\n"
            "      - commit_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
            "        file_path: \"fixtures/source-a.md\"\n"
            "        dirty_hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
            "      - commit_sha: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"
            "        file_path: \"fixtures/source-b.md\"\n"
            "        dirty_hash: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"
            "    created_at: 2026-07-27T17:39:01Z\n"
        )
        os.chdir(root)
        try:
            yield obj
        finally:
            os.chdir(previous)


@contextmanager
def workspace_with_cross_object_conflict(
    target_status: str = "active",
    preexisting_resolution: bool = False,
):
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source_dir = root / ".work-studio" / "objects" / "2026" / "07"
        target_dir = root / ".work-studio" / "objects" / "2026" / "08"
        source_dir.mkdir(parents=True)
        target_dir.mkdir(parents=True)
        source = source_dir / "2026-07-27-019-closed-source.md"
        target = target_dir / "2026-08-09-002-active-successor.md"
        source.write_text(
            "---\n"
            "schema_version: 1\n"
            "id: 2026-07-27-019\n"
            "status: closed\n"
            "state: close\n"
            "updated_at: 2026-07-27T16:16:01Z\n"
            "---\n"
            "## Claims\n\n"
            "  CONF-2026_07_27_019-001:\n"
            "    claim_id: CLM-2026_07_27_019-001\n"
            "    versions:\n"
            "      - commit_sha: aefd8623\n"
            "        file_path: \"skills/core/thinking-pressure-test-decision/SKILL.md\"\n"
            "        dirty_hash: clean\n"
            "      - commit_sha: unknown\n"
            "        file_path: \"~/.claude/skills/alawas-thinking-pressure-test-decision/SKILL.md\"\n"
            "        dirty_hash: install-drift\n"
            "    created_at: 2026-07-27T16:16:01Z\n"
        )
        resolution = ""
        if preexisting_resolution:
            resolution = (
                "\n"
                "  CONFRES-2026_08_09_002-001:\n"
                "    conflict_id: CONF-2026_07_27_019-001\n"
                "    source_object_id: 2026-07-27-019\n"
                "    resolver: codex\n"
                "    disposition: superseded\n"
                "    rationale: \"Already resolved.\"\n"
                "    timestamp: 2026-08-10T00:00:00Z\n"
            )
        target.write_text(
            "---\n"
            "schema_version: 1\n"
            "id: 2026-08-09-002\n"
            f"status: {target_status}\n"
            "state: build\n"
            "updated_at: 2026-08-10T00:00:00Z\n"
            "---\n"
            "## Claims\n"
            f"{resolution}"
        )
        os.chdir(root)
        try:
            yield source, target
        finally:
            os.chdir(previous)


class ConflictResolveTest(unittest.TestCase):
    def test_resolve_appends_confres_and_leaves_conflict_block_intact(self):
        with workspace_with_conflict() as obj:
            before = obj.read_text()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = cmd_conflict_resolve(argparse.Namespace(
                    id="2026-07-28-999",
                    conflict_id="CONF-2026_07_28_999-001",
                    resolver="codex",
                    disposition="superseded",
                    rationale="Synthetic fixture resolution.",
                    record_in=None,
                    expect_updated="2026-07-27T17:39:01Z",
                    force=False,
                ))

            self.assertEqual(result, 0)
            self.assertIn(
                "Conflict resolution CONFRES-2026_07_28_999-001 registered",
                stdout.getvalue(),
            )
            after = obj.read_text()
            self.assertIn("  CONF-2026_07_28_999-001:", after)
            self.assertIn("  CONFRES-2026_07_28_999-001:", after)
            self.assertIn("    conflict_id: CONF-2026_07_28_999-001", after)
            self.assertIn("    resolver: codex", after)
            self.assertIn("    disposition: superseded", after)
            self.assertIn('    rationale: "Synthetic fixture resolution."', after)
            self.assertIn("    timestamp: ", after)
            self.assertIn(
                before.split("  CONF-2026_07_28_999-001:", 1)[1].strip(),
                after,
            )
            self.assertNotEqual(
                parse_frontmatter(after)["updated_at"],
                "2026-07-27T17:39:01Z",
            )
            self.assertEqual(
                count_unresolved_conflicts(obj.parents[2]),
                0,
            )

    def test_record_in_appends_resolution_to_successor_without_mutating_source(self):
        with workspace_with_cross_object_conflict() as (source, target):
            source_before = source.read_text()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = cmd_conflict_resolve(argparse.Namespace(
                    id="2026-07-27-019",
                    conflict_id="CONF-2026_07_27_019-001",
                    resolver="codex",
                    disposition="superseded",
                    rationale="Closed-object source resolved in successor.",
                    record_in="2026-08-09-002",
                    expect_updated="2026-08-10T00:00:00Z",
                    force=False,
                ))

            self.assertEqual(result, 0)
            self.assertIn(
                "Conflict resolution CONFRES-2026_08_09_002-001 registered in 2026-08-09-002",
                stdout.getvalue(),
            )
            self.assertEqual(source.read_text(), source_before)
            target_after = target.read_text()
            self.assertIn("  CONFRES-2026_08_09_002-001:", target_after)
            self.assertIn("    conflict_id: CONF-2026_07_27_019-001", target_after)
            self.assertIn("    source_object_id: 2026-07-27-019", target_after)
            self.assertIn("    disposition: superseded", target_after)
            self.assertEqual(count_unresolved_conflicts(source.parents[2]), 0)

    def test_record_in_rejects_closed_target_without_append(self):
        with workspace_with_cross_object_conflict(target_status="closed") as (source, target):
            target_before = target.read_text()
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = cmd_conflict_resolve(argparse.Namespace(
                    id="2026-07-27-019",
                    conflict_id="CONF-2026_07_27_019-001",
                    resolver="codex",
                    disposition="superseded",
                    rationale="Should not append to a closed target.",
                    record_in="2026-08-09-002",
                    expect_updated="2026-08-10T00:00:00Z",
                    force=False,
                ))

            self.assertEqual(result, 1)
            self.assertIn("closed object 2026-08-09-002", stderr.getvalue())
            self.assertEqual(target.read_text(), target_before)
            self.assertEqual(count_unresolved_conflicts(source.parents[2]), 1)

    def test_record_in_rejects_missing_source_conflict_without_append(self):
        with workspace_with_cross_object_conflict() as (source, target):
            target_before = target.read_text()
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = cmd_conflict_resolve(argparse.Namespace(
                    id="2026-07-27-019",
                    conflict_id="CONF-2026_07_27_019-999",
                    resolver="codex",
                    disposition="superseded",
                    rationale="Should not append for a missing source conflict.",
                    record_in="2026-08-09-002",
                    expect_updated="2026-08-10T00:00:00Z",
                    force=False,
                ))

            self.assertEqual(result, 1)
            self.assertIn("not found in 2026-07-27-019", stderr.getvalue())
            self.assertEqual(target.read_text(), target_before)
            self.assertEqual(count_unresolved_conflicts(source.parents[2]), 1)

    def test_record_in_rejects_duplicate_resolution_anywhere(self):
        with workspace_with_cross_object_conflict(preexisting_resolution=True) as (source, target):
            target_before = target.read_text()
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = cmd_conflict_resolve(argparse.Namespace(
                    id="2026-07-27-019",
                    conflict_id="CONF-2026_07_27_019-001",
                    resolver="codex",
                    disposition="superseded",
                    rationale="Should not append duplicate resolution.",
                    record_in="2026-08-09-002",
                    expect_updated="2026-08-10T00:00:00Z",
                    force=False,
                ))

            self.assertEqual(result, 1)
            self.assertIn("already has a CONFRES- record", stderr.getvalue())
            self.assertEqual(target.read_text(), target_before)
            self.assertEqual(count_unresolved_conflicts(source.parents[2]), 0)


if __name__ == "__main__":
    unittest.main()
