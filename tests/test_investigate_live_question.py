"""Contract tests for the live-question investigation skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "investigate-live-question" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-3-investigate-live-question.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class InvestigateLiveQuestionContract(unittest.TestCase):
    def test_core_skill_frames_evidence_and_reality_contact_without_archive_access(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "activated Inquiry",
            "primary-source",
            "evidence from inference",
            "missing evidence",
            "reality contact",
            "Recommend before asking one decision-bearing question.",
            "answered", "reframed", "prototype-ready", "unresolved",
            "Evidence Bridge",
            "must not scan, read, or mutate the Personal Institution archive",
            "durable transition",
            "prototype-ready:",
            "creates and links",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_primary_sources_reality_contact_contradiction_unresolved_and_bridge_gate(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5",
            "primary-source", "reality contact", "contradiction", "unresolved",
            "Approved Evidence Bridge", "Personal Institution archive",
            "Outcome persistence", "Work Object is never left unchanged",
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
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-investigate-live-question"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "EVIDENCE-MODEL.md").is_file())
                self.assertTrue((adapter_dir / "references" / "SHARED-PROTOCOL.md").is_file())


if __name__ == "__main__":
    unittest.main()
