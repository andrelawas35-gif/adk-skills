"""Behavioral contracts for continuous, skill-aware grilling."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "skills" / "core"
AGREEMENT = ROOT / "references" / "AGREEMENT-LOOP.md"
PROFILES = ROOT / "references" / "SKILL-AWARE-GRILLING.md"
WORK_OBJECT = ROOT / "references" / "WORK-OBJECT.md"
FIXTURE = ROOT / "fixtures" / "skill-aware-grilling-conversation.md"


class SkillAwareGrillingContract(unittest.TestCase):
    def test_engine_is_a_real_one_question_conversation(self):
        text = " ".join(AGREEMENT.read_text().split())
        for phrase in (
            "continuous **Grilling Session**",
            "Opening context card",
            "State what changed",
            "Ask exactly one decision-bearing question and wait",
            "Never emit a completed plan",
            "There is no numerical question cap",
            "Repetition without progress is a failure",
        ):
            self.assertIn(phrase, text)

    def test_engine_defines_grounding_memory_and_code_challenges(self):
        text = " ".join(AGREEMENT.read_text().split())
        for phrase in (
            "**Evidence Ledger**",
            "cite the exact local file",
            "Treat Codex memory as a discovery aid",
            "newly inferred preference remains session-local",
            "When sources conflict, expose the conflict",
        ):
            self.assertIn(phrase, text)

    def test_engine_has_activation_non_activation_and_narrow_acceptance(self):
        text = " ".join(AGREEMENT.read_text().split())
        self.assertIn("the user explicitly asks to be grilled", text)
        self.assertIn("Do not activate for routine work", text)
        self.assertIn("`do recommended` accepts only", text)
        self.assertIn("never closes the session", text)

    def test_every_core_skill_declares_its_named_profile(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            skill = path.parent.name
            text = path.read_text()
            with self.subTest(skill=skill):
                self.assertIn("## Skill Grilling Profile", text)
                self.assertIn(f"`{skill}` profile", text)
                self.assertIn("references/SKILL-AWARE-GRILLING.md", text)

    def test_reference_has_every_profile_and_profile_shape(self):
        text = PROFILES.read_text()
        for path in sorted(CORE.glob("*/SKILL.md")):
            self.assertIn(f"### `{path.parent.name}`", text)
        sections = re.split(r"^### `[^`]+`$", text, flags=re.MULTILINE)[1:]
        self.assertEqual(len(sections), len(list(CORE.glob("*/SKILL.md"))))
        for path, section in zip(sorted(CORE.glob("*/SKILL.md")), sections):
            with self.subTest(skill=path.parent.name):
                for field in (
                    "**Inspect**",
                    "**First frontier**",
                    "**Challenge and novelty**",
                    "**Route**",
                    "**Complete when**",
                ):
                    self.assertIn(field, section)

    def test_profile_catalogue_defines_continuity_state(self):
        text = PROFILES.read_text()
        for field in (
            "Context Card",
            "Active profile and activation reason",
            "Decision Frontier",
            "Coverage",
            "Current recommendation",
            "Confirmed decisions",
            "Evidence Ledger",
            "Next question",
            "Coverage Proof",
        ):
            self.assertIn(field, text)

    def test_conductor_owns_lazy_persistence_and_concurrency(self):
        conductor = (CORE / "conduct-work-object" / "SKILL.md").read_text()
        work_object = WORK_OBJECT.read_text()
        self.assertIn("Create `## Grilling Session` lazily", conductor)
        self.assertIn("sole writer", conductor)
        self.assertIn("reconstruct the Context Card", work_object)
        self.assertIn("optimistic concurrency", work_object)

    def test_specialists_preserve_context_and_return_continuity(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            if path.parent.name == "conduct-work-object":
                continue
            text = " ".join(path.read_text().split())
            with self.subTest(skill=path.parent.name):
                self.assertIn("On direct entry, route through", text)
                self.assertIn("compact continuity record", text)
                self.assertIn("do not reset context", text)

    def test_fixture_covers_multiturn_nonactivation_long_loop_and_recovery(self):
        text = FIXTURE.read_text()
        for scenario in range(1, 13):
            self.assertIn(f"## Scenario {scenario} ", text)
        for path in sorted(CORE.glob("*/SKILL.md")):
            self.assertIn(f"`{path.parent.name}`", text)
        for phrase in (
            "asks exactly one question and waits",
            "Routine work does not trigger ceremony",
            "more than 200 material",
            "Every turn reduces uncertainty",
            "Coverage Proof",
            "concurrent revision",
        ):
            self.assertIn(phrase, text)

    def test_glossary_uses_canonical_terms(self):
        text = (ROOT / "CONTEXT.md").read_text()
        for term in (
            "**Grilling Session**",
            "**Context Card**",
            "**Decision Frontier**",
            "**Evidence Ledger**",
            "**Skill Grilling Profile**",
            "**Coverage Proof**",
        ):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
