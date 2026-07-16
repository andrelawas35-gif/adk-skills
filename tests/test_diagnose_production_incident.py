"""Contract tests for the diagnose-production-incident skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "diagnose-production-incident" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-3-diagnose-production-incident.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class DiagnoseProductionIncidentContract(unittest.TestCase):
    def test_core_skill_separates_containment_restoration_diagnosis_and_prevention(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "containment",
            "restoration",
            "ranked hypotheses",
            "one at a time",
            "affected path",
            "sanitized evidence",
            "Change Work Object",
            "does not stack speculative fixes",
            "external dependency",
            "manual-fallback",
            "unsupported",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_safe_intake_ranked_testing_recovery_dependency_and_follow_up(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5",
            "sanitized evidence", "containment", "restoration", "ranked hypothesis",
            "one at a time", "affected path", "external dependency", "waiting",
            "Change Work Object", "linked follow-up",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_generated_adapters_preserve_core_and_include_references(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR)], capture_output=True, text=True, cwd=str(ROOT)
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        core_body = namespaced_core_body(CORE)
        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-diagnose-production-incident"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())
                self.assertTrue((adapter_dir / "references" / "EVIDENCE-MODEL.md").is_file())


if __name__ == "__main__":
    unittest.main()
