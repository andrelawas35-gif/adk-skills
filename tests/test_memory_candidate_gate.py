"""Contract test for the PKM Memory Candidate admission gate."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "thinking-turn-signal-into-work" / "SKILL.md"
PLATFORMS = ("codex", "claude-code", "github-copilot")


class MemoryCandidateGateContract(unittest.TestCase):
    def test_memory_candidates_require_a_user_approved_redacted_summary(self):
        text = " ".join(CORE.read_text(encoding="utf-8").split())

        for required_clause in (
            "Memory Candidate gate",
            "user-approved summary that is minimum-necessary and redacted",
            "must not enter a Work Object",
            "personal-archive content",
            "Explicit activation does not bypass this gate",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_generated_adapters_preserve_the_gate(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter = ROOT / "adapters" / platform / "skills" / f"alawas-{CORE.parent.name}" / "SKILL.md"
                self.assertIn("Memory Candidate gate", adapter.read_text(encoding="utf-8"))

