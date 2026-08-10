"""Contract tests for the govern-scorecards skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "governance-govern-scorecards" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-4-govern-scorecards.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class GovernScorecardsContract(unittest.TestCase):
    def test_core_preserves_evidence_boundaries_and_versioning(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "completion",
            "decision quality",
            "reality contact",
            "loop burden",
            "routing quality",
            "recovery quality",
            "personal fit",
            "artifact value",
            "novelty yield",
            "composite score",
            "message counts",
            "identity",
            "insufficient",
            "Workflow Candidate",
            "maintain-working-method",
            "explicit human confirmation",
            "supersedes",
            "user-approved summary",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_required_scorecard_behaviors(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1",
            "Scenario 2",
            "Scenario 3",
            "Scenario 4",
            "conflict",
            "composite score",
            "unconfirmed Workflow Candidate",
            "maintain-working-method",
            "supersedes",
            "message counts",
            "identity",
            "personal-archive",
            "novelty churn",
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
                adapter_dir = ROOT / "adapters" / platform / "skills" / f"alawas-{CORE.parent.name}"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())
                self.assertTrue((adapter_dir / "references" / "EVIDENCE-MODEL.md").is_file())


if __name__ == "__main__":
    unittest.main()
