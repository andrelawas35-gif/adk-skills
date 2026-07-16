"""Behavioral contracts for skill-aware grilling."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "skills" / "core"
REFERENCE = ROOT / "references" / "SKILL-AWARE-GRILLING.md"


class SkillAwareGrillingContract(unittest.TestCase):
    def test_every_core_skill_declares_its_named_lens(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            skill = path.parent.name
            with self.subTest(skill=skill):
                self.assertIn("## Skill-aware grilling lens", path.read_text())
                self.assertIn(f"`{skill}` lens", path.read_text())

    def test_reference_has_every_lens_and_handoff_fields(self):
        text = REFERENCE.read_text()
        for path in sorted(CORE.glob("*/SKILL.md")):
            self.assertIn(f"### `{path.parent.name}`", text)
        for field in (
            "Current recommendation",
            "Confirmed decisions",
            "Open branches",
            "Evidence and assumptions",
            "Receiving first question",
        ):
            self.assertIn(field, text)

    def test_conductor_owns_lazy_grilling_persistence(self):
        text = (CORE / "conduct-work-object" / "SKILL.md").read_text()
        self.assertIn("Create the `## Grilling` section lazily", text)
        self.assertIn("sole writer", text)

    def test_specialists_route_direct_entry_and_return_handoff(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            if path.parent.name == "conduct-work-object":
                continue
            with self.subTest(skill=path.parent.name):
                text = " ".join(path.read_text().split())
                self.assertIn("On direct entry, route through", text)
                self.assertIn("standard five-field Grilling handoff", text)


if __name__ == "__main__":
    unittest.main()
