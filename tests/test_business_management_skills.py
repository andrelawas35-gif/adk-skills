from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "core"
PROFILES = ROOT / "references" / "SKILL-AWARE-GRILLING.md"
PIPELINE = ROOT / "references" / "BUSINESS-OPERATING-PIPELINE.md"
FIXTURE = ROOT / "fixtures" / "slice-5-business-management-skills.md"

SKILLS = {
    "business-formulate-strategy": (
        "coherent choice set",
        "public commitments",
        "business-manage-market-intelligence",
    ),
    "business-manage-market-intelligence": (
        "market boundary",
        "paid/licensed data",
        "business-manage-commercial-pipeline",
    ),
    "business-build-driver-based-plan-and-forecast": (
        "driver-based planning baseline",
        "published forecasts",
        "business-assess-financial-decision",
    ),
    "business-manage-enterprise-risk": (
        "residual exposure",
        "risk acceptance",
        "operations-diagnose-production-incident",
    ),
    "business-source-and-govern-suppliers": (
        "make/buy",
        "supplier contact",
        "business-assess-financial-decision",
    ),
    "business-direct-project-delivery": (
        "change-control rule",
        "baseline changes",
        "engineering-implement-bounded-change",
    ),
    "business-manage-customer-success": (
        "realized customer value",
        "customer contact",
        "business-manage-commercial-pipeline",
    ),
    "business-govern-initiative-portfolio": (
        "scarce attention",
        "funding",
        "business-direct-project-delivery",
    ),
    "business-design-pricing-and-packaging": (
        "value metric",
        "published prices",
        "business-manage-commercial-pipeline",
    ),
    "business-manage-liquidity-and-cash-runway": (
        "cash on time",
        "borrow",
        "business-build-driver-based-plan-and-forecast",
    ),
    "business-balance-demand-supply-capacity": (
        "usable capacity",
        "purchase orders",
        "business-manage-liquidity-and-cash-runway",
    ),
    "business-manage-commercial-pipeline": (
        "stage exit criteria",
        "edit a CRM",
        "business-assess-financial-decision",
    ),
    "business-assess-financial-decision": (
        "cash timing",
        "move money",
        "business-plan-workforce-accountability",
    ),
    "business-plan-workforce-accountability": (
        "role-level coverage",
        "personnel action",
        "business-improve-operating-process",
    ),
    "business-improve-operating-process": (
        "actual current state",
        "live process",
        "operations-diagnose-production-incident",
    ),
}


class BusinessManagementSkillContract(unittest.TestCase):
    @staticmethod
    def normalized(path):
        return " ".join(path.read_text(encoding="utf-8").lower().split())

    def test_skills_have_distinct_decision_and_authority_boundaries(self):
        for name, required in SKILLS.items():
            text = (CORE / name / "SKILL.md").read_text(encoding="utf-8")
            normalized = " ".join(text.lower().split())
            self.assertIn(f"name: {name}", text)
            self.assertIn("## Governing principle", text)
            self.assertIn("## Consequence and authority rules", text)
            self.assertIn("## Stage workflow", text)
            self.assertIn("## Final self-check", text)
            for phrase in required:
                self.assertIn(phrase.lower(), normalized, f"{name} missing {phrase!r}")

    def test_external_effects_are_never_implicit(self):
        for name in SKILLS:
            text = self.normalized(CORE / name / "SKILL.md")
            self.assertIn("authority", text, name)
            self.assertTrue(
                "requires explicit scoped authority" in text
                or "requires scoped authority" in text
                or "require explicit scoped authority" in text,
                name,
            )

    def test_each_skill_has_a_grilling_profile_and_fixture_scenario(self):
        profiles = PROFILES.read_text(encoding="utf-8")
        fixture = FIXTURE.read_text(encoding="utf-8")
        for name in SKILLS:
            self.assertIn(f"`alawas-{name}`", profiles)
            self.assertIn(name, fixture)

    def test_business_skills_share_operating_pipeline_reference(self):
        pipeline = PIPELINE.read_text(encoding="utf-8")
        self.assertIn("does not replace the Work Object lifecycle", pipeline)
        self.assertIn("business-manage-commercial-pipeline", pipeline)
        self.assertIn("Minimum handoff record", pipeline)
        for name in SKILLS:
            self.assertIn(name, pipeline)
            text = (CORE / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Business operating pipeline", text)
            self.assertIn("references/BUSINESS-OPERATING-PIPELINE.md", text)


if __name__ == "__main__":
    unittest.main()
