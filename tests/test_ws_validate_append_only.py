"""Regression tests for the append-only enforcement check in ws.validate.

Covers the new check built by 2026-08-09-003 and scoped by Decision 12 on that
object (implemented via 2026-08-11-020): ws.validate.check_append_only,
check_append_only_baseline, _find_snapshot, and _entry_timestamps.

These functions operate on Work Object FILE paths and diff protected sections
against a local .bak-<ts> snapshot sibling — distinct from the older
ws.sections.check_append_only(body, section, entry) helper, which is tested
elsewhere in test_ws_cli.py.
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.validate import (
    check_append_only,
    check_append_only_baseline,
    _find_snapshot,
    _entry_timestamps,
)


# A minimal, schema-shaped Work Object fixture with all four protected sections
# populated. The History heading and Evidence entry lead with the same
# whole-second timestamp 2026-08-11T00:00:00Z (different sections, so no
# collision). The Evidence entry cell leads with a timestamp to exercise the
# entry-cell-leading rule.
FIXTURE = """---
schema_version: 1
id: 2026-08-11-900
title: Regression fixture for ws.validate append-only check
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-11T00:00:00Z
updated_at: 2026-08-11T00:00:00Z
---
## Intent

Regression fixture for the ws.validate append-only check.

## Success evidence

- [ ] fixture

## Constraints and non-goals

**Constraints:** fixture

**Non-goals:** none

## Decisions and revisit triggers

### Decision 1 — fixture

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | fixture |
| **Authorization** | fixture |
| **Confidence** | high |
| **Actor** | fixture |
| **Revisit trigger** | none |
| **Rationale** | fixture |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | fixture | 2026-08-11T00:00:00Z initial |

## Open questions

none

## Next move

fixture

## History

### 2026-08-11T00:00:00Z — Created

- **State:** notice
- **Status:** active
- **Actor:** fixture
- **Rationale:** fixture
"""


class TestWsValidateAppendOnly(unittest.TestCase):
    """Regression tests for the new ws.validate append-only check functions."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.path = self.dir / "2026-08-11-900-fixture.md"
        self.snapshot = self.dir / "2026-08-11-900-fixture.md.bak-20260811T000000Z"
        self._write_fixture()

    def tearDown(self):
        self._tmp.cleanup()

    def _write_fixture(self):
        """(Re)write the live fixture and its snapshot as identical baselines."""
        self.path.write_text(FIXTURE, encoding="utf-8")
        self.snapshot.write_text(FIXTURE, encoding="utf-8")

    # ── _find_snapshot ────────────────────────────────────────────────────

    def test_find_snapshot_returns_most_recent(self):
        # _find_snapshot sorts .bak-* siblings lexicographically and returns
        # the last, matching real timestamps where a later timestamp is a
        # lexicographically larger string.
        newer = self.dir / "2026-08-11-900-fixture.md.bak-20260811T000002Z"
        newer.write_text(FIXTURE, encoding="utf-8")
        self.assertEqual(_find_snapshot(self.path), newer)

    def test_find_snapshot_none_when_absent(self):
        self.snapshot.unlink()
        self.assertIsNone(_find_snapshot(self.path))

    # ── check_append_only: clean baseline ────────────────────────────────

    def test_clean_baseline_passes(self):
        self.assertEqual(check_append_only(self.path), [])

    # ── check_append_only: seeded violation (criterion: fails on edit) ───

    def test_seeded_edit_to_history_fails(self):
        mutated = FIXTURE.replace("- **Rationale:** fixture", "- **Rationale:** fixture!")
        self.path.write_text(mutated, encoding="utf-8")
        errors = check_append_only(self.path)
        self.assertTrue(
            any("append-only violation" in e and "'history'" in e for e in errors),
            f"expected a history violation, got: {errors}",
        )

    def test_seeded_edit_to_evidence_fails(self):
        mutated = FIXTURE.replace("| [system] | fixture |", "| [system] | fixturex |")
        self.path.write_text(mutated, encoding="utf-8")
        errors = check_append_only(self.path)
        self.assertTrue(
            any("append-only violation" in e and "'evidence ledger'" in e for e in errors),
            f"expected an evidence-ledger violation, got: {errors}",
        )

    # ── check_append_only: append is allowed (criterion: passes on append)

    def test_append_new_history_passes(self):
        self._write_fixture()
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(
                "\n### 2026-08-11T00:01:00Z — Appended\n"
                "\n- **State:** build\n"
                "- **Status:** active\n"
                "- **Actor:** fixture\n"
                "- **Rationale:** fixture append\n"
            )
        self.assertEqual(check_append_only(self.path), [])

    # ── check_append_only: duplicate whole-second timestamps ─────────────

    def test_duplicate_whole_second_timestamp_fails(self):
        self._write_fixture()
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(
                "\n### 2026-08-11T00:00:00Z — Duplicate timestamp\n"
                "\n- **State:** build\n"
                "- **Status:** active\n"
                "- **Actor:** fixture\n"
                "- **Rationale:** fixture duplicate\n"
            )
        errors = check_append_only(self.path)
        self.assertTrue(
            any("duplicate whole-second timestamp" in e and "'history'" in e for e in errors),
            f"expected a duplicate-timestamp error, got: {errors}",
        )

    # ── check_append_only_baseline: no-baseline explicit warning ─────────

    def test_no_baseline_reports_explicit_warning(self):
        self.snapshot.unlink()
        warnings = check_append_only_baseline(self.path)
        self.assertEqual(len(warnings), 1)
        self.assertIn("no baseline snapshot", warnings[0])

    def test_no_baseline_never_silent_pass(self):
        # Without a snapshot the diff check cannot run, so check_append_only
        # returns no *violation* error — but the explicit no-baseline warning is
        # what surfaces it (never a silent pass).
        self.snapshot.unlink()
        self.assertEqual(check_append_only(self.path), [])
        self.assertEqual(len(check_append_only_baseline(self.path)), 1)

    # ── _entry_timestamps: per-section entry-identifier rule ─────────────

    def test_entry_timestamps_history_headings_only(self):
        text = (
            "### 2026-08-11T00:00:00Z — Created\n"
            "\n"
            "- **Note:** prose mentioning 2026-08-11T00:05:00Z is not an entry\n"
            "### 2026-08-11T00:01:00Z — Second\n"
        )
        self.assertEqual(
            _entry_timestamps(text, "history"),
            ["2026-08-11T00:00:00", "2026-08-11T00:01:00"],
        )

    def test_entry_timestamps_evidence_entry_cell_leading(self):
        text = (
            "| Tag | Source | Entry |\n"
            "|-----|--------|-------|\n"
            "| [system] | src | 2026-08-11T00:00:00Z initial |\n"
            "| [system] | src | note at 2026-08-11T00:05:00Z (mid-cell, not leading) |\n"
        )
        self.assertEqual(_entry_timestamps(text, "evidence ledger"), ["2026-08-11T00:00:00"])

    def test_entry_timestamps_claims_bullet_leading(self):
        text = (
            "- 2026-08-11T00:00:00Z claim with a leading timestamp\n"
            "- prose mention of 2026-08-11T00:05:00Z is not a bullet-leading entry\n"
        )
        self.assertEqual(_entry_timestamps(text, "claims"), ["2026-08-11T00:00:00"])

    def test_entry_timestamps_decisions_not_scanned(self):
        text = (
            "### Decision 1 — fixture\n"
            "\n"
            "A date-time string like 2026-08-11T00:00:00Z in a Decision body is prose.\n"
        )
        self.assertEqual(_entry_timestamps(text, "decisions and revisit triggers"), [])


if __name__ == "__main__":
    unittest.main()
