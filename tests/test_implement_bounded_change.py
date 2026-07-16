"""Contract tests for the accepted bounded-change implementation skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "implement-bounded-change" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-2-implement-bounded-change.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class ImplementBoundedChangeContract(unittest.TestCase):
    def test_core_skill_implements_only_an_accepted_tracer_bullet(self):
        text = CORE.read_text()

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "accepted tracer bullet",
            "repository inspection",
            "unrelated working-tree changes",
            "continuous verification",
            "material new decision",
            "authority boundary",
            "deviation",
            "does not deploy",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_preservation_verification_deviation_and_degradation(self):
        text = FIXTURE.read_text()

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
            "repository inspection", "unrelated working-tree changes",
            "continuous verification", "deviation", "manual-fallback",
            "unsupported", "does not deploy",
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
                adapter_dir = ROOT / "adapters" / platform / "skills" / "alawas-implement-bounded-change"
                self.assertIn(core_body, (adapter_dir / "SKILL.md").read_text())
                self.assertTrue((adapter_dir / "references" / "SHARED-PROTOCOL.md").is_file())
                self.assertTrue((adapter_dir / "references" / "CAPABILITY-DEGRADATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
