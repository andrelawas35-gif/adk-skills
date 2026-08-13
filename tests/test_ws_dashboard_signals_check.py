"""Focused checks for the workspace-level dashboard-signals validate check.

Cases:
  1. Both non-zero gauge counts are reported as warnings and `ws validate`
     still exits 0 (advisory).
  2. Both counts zero -> the check is silent and produces no errors.
  3. A malformed CLM- heading fails closed as a validation error (matching the
     readers' ValueError contract), not as a warning.
"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tools.ws.validate import check_dashboard_signals, run_checks


def _write_object(objects_dir: Path, rel: str, body: str) -> Path:
    path = objects_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: 2026-08-09-999\n---\n" + body)
    return path


def _claims_body(claims: str) -> str:
    return "## Intent\n\nFixture for the dashboard-signals check.\n\n" \
        f"## Claims\n\n{claims}\n"


class DashboardSignalsCheckTest(unittest.TestCase):
    def test_reports_both_counts_as_warnings_and_exits_zero(self):
        body = _claims_body(
            "  CONF-2026_08_09_999-001:\n"
            "  CLM-2026_08_09_999-001:\n"
            '    text: "single-sourced claim"\n'
            "    kind: inference\n"
            "    state: captured\n"
            '    scope: "refs/one"\n'
            "    created_at: 2026-08-09T00:00:00Z\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp) / ".work-studio" / "objects"
            _write_object(objects_dir, "2026/08/2026-08-09-999-fixture.md", body)

            warnings, errors = check_dashboard_signals(objects_dir)

            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 2)
            self.assertIn("1 unresolved conflict", warnings[0])
            self.assertIn("1 claim(s) below support adequacy", warnings[1])

            # Advisory: the full default run still exits 0 and prints the gauge.
            stderr = io.StringIO()
            stdout = io.StringIO()
            with redirect_stderr(stderr), redirect_stdout(stdout):
                result = run_checks(None, [], objects_dir=objects_dir)

            self.assertEqual(result, 0)
            self.assertIn("unresolved conflict", stderr.getvalue())
            self.assertIn("All default validation checks passed.", stdout.getvalue())

    def test_silent_when_counts_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp) / ".work-studio" / "objects"
            _write_object(
                objects_dir,
                "2026/08/2026-08-09-998-fixture.md",
                "## Intent\n\nNo claims.\n",
            )
            warnings, errors = check_dashboard_signals(objects_dir)
            self.assertEqual(warnings, [])
            self.assertEqual(errors, [])

    def test_malformed_claim_heading_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp) / ".work-studio" / "objects"
            _write_object(
                objects_dir,
                "2026/08/2026-08-09-997-fixture.md",
                "## Claims\n\n  CLM-BROKEN:\n",
            )
            warnings, errors = check_dashboard_signals(objects_dir)
            self.assertEqual(warnings, [])
            self.assertEqual(len(errors), 1)
            self.assertIn("malformed claim heading", errors[0])


if __name__ == "__main__":
    unittest.main()
