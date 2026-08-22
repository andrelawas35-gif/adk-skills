#!/usr/bin/env python3
"""Regression tests proving tools/runtime/tracer.py's Decision-3 exit
criteria (WO 2026-08-15-001, Decision 4): the traced Work Object's
`updated_at` is byte-identical before and after a run, for both the
continue (y) and stop (N) interrupt answers.

Invocation: the tracer resolves its own repo root by walking up from cwd
for a `.work-studio/` directory, then subprocess-invokes
`python3 -m tools.ws validate` with that root as cwd -- so `tools.ws` must
be importable there. A synthetic sandboxed workspace would break that inner
call. These tests instead run the tracer as a subprocess against the real
repository (matching how it was manually verified twice in WO
2026-08-14-008), targeting a stable, low-consequence, dedicated build-state Work Object
that is dedicated and low-consequence (2026-08-22-011) so no other test or session
activity can race it. Read-only against `.work-studio/objects/`; the only
side effect is a gitignored trace log under `runtime/traces/`, cleaned up
after each test.

Dependency-free -- standard-library subprocess + unittest only, matching
the repo convention. Run with:

    python3 -m unittest discover -s tests -v
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_WO_GLOB = "2026-08-22-011-*.md"


def _find_target() -> Path:
    matches = sorted(ROOT.glob(f".work-studio/objects/*/*/{TARGET_WO_GLOB}"))
    if not matches:
        raise FileNotFoundError(f"Demo Work Object not found: {TARGET_WO_GLOB}")
    return matches[0]


def _read_updated_at(file_path: Path) -> str:
    text = file_path.read_text(encoding="utf-8")
    match = re.search(r"^updated_at:\s*(\S+)", text, re.MULTILINE)
    return match.group(1) if match else None


def _run_tracer(answer: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.runtime.tracer", "2026-08-22-011"],
        cwd=ROOT, input=f"{answer}\n", capture_output=True, text=True, encoding="utf-8",
    )


class RuntimeTracerTest(unittest.TestCase):
    def setUp(self):
        self.target = _find_target()
        self.before_traces = set((ROOT / "runtime" / "traces").glob("*.jsonl")) \
            if (ROOT / "runtime" / "traces").is_dir() else set()

    def tearDown(self):
        traces_dir = ROOT / "runtime" / "traces"
        if traces_dir.is_dir():
            after = set(traces_dir.glob("*.jsonl"))
            for new_trace in after - self.before_traces:
                new_trace.unlink()

    def test_continue_run_completes_with_unchanged_updated_at(self):
        before = _read_updated_at(self.target)
        result = _run_tracer("y")
        after = _read_updated_at(self.target)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, after)
        self.assertIn('"outcome": "completed"', result.stdout)
        self.assertIn('"canonical_state_unchanged": true', result.stdout)

    def test_stop_run_halts_cleanly_with_unchanged_updated_at(self):
        before = _read_updated_at(self.target)
        result = _run_tracer("n")
        after = _read_updated_at(self.target)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, after)
        self.assertIn('"outcome": "stopped_by_director"', result.stdout)

    def test_unknown_work_object_id_fails_without_touching_anything(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.runtime.tracer", "9999-99-99-999"],
            cwd=ROOT, input="y\n", capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn('"event": "failed"', result.stdout)


if __name__ == "__main__":
    unittest.main()
