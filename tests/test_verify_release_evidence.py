"""Contract tests for the release-evidence verification skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "engineering-verify-release-evidence" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-2-verify-release-evidence.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class VerifyReleaseEvidenceContract(unittest.TestCase):
    def test_core_skill_reports_proportionate_evidence_without_releasing(self):
        text = CORE.read_text(encoding="utf-8")

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "acceptance",
            "failure and recovery",
            "degraded dependencies",
            "privacy and security",
            "evidence gap",
            "consequence",
            "does not deploy or release",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_success_gaps_degradation_duplicates_and_no_release_claim(self):
        text = FIXTURE.read_text(encoding="utf-8")

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
            "successful verification", "missing evidence", "degraded dependency",
            "retry", "duplicate", "privacy", "security", "does not deploy or release",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_generated_adapters_preserve_core_and_include_references(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR)],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        core_body = namespaced_core_body(CORE)
        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter_dir = ROOT / "adapters" / platform / "skills" / f"alawas-{CORE.parent.name}"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text(encoding="utf-8"))
                self.assertTrue((adapter_dir / "references" / "CAPABILITY-DEGRADATION.md").is_file())
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())


if __name__ == "__main__":
    unittest.main()
