"""Contract tests for the bounded tracer-bullet design skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "design-design-tracer-bullet" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-2-design-tracer-bullet.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class DesignTracerBulletContract(unittest.TestCase):
    def test_core_skill_records_an_agreed_bounded_design_without_implementation(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "Design-state Work Object",
            "Recommend before asking one question.",
            "riskiest assumption",
            "authorization",
            "failure behavior",
            "observability",
            "rollback",
            "does not implement",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_recommendation_recording_risk_rollback_and_adjacent_possibility(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
            "recommendation", "one question", "accepted design",
            "riskiest assumption", "rollback", "observability",
            "Adjacent Possibility Pass", "option space", "does not implement",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_generated_adapters_preserve_core_and_include_references(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR)],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        core_body = namespaced_core_body(CORE)
        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-design-tracer-bullet"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "SHARED-PROTOCOL.md").is_file())
                self.assertTrue((adapter_dir / "references" / "CAPABILITY-DEGRADATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
