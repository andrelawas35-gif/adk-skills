"""Contract tests for the design implementation verification skill."""

import subprocess
import sys
import unittest
from pathlib import Path

from adapter_helpers import namespaced_core_body


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "design-verify-design-implementation" / "SKILL.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class VerifyDesignImplementationContract(unittest.TestCase):
    def test_core_skill_checks_confirmed_changes_with_honest_deferred_dimensions(self):
        text = CORE.read_text(encoding="utf-8")

        for required_clause in (
            "## Governing principle",
            "## Boundaries and non-goals",
            "## Required capabilities",
            "structural",
            "visual",
            "browser rendering",
            "confirmed proposal",
            "[system:verification-report]",
            "checked",
            "deferred",
            "manual-fallback",
            "does not fix",
            "## Final self-check",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text, f"Missing: {required_clause}")

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
                self.assertTrue((adapter_dir / "references" / "CONSEQUENCE-AUTHORITY.md").is_file())


if __name__ == "__main__":
    unittest.main()
