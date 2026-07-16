"""Contract tests for the maintain-working-method skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "maintain-working-method" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-4-maintain-working-method.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class MaintainWorkingMethodContract(unittest.TestCase):
    def test_core_preserves_candidate_evidence_and_requires_scoped_promotion(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "immutable identity",
            "proposed rule",
            "scope",
            "origin references",
            "append-only evidence",
            "bounded test references",
            "contrary-evidence review",
            "supported",
            "contradicted",
            "insufficient",
            "separate, linked, versioned Working Method",
            "explicit human confirmation",
            "supersedes",
            "Evidence Bridge",
            "manual-fallback",
            "unsupported",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_candidate_lifecycle_and_evidence_boundaries(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1",
            "Scenario 2",
            "Scenario 3",
            "Scenario 4",
            "Scenario 5",
            "Scenario 6",
            "outcome-review",
            "supporting evidence",
            "contrary evidence",
            "none observed within scope",
            "supported",
            "contradicted",
            "insufficient",
            "separate Working Method",
            "explicit human confirmation",
            "supersedes",
            "approved Evidence Bridge",
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
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-maintain-working-method"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())
                self.assertTrue((adapter_dir / "references" / "EVIDENCE-MODEL.md").is_file())


if __name__ == "__main__":
    unittest.main()
