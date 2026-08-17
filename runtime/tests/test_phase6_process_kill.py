#!/usr/bin/env python3
"""Process-boundary kill/resume test for the Phase 6 graph (WO 2026-08-17-008).

Proves slice 4's riskiest assumption: a real SIGKILL (ungraceful process exit)
after the branch superstep commits resumes from the SQLite checkpoint without
re-running the completed branches and fires the join exactly once.

Run under the uv-managed Python 3.11 environment:

    uv run python -m unittest discover -s runtime/tests -v
"""

import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_WO = "2026-07-27-001"
GRAPH_MODULE = ["-m", "runtime.graph"]


def _digest_work_studio() -> str:
    """Hash every canonical file so any change is observable."""
    h = hashlib.sha256()
    for p in sorted(ROOT.glob(".work-studio/**/*")):
        if p.is_file():
            h.update(str(p.relative_to(ROOT)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


class Phase6ProcessKillTests(unittest.TestCase):

    def test_kill_after_branch_superstep_resumes_without_reexecution(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            branch_marker = tmp / "branches.txt"
            join_signal = tmp / "join_started"

            before = _digest_work_studio()

            # ── Run 1: pause in the join (after branches commit), then SIGKILL.
            env1 = dict(os.environ)
            env1["PHASE6_BRANCH_MARKER"] = str(branch_marker)
            env1["PHASE6_JOIN_SIGNAL_FILE"] = str(join_signal)
            env1["PHASE6_JOIN_SLEEP_SECONDS"] = "60"  # wide window to kill
            proc = subprocess.Popen(
                [sys.executable, *GRAPH_MODULE, "run-phase6",
                 TARGET_WO, "process-kill-test",
                 "--checkpoint-db", str(checkpoint_db)],
                cwd=str(ROOT), env=env1,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )

            # Wait (bounded) for the join to signal, proving branches committed.
            deadline = time.time() + 60
            while time.time() < deadline and not join_signal.exists():
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    self.fail(f"graph exited before join signal: {out} {err}")
                time.sleep(0.05)
            self.assertTrue(join_signal.exists(), "join never signaled")

            # Both branches recorded exactly one side effect before the kill.
            marker_lines = branch_marker.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(marker_lines),
                             f"branch side-effect count: {len(marker_lines)}")

            proc.send_signal(signal.SIGKILL)
            proc.wait(timeout=10)
            proc.communicate()  # close the killed process's pipes

            # ── Run 2: resume the same thread_id without the pause hook.
            env2 = dict(os.environ)
            env2["PHASE6_BRANCH_MARKER"] = str(branch_marker)  # keep counting
            result = subprocess.run(
                [sys.executable, *GRAPH_MODULE, "run-phase6",
                 TARGET_WO, "process-kill-test",
                 "--checkpoint-db", str(checkpoint_db), "--resume"],
                cwd=str(ROOT), env=env2, capture_output=True, text=True,
                timeout=120,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["join_fired"])
            # WO 2026-08-17-001 Decision 6 + Phase 6 Decision 11: derive_proposal
            # returns the real skill name (state-keyed) and the join deduplicates,
            # so TARGET_WO (state "build") yields a single "implement-bounded-change".
            self.assertEqual(
                "implement-bounded-change",
                payload["join_proposal"],
            )

            # Branches must NOT have re-executed after the kill.
            marker_lines = branch_marker.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(marker_lines),
                             f"branch re-executed: {len(marker_lines)} lines")

            # Canonical state must be byte-identical across kill + resume.
            after = _digest_work_studio()
            self.assertEqual(before, after,
                             "canonical state changed across kill/resume")


if __name__ == "__main__":
    unittest.main()
