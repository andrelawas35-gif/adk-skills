"""Behavioral contracts for continuous, skill-aware grilling."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "skills" / "core"
ENGINE = CORE / "thinking-grilling-session" / "SKILL.md"
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
            "Only confirmed shared understanding authorizes",
            "Two answered questions are never a reason to end a session",
            "Do not infer an exhaustive list of future questions",
            "Re-evaluate the Decision Frontier after every answer",
            "ephemeral",
            "Infer the smallest fitting initial Skill Grilling Profile",
            "Candidate Card",
            "Three-part threshold",
            "Candidate entry always requires explicit user acceptance",
            "Changed since last turn",
            "Choice Frame",
            "at most two alternatives",
            "not a score, vote, or probability of success",
            "When every credible option is low confidence",
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
        self.assertIn("Do not nominate routine work", text)
        self.assertIn("`do recommended` accepts only", text)
        self.assertIn("never closes the session", text)

    def test_every_stage_skill_uses_a_minimal_engine_entry(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            skill = path.parent.name
            if path == ENGINE:
                continue
            text = " ".join(path.read_text().split())
            with self.subTest(skill=skill):
                self.assertIn("## Grilling entry and stage lens", text)
                self.assertIn(f"`{skill}` profile", text)
                self.assertIn("Follow `references/AGREEMENT-LOOP.md` in full", text)
                self.assertIn("references/SKILL-AWARE-GRILLING.md", text)
                self.assertIn("nominate a Grilling Candidate", text)
                self.assertIn("Candidate Card", text)
                self.assertIn("do not silently start a continuous session", text)

    def test_engine_is_a_first_class_ephemeral_entry_point(self):
        text = " ".join(ENGINE.read_text().split())
        for phrase in (
            "visible entry point",
            "explicit grilling request in a Work Studio-pinned project",
            "Run ephemerally unless an active Work Object is relevant",
            "user asks to retain the session",
            "generic `grilling` skill",
        ):
            self.assertIn(phrase, text)

    def test_reference_has_every_profile_and_profile_shape(self):
        text = PROFILES.read_text()
        for path in sorted(CORE.glob("*/SKILL.md")):
            if path == ENGINE:
                continue
            self.assertIn(f"### `{path.parent.name}`", text)
        sections = re.split(r"^### `[^`]+`$", text, flags=re.MULTILINE)[1:]
        stage_skills = [path for path in sorted(CORE.glob("*/SKILL.md"))
                        if path != ENGINE]
        self.assertEqual(len(sections), len(stage_skills))
        for path, section in zip(stage_skills, sections):
            with self.subTest(skill=path.parent.name):
                for field in (
                    "**Gates**",
                    "**Escalation**",
                    "**Pressure scenario**",
                ):
                    self.assertIn(field, section)

    def test_engine_owns_continuity_and_profiles_remain_stage_only(self):
        agreement = AGREEMENT.read_text()
        profiles = PROFILES.read_text()
        for field in (
            "Context Card",
            "Active profile and activation reason",
            "Decision Frontier",
            "Coverage",
            "Current recommendation",
            "Confirmed decisions",
            "Evidence Ledger",
            "Next question",
        ):
            self.assertIn(field, agreement)
        for forbidden in (
            "## Shared behavior",
            "## Compact Grilling Session state",
            "## Continuity record",
            "## Persistence routing",
            "## Coverage Proof across profiles",
        ):
            self.assertNotIn(forbidden, profiles)

    def test_conductor_owns_lazy_persistence_and_concurrency(self):
        conductor = (CORE / "governance-conduct-work-object" / "SKILL.md").read_text()
        work_object = WORK_OBJECT.read_text()
        self.assertIn("conductor owns durable checkpoint writes only", conductor)
        self.assertIn("sole writer", conductor)
        self.assertIn("reconstruct the Context Card", work_object)
        self.assertIn("optimistic concurrency", work_object)

    def test_stage_skills_do_not_reimplement_the_engine(self):
        for path in sorted(CORE.glob("*/SKILL.md")):
            if path.parent.name in {"governance-conduct-work-object", "thinking-grilling-session"}:
                continue
            text = " ".join(path.read_text().split())
            with self.subTest(skill=path.parent.name):
                self.assertNotIn("IS the Agreement Loop", text)
                self.assertNotIn("end every response after exactly one", text)
                self.assertNotIn("owns Grilling Session continuity", text)

    def test_fixture_covers_multiturn_nonactivation_long_loop_and_recovery(self):
        text = FIXTURE.read_text()
        for scenario in range(1, 16):
            self.assertIn(f"## Scenario {scenario} ", text)
        for path in sorted(CORE.glob("*/SKILL.md")):
            if path != ENGINE:
                self.assertIn(f"`{path.parent.name}`", text)
        for phrase in (
            "asks exactly one question and waits",
            "Routine work does not trigger ceremony",
            "more than 200 material",
            "Every turn reduces uncertainty",
            "Coverage Proof",
            "concurrent revision",
            "confirmation of shared understanding",
            "Two answers do not end the session",
            "exactly one third",
            "frontier is discovered progressively",
            "drip-feed that fixed list",
            "ephemeral",
            "Work Studio-pinned project",
            "Candidate Card",
            "does not silently enter",
            "Changed since last turn",
            "all credible options are low confidence",
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
