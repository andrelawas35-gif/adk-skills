"""Tests for ws engineering-handoff inspect|approve|reject (WO 2026-08-22-025).

Sets up a temp workspace + Phase 6 checkpoint with an engineering payload,
then exercises the CLI command against the verified runtime exposure.
"""

import argparse
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
# REPO_ROOT must sit at sys.path[0] so `runtime` resolves before the editable
# work_studio_ws finder is consulted; TOOLS_DIR follows for `ws`.
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(REPO_ROOT))

from ws.engineering_handoff import cmd_engineering_handoff  # noqa: E402
from runtime.graph import run_phase6  # noqa: E402


WO_ID = "2026-08-22-900"
WO_FRONTMATTER = """---
schema_version: 1
id: 2026-08-22-900
title: Engineering handoff CLI fixture
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
engineering_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: CI failure and verification gap
---
## Intent

Engineering dispatch CLI fixture.

## Open questions

- CI failure and verification gap
"""


class EngineeringHandoffCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        obj_dir = self._tmp / ".work-studio" / "objects" / "2026" / "08"
        obj_dir.mkdir(parents=True)
        self.wo_path = obj_dir / f"{WO_ID}-engineering-cli-fixture.md"
        self.wo_path.write_text(WO_FRONTMATTER, encoding="utf-8")
        self.checkpoint_db = self._tmp / "phase6-engineering.sqlite"
        self._old_cwd = Path.cwd()
        os.chdir(self._tmp)

    def tearDown(self):
        os.chdir(self._old_cwd)
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _seed_engineering_payload(self, thread_id=WO_ID):
        """Run Phase 6 once so the checkpoint holds an engineering payload."""
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            run_phase6(WO_ID, thread_id, self.checkpoint_db)

    def _run_cmd(self, handoff_command, **kwargs):
        args = argparse.Namespace(
            id=WO_ID,
            thread_id=kwargs.get("thread_id"),
            checkpoint_db=str(self.checkpoint_db),
            handoff_command=handoff_command,
        )
        buf = io.StringIO()
        err_buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err_buf):
            rc = cmd_engineering_handoff(args)
        return rc, buf.getvalue(), err_buf.getvalue()

    def test_inspect_reports_no_handoff_when_checkpoint_empty(self):
        rc, out, _ = self._run_cmd("inspect")
        self.assertEqual(rc, 0)
        self.assertIn("no proposed engineering handoff", out)

    def test_inspect_shows_proposed_engineering_handoff(self):
        self._seed_engineering_payload()
        rc, out, _ = self._run_cmd("inspect")
        self.assertEqual(rc, 0)
        self.assertIn("engineering handoff proposed", out)
        self.assertIn("engineering-verify-release-evidence", out)

    def test_inspect_uses_thread_id_override(self):
        self._seed_engineering_payload(thread_id="custom-thread")
        rc, out, _ = self._run_cmd("inspect", thread_id="custom-thread")
        self.assertEqual(rc, 0)
        self.assertIn("engineering handoff proposed", out)

    def test_approve_records_history_and_evidence(self):
        self._seed_engineering_payload()
        rc, out, _ = self._run_cmd("approve")
        self.assertEqual(rc, 0)
        self.assertIn("Engineering handoff approved", out)

        text = self.wo_path.read_text(encoding="utf-8")
        self.assertIn("Engineering handoff approved", text)
        self.assertIn("Engineering handoff approved (to engineering-verify-release-evidence)",
                      text)
        self.assertIn("[decision]", text)

    def test_reject_records_history_and_evidence(self):
        self._seed_engineering_payload()
        rc, out, _ = self._run_cmd("reject")
        self.assertEqual(rc, 0)
        self.assertIn("Engineering handoff rejected", out)

        text = self.wo_path.read_text(encoding="utf-8")
        self.assertIn("Engineering handoff rejected", text)
        self.assertIn("[decision]", text)

    def test_decision_refuses_when_no_handoff(self):
        rc, _, err = self._run_cmd("approve")
        self.assertNotEqual(rc, 0)
        self.assertIn("no proposed engineering handoff to approve", err)
        text = self.wo_path.read_text(encoding="utf-8")
        self.assertNotIn("Engineering handoff approved", text)


if __name__ == "__main__":
    unittest.main()
