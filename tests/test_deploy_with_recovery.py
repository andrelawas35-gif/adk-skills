"""Contract tests for the deploy-with-recovery skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "deploy-with-recovery" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-3-deploy-with-recovery.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class DeployWithRecoveryContract(unittest.TestCase):
    def test_core_skill_requires_authorized_incremental_deployment_and_observation(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "explicit deployment authority",
            "platform runbook",
            "readiness",
            "migration",
            "budget",
            "rollback",
            "incremental",
            "sanitized",
            "post-deployment reality checks",
            "observe",
            "does not claim closure",
            "manual-fallback",
            "unsupported",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_success_missing_readiness_rollback_sanitization_and_degradation(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
            "successful incremental deployment", "missing readiness",
            "failed verification", "rollback", "sanitized evidence",
            "manual-fallback", "unsupported", "observe", "does not claim closure",
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
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-deploy-with-recovery"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())
                self.assertTrue((adapter_dir / "references" / "CAPABILITY-DEGRADATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
