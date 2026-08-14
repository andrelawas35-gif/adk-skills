"""Regression tests for the ws inputs read command (2026-08-14-001).

Covers the read-only citation extractor built by 2026-08-11-010 (Direction 2)
and scoped by Decision 5 on that object, implemented via successor
2026-08-14-001: ws.__main__.cmd_inputs / _extract_citations. Exercises
objects / files (with :line) / ADRs (both "ADR 0022" and "ADR-0022")
extraction, HTML-comment stripping, the read-only guarantee, and the clean
unknown-ID failure path.
"""

import argparse
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.__main__ import cmd_inputs, _extract_citations


# A minimal, schema-shaped Work Object fixture whose Intent, Decisions, and
# Evidence ledger cite an object ID, file paths with line refs, and both ADR
# spellings. The HTML comment at the end must be stripped (template metadata,
# not object content).
FIXTURE = """---
schema_version: 1
id: 2026-08-14-900
title: Regression fixture for ws inputs
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-14T00:00:00Z
updated_at: 2026-08-14T00:00:00Z
---
## Intent

Fixture exercising 2026-08-09-003 and tools/ws/validate.py:264 and ADR 0022.

## Decisions and revisit triggers

### Decision 1 — fixture

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | fixture referencing ADR-0023 |
| **Authorization** | fixture |
| **Confidence** | high |
| **Actor** | fixture |
| **Revisit trigger** | none |
| **Rationale** | fixture |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | 2026-08-11-018 | cites tests/test_ws_cli.py:40 |
<!-- Template comment: references/FAKE-NOT-REAL.md must be stripped -->
"""


class ExtractCitationsTests(unittest.TestCase):
    """Unit tests for the pure citation extractor."""

    def test_extracts_object_ids(self):
        found = _extract_citations("uses 2026-08-09-003 and 2026-08-11-018")
        self.assertIn("2026-08-09-003", found["objects"])
        self.assertIn("2026-08-11-018", found["objects"])

    def test_extracts_files_with_line(self):
        found = _extract_citations(
            "see tools/ws/validate.py:264 and tests/test_ws_cli.py:40"
        )
        self.assertIn("tools/ws/validate.py:264", found["files"])
        self.assertIn("tests/test_ws_cli.py:40", found["files"])

    def test_extracts_adrs_both_forms(self):
        found = _extract_citations("ADR 0022 and ADR-0023 and adr 0024")
        self.assertIn("ADR 0022", found["adrs"])
        self.assertIn("ADR-0023", found["adrs"])
        self.assertIn("ADR 0024", found["adrs"])


class CmdInputsTests(unittest.TestCase):
    """End-to-end tests for cmd_inputs against a temp workspace."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._tmpdir = Path(self._tmp.name)
        objects = self._tmpdir / ".work-studio" / "objects" / "2026" / "08"
        objects.mkdir(parents=True)
        self._obj_path = objects / "2026-08-14-900-fixture.md"
        self._obj_path.write_text(FIXTURE)
        self._old_cwd = os.getcwd()
        os.chdir(self._tmpdir)

    def tearDown(self):
        os.chdir(self._old_cwd)
        self._tmp.cleanup()

    def _run(self, obj_id):
        out_buf, err_buf = io.StringIO(), io.StringIO()
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            rc = cmd_inputs(argparse.Namespace(id=obj_id))
        return rc, out_buf.getvalue(), err_buf.getvalue()

    def test_reports_expected_citations(self):
        rc, out, _ = self._run("2026-08-14-900")
        self.assertEqual(rc, 0)
        self.assertIn("2026-08-09-003", out)
        self.assertIn("tools/ws/validate.py:264", out)
        self.assertIn("tests/test_ws_cli.py:40", out)
        self.assertIn("ADR 0022", out)
        self.assertIn("ADR-0023", out)

    def test_strips_html_comments(self):
        rc, out, _ = self._run("2026-08-14-900")
        self.assertEqual(rc, 0)
        self.assertNotIn("FAKE-NOT-REAL.md", out)

    def test_unknown_id_fails_cleanly(self):
        rc, _, err = self._run("2026-08-14-999")
        self.assertNotEqual(rc, 0)
        self.assertIn("not found", err)

    def test_is_read_only(self):
        before = self._obj_path.read_bytes()
        rc, _, _ = self._run("2026-08-14-900")
        self.assertEqual(rc, 0)
        self.assertEqual(self._obj_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
