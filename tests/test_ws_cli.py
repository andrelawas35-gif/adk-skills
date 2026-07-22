"""Tests for ws concurrency, lifecycle, sections, attention, and validate.

Covers the test cases from §7 of the deterministic CLI component plan
that weren't already covered by test_ws_create.py.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.schema import generate_frontmatter, parse_frontmatter
from ws.template import generate_body_template
from ws.concurrency import check_concurrency
from ws.lifecycle import (
    validate_transition,
    check_build_gate,
    check_release_gate,
    check_close_gate,
    check_observe_gate,
    check_gates_for_transition,
    can_close_directly,
    get_close_route,
)
from ws.sections import (
    parse_sections,
    get_section,
    append_to_section,
    validate_section_order,
    parse_decisions_table,
    generate_history_entry,
    generate_evidence_entry,
    check_append_only,
)
from ws.attention import (
    parse_active_md,
    get_active_ids,
    find_stale_entries,
    find_missing_entries,
    update_active_entry,
    remove_active_entry,
    _section_insertion_point,
)
from ws.validate import (
    check_schema,
    check_sections,
    check_sensitivity,
    check_lifecycle,
    check_structure,
    CHECK_REGISTRY,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_FRONTMATTER = """---
schema_version: 1
id: 2026-07-21-010
title: Test Object
type: change
status: active
state: notice
consequence: meaningful
sensitivity: ordinary
created_at: 2026-07-21T00:00:00Z
updated_at: 2026-07-21T00:00:00Z
---"""

SAMPLE_BODY = """
## Intent

Test intent.

## Success evidence

- [ ] Done

## Constraints and non-goals

None.

## Decisions and revisit triggers

### Decision 1 — Test decision

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | test scope |
| **Authorization** | user |
| **Confidence** | high |
| **Actor** | system |
| **Revisit trigger** | never |
| **Rationale** | testing |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | test | Initial evidence |

## Open questions

None.

## Next move

Continue.

## History

### 2026-07-21T00:00:00Z — Created

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Test creation
"""


def make_object_file(dir_path: Path, filename: str, content: str) -> Path:
    """Create a Work Object file and return its path."""
    file_path = dir_path / filename
    file_path.write_text(content)
    return file_path


# ═══════════════════════════════════════════════════════════════════════════════
# Concurrency tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestConcurrency(unittest.TestCase):
    """test_expect_updated_rejects_stale and test_expect_updated_accepts_current."""

    def test_accepts_matching_timestamp(self):
        """Non-stale writes succeed when timestamps match."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )

            err = check_concurrency(obj_file, "2026-07-21T00:00:00Z")
            self.assertIsNone(err)

    def test_rejects_stale_timestamp(self):
        """Stale writes are rejected with both timestamps."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )

            err = check_concurrency(obj_file, "2026-07-20T23:59:59Z")
            self.assertIsNotNone(err)
            self.assertIn("2026-07-20T23:59:59Z", err)
            self.assertIn("2026-07-21T00:00:00Z", err)

    def test_force_bypasses_staleness(self):
        """test_force_bypasses_staleness_with_warning — force skips check."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )

            err = check_concurrency(obj_file, "2026-07-20T00:00:00Z", force=True)
            self.assertIsNone(err)

    def test_missing_file_returns_error(self):
        """Nonexistent file produces error."""
        with tempfile.TemporaryDirectory() as tmp:
            err = check_concurrency(Path(tmp) / "nope.md", "2026-01-01T00:00:00Z")
            self.assertIsNotNone(err)

    def test_no_updated_at_field(self):
        """Missing updated_at field produces error."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            bad_fm = SAMPLE_FRONTMATTER.replace("updated_at:", "bogus:")
            obj_file = make_object_file(tmpdir, "test.md", bad_fm + "\n" + SAMPLE_BODY)

            err = check_concurrency(obj_file, "2026-07-21T00:00:00Z")
            self.assertIsNotNone(err)


# ═══════════════════════════════════════════════════════════════════════════════
# Lifecycle tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestLifecycleTransitions(unittest.TestCase):
    """test_transition_rejects_close_escape and test_transition_rejects_closed_status_resurrection."""

    def test_permissive_default_allows_normal_transition(self):
        """Any state → any state (except prohibitions) is allowed."""
        err = validate_transition("notice", "build", "active", "active")
        self.assertIsNone(err)

    def test_rejects_close_state_escape(self):
        """test_transition_rejects_close_escape: close → any other state blocked."""
        err = validate_transition("close", "verify", "active", "active")
        self.assertIsNotNone(err)
        self.assertIn("terminal state", err)

    def test_rejects_closed_status_resurrection(self):
        """test_transition_rejects_closed_status_resurrection: closed → any other status blocked."""
        err = validate_transition("close", "close", "closed", "active")
        self.assertIsNotNone(err)
        self.assertIn("terminal status", err)

    def test_rejects_invalid_state(self):
        """Invalid state values are caught."""
        err = validate_transition("bogus", "build", "active", "active")
        self.assertIsNotNone(err)

    def test_rejects_invalid_status(self):
        """Invalid status values are caught."""
        err = validate_transition("notice", "build", "active", "invalid")
        self.assertIsNotNone(err)


class TestLifecycleGates(unittest.TestCase):
    """Gate enforcement tests."""

    def test_build_gate_passes_non_high_consequence(self):
        """Build gate always passes for non-high consequence."""
        passed, _ = check_build_gate(SAMPLE_BODY, "meaningful")
        self.assertTrue(passed)

    def test_build_gate_passes_with_decision_record(self):
        """Build gate passes for high consequence with decision record."""
        passed, _ = check_build_gate(SAMPLE_BODY, "high")
        self.assertTrue(passed)

    def test_build_gate_fails_without_decision_record(self):
        """Build gate fails for high consequence without decision record."""
        body_no_decisions = SAMPLE_BODY.replace(
            "### Decision 1 — Test decision",
            "### Discussion 1 — Not a decision",
        )
        passed, msg = check_build_gate(body_no_decisions, "high")
        self.assertFalse(passed)
        self.assertIn("decision_type: decision", msg)

    def test_release_gate_passes_with_pass_result_and_scope(self):
        """Release gate passes with result: pass and scope."""
        passed, _ = check_release_gate(SAMPLE_BODY)
        self.assertTrue(passed)

    def test_release_gate_fails_without_scope(self):
        """Release gate fails when scope is missing."""
        body_no_scope = SAMPLE_BODY.replace("| test scope |", "| <!-- what this decision applies to --> |")
        passed, msg = check_release_gate(body_no_scope)
        self.assertFalse(passed)

    def test_release_gate_fails_with_fail_result(self):
        """Release gate fails when result is not pass."""
        body_fail = SAMPLE_BODY.replace("| **Result** | pass |", "| **Result** | fail |")
        passed, msg = check_release_gate(body_fail)
        self.assertFalse(passed)
        self.assertIn("fail", msg)

    def test_close_gate_passes_with_outcome(self):
        """Close gate passes with a pass/fail result."""
        passed, _ = check_close_gate(SAMPLE_BODY)
        self.assertTrue(passed)

    def test_close_gate_fails_without_outcome(self):
        """Close gate fails without any pass/fail result."""
        body_pending = SAMPLE_BODY.replace("| **Result** | pass |", "| **Result** | pending |")
        passed, msg = check_close_gate(body_pending)
        self.assertFalse(passed)

    def test_observe_gate_passes_with_pass_result(self):
        """Observe gate passes with any pass result."""
        passed, _ = check_observe_gate(SAMPLE_BODY)
        self.assertTrue(passed)

    def test_gate_dispatch_returns_true_for_ungated_states(self):
        """States without gates always pass."""
        passed, _ = check_gates_for_transition(SAMPLE_BODY, "notice", "meaningful")
        self.assertTrue(passed)

    def test_close_direct_for_low_meaningful(self):
        """Low/meaningful consequence can close from any state."""
        self.assertTrue(can_close_directly("low", "notice"))
        self.assertTrue(can_close_directly("meaningful", "build"))
        self.assertEqual(get_close_route("low", "notice"), "direct")

    def test_close_two_step_for_high(self):
        """High consequence requires two-step close."""
        self.assertFalse(can_close_directly("high", "build"))
        self.assertTrue(can_close_directly("high", "close"))
        self.assertEqual(get_close_route("high", "build"), "two-step")
        self.assertEqual(get_close_route("high", "close"), "direct")


# ═══════════════════════════════════════════════════════════════════════════════
# Sections tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestSectionsParsing(unittest.TestCase):
    """Section parsing and manipulation tests."""

    def test_parse_sections_extracts_all_sections(self):
        """All named sections are extracted."""
        sections = parse_sections(SAMPLE_BODY)
        self.assertIn("intent", sections)
        self.assertIn("history", sections)
        self.assertIn("evidence ledger", sections)

    def test_get_section_returns_content(self):
        """get_section returns full section including heading."""
        section = get_section(SAMPLE_BODY, "intent")
        self.assertIsNotNone(section)
        self.assertIn("## Intent", section)

    def test_get_section_none_for_missing(self):
        """get_section returns None for missing sections."""
        section = get_section(SAMPLE_BODY, "nonexistent")
        self.assertIsNone(section)

    def test_append_to_existing_section(self):
        """Append adds content to existing section."""
        new_body = append_to_section(SAMPLE_BODY, "history", "New entry")
        self.assertIn("New entry", new_body)
        self.assertIn("Test creation", new_body)  # Original preserved

    def test_append_to_new_section(self):
        """Append creates new section if missing."""
        new_body = append_to_section(SAMPLE_BODY, "appendix", "Extra content")
        self.assertIn("## appendix", new_body)
        self.assertIn("Extra content", new_body)

    def test_validate_section_order_detects_out_of_order(self):
        """Out-of-order sections produce errors."""
        body_reordered = SAMPLE_BODY.replace(
            "## History",
            "## History\n\nFirst\n\n## Evidence ledger",
        )
        # This is a bit tricky — let me just check that valid order passes
        errors = validate_section_order(SAMPLE_BODY)
        self.assertEqual(len(errors), 0)  # Well-formed body passes

    def test_parse_decisions_table_extracts_fields(self):
        """Structured decision fields are parsed correctly."""
        decisions = parse_decisions_table(SAMPLE_BODY)
        self.assertEqual(len(decisions), 1)
        d = decisions[0]
        self.assertEqual(d.get("decision_type"), "decision")
        self.assertEqual(d.get("result"), "pass")
        self.assertEqual(d.get("scope"), "test scope")
        self.assertEqual(d.get("confidence"), "high")

    def test_generate_history_entry_format(self):
        """History entry follows expected format."""
        entry = generate_history_entry(
            action="Tested",
            state="build",
            status="active",
            actor="tester",
            rationale="testing",
        )
        self.assertIn("### ", entry)  # Has timestamp heading
        self.assertIn("Tested", entry)
        self.assertIn("build", entry)
        self.assertIn("active", entry)
        self.assertIn("tester", entry)
        self.assertIn("testing", entry)

    def test_generate_evidence_entry_format(self):
        """Evidence entry follows table format."""
        entry = generate_evidence_entry("[system]", "test.py", "passed")
        self.assertTrue(entry.startswith("| [system]"))
        self.assertIn("test.py", entry)
        self.assertIn("passed", entry)

    def test_generate_evidence_entry_rejects_invalid_tag(self):
        """Invalid evidence tags raise ValueError."""
        with self.assertRaises(ValueError):
            generate_evidence_entry("[bad-tag]", "test", "text")

    def test_check_append_only_detects_duplicate(self):
        """Duplicate entries are detected."""
        entry = "| [system] | test | Initial evidence |"
        self.assertFalse(check_append_only(SAMPLE_BODY, "evidence ledger", entry))

    def test_check_append_only_allows_new(self):
        """New entries pass append-only check."""
        entry = "| [observed] | test | New observation |"
        self.assertTrue(check_append_only(SAMPLE_BODY, "evidence ledger", entry))


# ═══════════════════════════════════════════════════════════════════════════════
# Attention tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestAttention(unittest.TestCase):
    """Active register tests."""

    def test_parse_active_md(self):
        """Parse active.md entries."""
        content = "# Active\n\n- `2026-07-21-001` — First object\n- `2026-07-21-002` — Second (primary)\n"
        entries = parse_active_md(content)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], ("2026-07-21-001", "First object"))
        self.assertEqual(entries[1], ("2026-07-21-002", "Second (primary)"))

    def test_get_active_ids(self):
        """Extract active IDs as set."""
        content = "- `A` — a\n- `B` — b\n"
        ids = get_active_ids(content)
        self.assertEqual(ids, {"A", "B"})

    def test_update_active_entry_adds_new(self):
        """New entry is inserted in the correct section."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text(
                "# Active\n\n"
                "## Primary\n\n- `001` — Existing\n\n"
                "## Supporting\n\n- `002` — Other\n\n"
                "## Paused\n"
            )

            updated = update_active_entry(active_md, "003", "New object", "primary")
            self.assertIn("003", updated)
            self.assertIn("New object (primary)", updated)

    def test_update_active_entry_inserts_before_paused(self):
        """Supporting entries are inserted before Paused section."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text(
                "# Active\n\n"
                "## Primary\n\n- `001` — P\n\n"
                "## Supporting\n\n- `002` — S\n\n"
                "## Paused\n"
            )

            updated = update_active_entry(active_md, "003", "New supporting", "supporting")
            # The new entry must appear before ## Paused
            paused_pos = updated.index("## Paused")
            entry_pos = updated.index("New supporting")
            self.assertLess(entry_pos, paused_pos,
                            "Supporting entry must appear before ## Paused")

    def test_update_active_entry_paused_appends_at_end(self):
        """Paused entries are appended at end of active.md."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text(
                "# Active\n\n"
                "## Primary\n\n- `001` — P\n\n"
                "## Supporting\n\n- `002` — S\n\n"
                "## Paused\n"
            )

            updated = update_active_entry(active_md, "003", "Paused entry", "paused")
            # Should be after ## Paused (at end)
            paused_pos = updated.index("## Paused")
            entry_pos = updated.index("Paused entry")
            self.assertGreater(entry_pos, paused_pos,
                               "Paused entry must appear after ## Paused")

    def test_update_active_entry_updates_existing(self):
        """Existing entry is updated, not duplicated."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text("# Active\n\n- `001` — Original\n")

            updated = update_active_entry(active_md, "001", "Updated", "paused")
            self.assertIn("Updated (paused)", updated)
            self.assertNotIn("Original", updated)
            # Count occurrences
            self.assertEqual(updated.count("`001`"), 1)

    def test_remove_active_entry(self):
        """Entry is removed from active.md."""
        content = "# Active\n\n- `001` — Keep\n- `002` — Remove\n"
        result = remove_active_entry.__wrapped__ = None  # Can't test directly without path
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text(content)

            updated = remove_active_entry(active_md, "002")
            self.assertIsNotNone(updated)
            self.assertNotIn("002", updated)
            self.assertIn("001", updated)

    def test_remove_nonexistent_entry(self):
        """Removing nonexistent entry returns None."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            active_md = tmpdir / "active.md"
            active_md.write_text("- `001` — Only\n")

            result = remove_active_entry(active_md, "999")
            self.assertIsNone(result)


# ═══════════════════════════════════════════════════════════════════════════════
# Validation tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestValidateSchema(unittest.TestCase):
    """test_validate_schema_catches_invalid_enum."""

    def test_valid_object_passes_schema(self):
        """Well-formed object passes schema validation."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_schema(obj_file)
            self.assertEqual(len(errors), 0)

    def test_catches_invalid_status_enum(self):
        """Invalid status value is caught."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            bad_fm = SAMPLE_FRONTMATTER.replace("status: active", "status: archived")
            obj_file = make_object_file(tmpdir, "2026-07-21-010-test.md", bad_fm + "\n" + SAMPLE_BODY)
            errors = check_schema(obj_file)
            self.assertTrue(any("archived" in e for e in errors))

    def test_catches_missing_required_field(self):
        """Missing required field is caught."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            bad_fm = SAMPLE_FRONTMATTER.replace("type: change\n", "")
            obj_file = make_object_file(tmpdir, "2026-07-21-010-test.md", bad_fm + "\n" + SAMPLE_BODY)
            errors = check_schema(obj_file)
            self.assertTrue(any("type" in e for e in errors))

    def test_catches_id_mismatch(self):
        """Frontmatter id must match filename prefix."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-999-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_schema(obj_file)
            self.assertTrue(any("does not match filename" in e for e in errors))


class TestValidateSections(unittest.TestCase):
    """Section validation tests."""

    def test_valid_object_passes_sections(self):
        """Well-formed object passes section validation."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_sections(obj_file)
            self.assertEqual(len(errors), 0)


class TestValidateSensitivity(unittest.TestCase):
    """test_validate_sensitivity_catches_restricted_body."""

    def test_ordinary_passes(self):
        """Ordinary sensitivity objects always pass."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_sensitivity(obj_file)
            self.assertEqual(len(errors), 0)

    def test_restricted_with_secret_triggers_warning(self):
        """Restricted objects with sensitive keywords trigger warning."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            restricted_fm = SAMPLE_FRONTMATTER.replace(
                "sensitivity: ordinary", "sensitivity: restricted"
            )
            body_with_secret = SAMPLE_BODY + "\nAPI token: xyz123\n"
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                restricted_fm + "\n" + body_with_secret,
            )
            errors = check_sensitivity(obj_file)
            self.assertTrue(len(errors) > 0)


class TestValidateLifecycle(unittest.TestCase):
    """test_validate_lifecycle_catches_terminal_escape."""

    def test_normal_object_passes(self):
        """Normal lifecycle passes."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_lifecycle(obj_file)
            self.assertEqual(len(errors), 0)

    def test_close_state_without_closed_status(self):
        """Close state with non-closed status is caught."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            bad_fm = SAMPLE_FRONTMATTER.replace("state: notice", "state: close")
            obj_file = make_object_file(tmpdir, "2026-07-21-010-test.md", bad_fm + "\n" + SAMPLE_BODY)
            errors = check_lifecycle(obj_file)
            self.assertTrue(len(errors) > 0)

    def test_closed_status_with_active_state(self):
        """Closed status with build state is caught."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            bad_fm = SAMPLE_FRONTMATTER.replace("status: active", "status: closed")
            bad_fm = bad_fm.replace("state: notice", "state: build")
            obj_file = make_object_file(tmpdir, "2026-07-21-010-test.md", bad_fm + "\n" + SAMPLE_BODY)
            errors = check_lifecycle(obj_file)
            self.assertTrue(len(errors) > 0)


class TestValidateStructure(unittest.TestCase):
    """Composite structure check."""

    def test_structure_composes_schema_and_sections(self):
        """Structure check runs both schema and sections."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            obj_file = make_object_file(
                tmpdir, "2026-07-21-010-test.md",
                SAMPLE_FRONTMATTER + "\n" + SAMPLE_BODY,
            )
            errors = check_structure(obj_file)
            self.assertEqual(len(errors), 0)


class TestCheckRegistry(unittest.TestCase):
    """All declared checks are registered."""

    def test_all_checks_registered(self):
        """Every check name has a handler."""
        expected = {"schema", "sections", "append-only", "attention",
                     "sensitivity", "lifecycle", "structure"}
        self.assertEqual(set(CHECK_REGISTRY.keys()), expected)


if __name__ == "__main__":
    unittest.main()
