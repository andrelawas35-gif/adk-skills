"""Focused checks for the unresolved-conflicts dashboard reader."""

import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from tools.ws.dashboard_signals import count_unresolved_conflicts


@contextmanager
def workspace_with_claims(claims: str):
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        objects = root / ".work-studio" / "objects" / "2026" / "07"
        objects.mkdir(parents=True)
        (objects / "2026-07-28-999-fixture.md").write_text(
            f"## Claims\n\n{claims}\n"
        , encoding="utf-8")
        os.chdir(root)
        try:
            yield
        finally:
            os.chdir(previous)


class DashboardSignalsTest(unittest.TestCase):
    def test_counts_canonical_conflict_heading(self):
        with workspace_with_claims("  CONF-2026_07_28_999-001:"):
            self.assertEqual(count_unresolved_conflicts(), 1)

    def test_matching_confres_record_removes_conflict_from_unresolved_count(self):
        claims = (
            "  CONF-2026_07_28_999-001:\n"
            "    claim_id: CLM-2026_07_28_999-001\n"
            "  CONFRES-2026_07_28_999-001:\n"
            "    conflict_id: CONF-2026_07_28_999-001\n"
            "    disposition: superseded\n"
        )
        with workspace_with_claims(claims):
            self.assertEqual(count_unresolved_conflicts(), 0)

    def test_confres_heading_does_not_trigger_malformed_conflict_guard(self):
        claims = (
            "  CONF-2026_07_28_999-001:\n"
            "  CONFRES-2026_07_28_999-001:\n"
            "    conflict_id: CONF-2026_07_28_999-001\n"
        )
        with workspace_with_claims(claims):
            self.assertEqual(count_unresolved_conflicts(), 0)

    def test_conflict_id_field_without_confres_does_not_resolve_conflict(self):
        claims = (
            "  CONF-2026_07_28_999-001:\n"
            "    conflict_id: CONF-2026_07_28_999-001\n"
        )
        with workspace_with_claims(claims):
            self.assertEqual(count_unresolved_conflicts(), 1)

    def test_malformed_conflict_heading_fails_visibly(self):
        for heading in ("  CONF-BROKEN:", "  CONF-BROKEN"):
            with self.subTest(heading=heading):
                with workspace_with_claims(heading):
                    with self.assertRaisesRegex(
                        ValueError,
                        r"2026-07-28-999-fixture\.md: malformed conflict heading: CONF-BROKEN",
                    ):
                        count_unresolved_conflicts()


if __name__ == "__main__":
    unittest.main()
