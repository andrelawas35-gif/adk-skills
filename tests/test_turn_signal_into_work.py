"""Contract tests for the Slice 2 signal-capture skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "thinking-turn-signal-into-work" / "SKILL.md"
FIXTURE = ROOT / "fixtures" / "slice-2-turn-signal-into-work.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class TurnSignalIntoWorkContract(unittest.TestCase):
    def test_core_skill_defines_activation_and_authority_boundaries(self):
        text = CORE.read_text(encoding="utf-8")

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "explicit activation",
            "discard", "remember", "incubate", "activate",
            "user-approved summary",
            "must not scan, read, or mutate",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_fixture_covers_capture_activation_and_degradation(self):
        text = FIXTURE.read_text(encoding="utf-8")

        for required_clause in (
            "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
            "user's language", "explicit activation", "user-approved",
            "manual-fallback", "unsupported",
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
                self.assertTrue((adapter_dir / "references" / "EVIDENCE-MODEL.md").is_file())


if __name__ == "__main__":
    unittest.main()
