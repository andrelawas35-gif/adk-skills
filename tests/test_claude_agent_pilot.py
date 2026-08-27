import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AGENT_FILE = ROOT / ".claude" / "agents" / "thinker-pressure-test-pilot.md"


class ClaudeAgentPilotBoundary(unittest.TestCase):
    def test_thinker_pressure_test_pilot_is_narrow_and_read_only(self):
        text = AGENT_FILE.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]

        self.assertIn("name: thinker-pressure-test-pilot", frontmatter)
        self.assertIn("tools: Read, Grep, Glob", frontmatter)
        self.assertIn("model: inherit", frontmatter)
        self.assertIn("  - alawas-thinking-pressure-test-decision", frontmatter)
        self.assertNotIn("Bash", frontmatter)
        self.assertNotIn("Edit", frontmatter)
        self.assertIn("Stay read-only.", text)
        self.assertIn("Do not implement, migrate, rewrite, delete, export, deploy, or update Work", text)


if __name__ == "__main__":
    unittest.main()
