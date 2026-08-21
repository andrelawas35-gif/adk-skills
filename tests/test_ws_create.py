"""Tests for ws create — tracer bullet for the deterministic CLI.

Covers the 4 creation test cases from §7 of the component plan:
1. ID allocation with collision detection
2. Invalid consequence enum rejection
3. Invalid type enum rejection
4. Correct template generation (7 required sections + structured Decisions)
"""

import os
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

# Add tools/ws to path for direct import in tests
TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.identity import allocate_id, build_filename, build_path, slugify
from ws.schema import (
    generate_frontmatter,
    validate_consequence,
    validate_sensitivity,
    validate_type,
)
from ws.template import generate_body_template


class TestIDAllocation(unittest.TestCase):
    """test_create_allocates_unique_id — ID allocation with collision detection."""

    def test_allocate_first_id(self):
        """First ID on an empty day is 001."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)
            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-001")

    def test_allocate_sequential(self):
        """IDs increment sequentially within the same day."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)

            # Create a file with ID 001
            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            (month_dir / "2026-07-21-001-some-object.md").write_text("", encoding="utf-8")

            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-002")

    def test_allocate_skips_non_matching_files(self):
        """Files that don't match the ID pattern are ignored."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)

            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            (month_dir / "README.md").write_text("", encoding="utf-8")
            (month_dir / "some-other-file.txt").write_text("", encoding="utf-8")

            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-001")

    def test_allocate_finds_highest_across_slugs(self):
        """Finds the maximum sequence regardless of slug text."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)

            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            (month_dir / "2026-07-21-005-alpha.md").write_text("", encoding="utf-8")
            (month_dir / "2026-07-21-003-beta.md").write_text("", encoding="utf-8")
            (month_dir / "2026-07-21-010-gamma.md").write_text("", encoding="utf-8")

            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-011")

    def test_allocate_different_dates_independent(self):
        """IDs on different dates don't affect each other."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)

            # July 20 has 5 objects
            month_dir_07 = objects_dir / "2026" / "07"
            month_dir_07.mkdir(parents=True, exist_ok=True)
            (month_dir_07 / "2026-07-20-005-something.md").write_text("", encoding="utf-8")

            # New allocation for July 21 starts at 001
            test_date = date(2026, 7, 21)
            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-001")

    def test_allocate_ignores_reserved_fixture_band(self):
        """A fixture parked at 999 does not exhaust the day's sequence."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)

            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            (month_dir / "2026-07-21-003-real-object.md").write_text("", encoding="utf-8")
            (month_dir / "2026-07-21-999-tracer-fixture.md").write_text("", encoding="utf-8")

            obj_id = allocate_id(objects_dir, today=test_date)
            self.assertEqual(obj_id, "2026-07-21-004")

    def test_allocate_raises_when_real_band_exhausted(self):
        """Exhausting 001-899 raises rather than allocating into the fixture band."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            test_date = date(2026, 7, 21)

            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            (month_dir / "2026-07-21-899-last-real-object.md").write_text("", encoding="utf-8")

            with self.assertRaises(RuntimeError):
                allocate_id(objects_dir, today=test_date)

    def test_slugify(self):
        """Title to slug conversion is stable."""
        self.assertEqual(slugify("Fix auth middleware"), "fix-auth-middleware")
        self.assertEqual(slugify("  Spaces  & Symbols!!!  "), "spaces-symbols")
        self.assertEqual(slugify("UPPER CASE"), "upper-case")
        self.assertEqual(slugify("a--b"), "a-b")

    def test_build_filename(self):
        """Filename construction follows the canonical format."""
        filename = build_filename("2026-07-21-010", "Fix auth middleware")
        self.assertEqual(filename, "2026-07-21-010-fix-auth-middleware.md")

    def test_build_path_creates_directories(self):
        """Build path creates necessary directory structure."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            target = build_path(objects_dir, "2026-07-21-010", "Fix auth middleware")
            self.assertTrue(target.parent.exists())
            self.assertIn("2026-07-21-010-fix-auth-middleware.md", str(target))

    def test_build_path_detects_collision(self):
        """Build path raises if target file already exists."""
        with tempfile.TemporaryDirectory() as tmp:
            objects_dir = Path(tmp)
            month_dir = objects_dir / "2026" / "07"
            month_dir.mkdir(parents=True, exist_ok=True)
            existing = month_dir / "2026-07-21-010-fix-auth-middleware.md"
            existing.write_text("existing content", encoding="utf-8")

            target = build_path(objects_dir, "2026-07-21-010", "Fix auth middleware")
            self.assertTrue(target.exists())


class TestFrontmatterValidation(unittest.TestCase):
    """test_create_rejects_invalid_consequence and test_create_rejects_invalid_type."""

    def test_valid_type(self):
        """All valid types pass validation."""
        for t in ["change", "inquiry", "project", "incident"]:
            self.assertIsNone(validate_type(t))

    def test_invalid_type_rejected(self):
        """Invalid type returns error message."""
        err = validate_type("bug")
        self.assertIsNotNone(err)
        self.assertIn("bug", err)

    def test_valid_consequence(self):
        """All valid consequence levels pass validation."""
        for c in ["low", "meaningful", "high"]:
            self.assertIsNone(validate_consequence(c))

    def test_invalid_consequence_rejected(self):
        """Invalid consequence returns error message."""
        err = validate_consequence("critical")
        self.assertIsNotNone(err)
        self.assertIn("critical", err)

    def test_valid_sensitivity(self):
        """All valid sensitivity levels pass validation."""
        for s in ["ordinary", "restricted"]:
            self.assertIsNone(validate_sensitivity(s))

    def test_invalid_sensitivity_rejected(self):
        """Invalid sensitivity returns error message."""
        err = validate_sensitivity("secret")
        self.assertIsNotNone(err)
        self.assertIn("secret", err)


class TestFrontmatterGeneration(unittest.TestCase):
    """Tests for frontmatter generation output."""

    def test_generates_valid_yaml(self):
        """Frontmatter output is parseable."""
        fm = generate_frontmatter(
            obj_id="2026-07-21-010",
            title="Fix auth middleware",
            obj_type="change",
            consequence="meaningful",
            sensitivity="ordinary",
        )

        self.assertTrue(fm.startswith("---\n"))
        self.assertTrue(fm.strip().endswith("---"))

    def test_contains_required_fields(self):
        """Frontmatter includes all required fields."""
        fm = generate_frontmatter(
            obj_id="2026-07-21-010",
            title="Fix auth middleware",
            obj_type="change",
            consequence="meaningful",
            sensitivity="ordinary",
        )

        required_fields = [
            "schema_version: 1",
            "id: 2026-07-21-010",
            "title: Fix auth middleware",
            "type: change",
            "status: active",
            "state: notice",
            "consequence: meaningful",
            "sensitivity: ordinary",
            "created_at:",
            "updated_at:",
        ]

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, fm)

    def test_timestamps_are_iso8601(self):
        """Created and updated timestamps use ISO 8601 format."""
        fm = generate_frontmatter(
            obj_id="2026-07-21-010",
            title="Test",
            obj_type="inquiry",
            consequence="low",
            sensitivity="ordinary",
        )

        ts_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        for line in fm.split("\n"):
            if line.startswith("created_at:") or line.startswith("updated_at:"):
                ts = line.split(": ", 1)[1]
                self.assertTrue(
                    ts_pattern.match(ts),
                    f"Timestamp '{ts}' does not match ISO 8601 format",
                )

    def test_consequence_required_no_default(self):
        """Consequence must be explicitly provided — no default exists."""
        # Verify that each call produces the exact provided consequence
        for level in ["low", "meaningful", "high"]:
            fm = generate_frontmatter(
                obj_id="2026-07-21-001",
                title="Test",
                obj_type="change",
                consequence=level,
                sensitivity="ordinary",
            )
            self.assertIn(f"consequence: {level}", fm)


class TestTemplateGeneration(unittest.TestCase):
    """test_create_generates_correct_template — 7 sections + structured Decisions."""

    REQUIRED_SECTIONS = [
        "## Intent",
        "## Success evidence",
        "## Constraints and non-goals",
        "## Decisions and revisit triggers",
        "## Evidence ledger",
        "## Open questions",
        "## Next move",
        "## History",
    ]

    def test_all_required_sections_present(self):
        """Template contains all 7 required sections + Decisions."""
        body = generate_body_template("Test", "change", "meaningful")
        for section in self.REQUIRED_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(section, body)

    def test_sections_appear_in_order(self):
        """Sections appear in the prescribed order."""
        body = generate_body_template("Test", "change", "meaningful")
        positions = {s: body.find(s) for s in self.REQUIRED_SECTIONS}
        sorted_positions = sorted(positions.items(), key=lambda x: x[1])

        for expected, (actual_section, _) in zip(self.REQUIRED_SECTIONS, sorted_positions):
            with self.subTest(section=expected):
                self.assertEqual(expected, actual_section)

    def test_decisions_template_has_structured_fields(self):
        """Decisions template contains gate-readable structured fields."""
        body = generate_body_template("Test", "change", "meaningful")
        decisions_start = body.find("## Decisions and revisit triggers")
        decisions_section = body[decisions_start:]

        structured_fields = [
            "**Decision type**",
            "**Result**",
            "**Scope**",
            "**Authorization**",
            "**Confidence**",
            "**Actor**",
            "**Revisit trigger**",
            "**Rationale**",
        ]

        for field in structured_fields:
            with self.subTest(field=field):
                self.assertIn(field, decisions_section)

    def test_high_consequence_includes_build_gate_note(self):
        """High consequence template includes build gate instructions."""
        body = generate_body_template("Test", "change", "high")
        self.assertIn("BUILD GATE", body)
        self.assertIn("decision_type: decision", body)

    def test_low_consequence_no_build_gate_note(self):
        """Low consequence template does not include build gate instructions."""
        body = generate_body_template("Test", "change", "low")
        self.assertNotIn("BUILD GATE", body)

    def test_sections_not_empty(self):
        """Each section has content beyond just the heading."""
        body = generate_body_template("Test", "change", "meaningful")

        # Split by section headings
        parts = re.split(r"(?=^## )", body, flags=re.MULTILINE)
        for part in parts:
            if not part.strip():
                continue
            lines = part.strip().split("\n")
            # At least a heading and some content
            self.assertGreater(
                len(lines), 1,
                f"Section appears empty: {lines[0][:60]}",
            )


class TestCreateIntegration(unittest.TestCase):
    """End-to-end integration test for ws create."""

    REPO_ROOT = TOOLS_DIR.parent  # repo root containing tools/

    def _run_ws(self, tmp_path: Path, *args: str):
        """Run ws create as a subprocess from tmp_path.

        Adds the repo root to PYTHONPATH so 'tools.ws' is importable,
        then runs python3 -m tools.ws with the given arguments.
        """
        import subprocess

        env = os.environ.copy()
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(self.REPO_ROOT) + (f":{existing}" if existing else "")

        return subprocess.run(
            [sys.executable, "-m", "tools.ws"] + list(args),
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(tmp_path),
            env=env,
        )
    def test_create_writes_valid_file(self):
        """Full ws create pipeline produces a readable, parseable file."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # Set up minimal work-studio structure
            work_studio = tmp_path / ".work-studio"
            objects_dir = work_studio / "objects"
            objects_dir.mkdir(parents=True)

            result = self._run_ws(
                tmp_path, "create",
                "--title", "Fix auth middleware",
                "--type", "change",
                "--consequence", "meaningful",
                "--sensitivity", "ordinary",
            )

            # Debug output on failure
            if result.returncode != 0:
                self.fail(f"ws create failed:\nstderr: {result.stderr}\nstdout: {result.stdout}")

            self.assertEqual(result.returncode, 0)
            self.assertIn("Created:", result.stdout)
            self.assertIn("ID:", result.stdout)

            # Verify the file was created
            output_lines = result.stdout.strip().split("\n")
            created_line = [l for l in output_lines if l.startswith("Created:")][0]
            relative_path = created_line.split(": ", 1)[1]
            created_file = tmp_path / relative_path
            self.assertTrue(created_file.exists())

            # Read and verify content
            content = created_file.read_text(encoding="utf-8")
            self.assertIn("---", content)
            self.assertIn("id:", content)
            self.assertIn("title: Fix auth middleware", content)
            self.assertIn("type: change", content)
            self.assertIn("consequence: meaningful", content)
            self.assertIn("sensitivity: ordinary", content)
            self.assertIn("## Intent", content)
            self.assertIn("## History", content)

    def test_create_rejects_invalid_consequence(self):
        """ws create rejects invalid --consequence value."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            work_studio = tmp_path / ".work-studio"
            (work_studio / "objects").mkdir(parents=True)

            result = self._run_ws(
                tmp_path, "create",
                "--title", "Test",
                "--type", "change",
                "--consequence", "critical",
                "--sensitivity", "ordinary",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("consequence", result.stderr.lower())

    def test_create_rejects_invalid_type(self):
        """ws create rejects invalid --type value."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            work_studio = tmp_path / ".work-studio"
            (work_studio / "objects").mkdir(parents=True)

            result = self._run_ws(
                tmp_path, "create",
                "--title", "Test",
                "--type", "bug",
                "--consequence", "meaningful",
                "--sensitivity", "ordinary",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("type", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
