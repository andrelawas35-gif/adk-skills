#!/usr/bin/env python3
"""Multi-process concurrent runs test for the Phase 6 graph (WO 2026-08-17-008).

Proves slice 11's assumption: two independent Phase 6 runs launched concurrently
in separate processes (separate threads, separate checkpoint DBs) both complete
correctly -- each firing its join exactly once with the deterministic state-
routed proposal -- without interfering with each other or with canonical state.

Run under the uv-managed Python 3.11 environment:

    uv run python -m unittest discover -s runtime/tests -v
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime.graph import inspect_phase6

ROOT = Path(__file__).resolve().parents[2]
TARGET_WO = "2026-08-22-011"
GRAPH_MODULE = ["-m", "runtime.graph"]
EXPECTED_PROPOSAL = "implement-bounded-change"  # state "build" routing


def _digest_work_studio() -> str:
    """Hash every canonical file so any change is observable."""
    h = hashlib.sha256()
    for p in sorted(ROOT.glob(".work-studio/**/*")):
        if p.is_file():
            h.update(str(p.relative_to(ROOT)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _run_phase6_cli(thread_id, checkpoint_db, resume=False, env_extra=None):
    args = [
        sys.executable, *GRAPH_MODULE, "run-phase6", TARGET_WO, thread_id,
        "--checkpoint-db", str(checkpoint_db),
    ]
    if resume:
        args.append("--resume")
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        args, cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=120
    )


class Phase6ConcurrentTests(unittest.TestCase):

    def test_two_concurrent_runs_complete_independently(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            db_a = tmp / "a.sqlite"
            db_b = tmp / "b.sqlite"
            before = _digest_work_studio()

            # Launch both subprocesses concurrently (separate threads + DBs).
            p_a = subprocess.Popen(
                [sys.executable, *GRAPH_MODULE, "run-phase6", TARGET_WO, "conc-a",
                 "--checkpoint-db", str(db_a)],
                cwd=str(ROOT), env=dict(os.environ),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            p_b = subprocess.Popen(
                [sys.executable, *GRAPH_MODULE, "run-phase6", TARGET_WO, "conc-b",
                 "--checkpoint-db", str(db_b)],
                cwd=str(ROOT), env=dict(os.environ),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            out_a, err_a = p_a.communicate(timeout=120)
            out_b, err_b = p_b.communicate(timeout=120)
            self.assertEqual(0, p_a.returncode, err_a)
            self.assertEqual(0, p_b.returncode, err_b)

            payload_a = json.loads(out_a)
            payload_b = json.loads(out_b)
            self.assertTrue(payload_a["join_fired"])
            self.assertTrue(payload_b["join_fired"])
            self.assertEqual(EXPECTED_PROPOSAL, payload_a["join_proposal"])
            self.assertEqual(EXPECTED_PROPOSAL, payload_b["join_proposal"])

            # Each checkpoint DB is independent: its own thread completed.
            self.assertTrue(inspect_phase6("conc-a", db_a)["join_fired"])
            self.assertTrue(inspect_phase6("conc-b", db_b)["join_fired"])

            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across concurrent runs",
            )

    def test_concurrent_resume_variant(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            crash_marker = tmp / "crash.txt"
            db_crash = tmp / "crash.sqlite"
            db_ok = tmp / "ok.sqlite"
            before = _digest_work_studio()

            crash_env = {
                "PHASE6_CRASH_NODE": "join",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }

            # Launch concurrently: one crashes before join, one completes.
            p_crash = subprocess.Popen(
                [sys.executable, *GRAPH_MODULE, "run-phase6", TARGET_WO, "crash-t",
                 "--checkpoint-db", str(db_crash)],
                cwd=str(ROOT), env={**os.environ, **crash_env},
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            p_ok = subprocess.Popen(
                [sys.executable, *GRAPH_MODULE, "run-phase6", TARGET_WO, "ok-t",
                 "--checkpoint-db", str(db_ok)],
                cwd=str(ROOT), env=dict(os.environ),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            out_crash, err_crash = p_crash.communicate(timeout=120)
            out_ok, err_ok = p_ok.communicate(timeout=120)

            # The crash run exits nonzero (Phase6Crash); the ok run completes.
            self.assertNotEqual(0, p_crash.returncode, err_crash)
            self.assertEqual(0, p_ok.returncode, err_ok)
            self.assertTrue(json.loads(out_ok)["join_fired"])

            # Resume the crashed thread: join fires exactly once.
            r = _run_phase6_cli(
                "crash-t", db_crash, resume=True, env_extra=crash_env
            )
            self.assertEqual(0, r.returncode, r.stderr)
            payload = json.loads(r.stdout)
            self.assertTrue(payload["join_fired"])
            self.assertEqual(EXPECTED_PROPOSAL, payload["join_proposal"])

            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across concurrent resume",
            )


if __name__ == "__main__":
    unittest.main()
