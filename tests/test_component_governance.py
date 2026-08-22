import unittest
from pathlib import Path

from tools.ws.component_governance import (
    VALID_COMPONENT_KINDS,
    VALID_GOVERNANCE_DOMAINS,
    governance_domain_for_skill,
    validate_skill_governance_domain,
)
from tools.ws.validate import check_ledger
from pydantic import ValidationError
from runtime.handoff import HandoffEnvelope


ROOT = Path(__file__).resolve().parents[1]


class ComponentGovernanceTests(unittest.TestCase):
    def test_canonical_taxonomy_is_exact(self):
        self.assertEqual(
            {"skill", "protocol", "runtime", "tooling", "artifact-schema", "integration"},
            set(VALID_COMPONENT_KINDS),
        )
        self.assertEqual(
            {"business", "design", "engineering", "governance", "operations", "research", "thinking", "cross-cutting"},
            set(VALID_GOVERNANCE_DOMAINS),
        )

    def test_routed_skill_domain_is_declared_and_mismatch_fails(self):
        self.assertEqual("engineering", governance_domain_for_skill("implement-bounded-change"))
        self.assertEqual("business", governance_domain_for_skill("business-formulate-strategy"))
        with self.assertRaisesRegex(ValueError, "mismatch"):
            validate_skill_governance_domain("implement-bounded-change", "business")
        with self.assertRaisesRegex(ValueError, "no governance domain declared"):
            governance_domain_for_skill("invented-skill")

    def test_ledger_registers_governed_business_skills(self):
        text = (ROOT / ".work-studio" / "component-ledger.md").read_text(encoding="utf-8")
        for name in (
            "business-formulate-strategy",
            "business-manage-market-intelligence",
            "business-build-driver-based-plan-and-forecast",
            "business-manage-enterprise-risk",
            "business-source-and-govern-suppliers",
            "business-direct-project-delivery",
            "business-manage-customer-success",
            "business-govern-initiative-portfolio",
            "business-design-pricing-and-packaging",
            "business-manage-liquidity-and-cash-runway",
            "business-balance-demand-supply-capacity",
            "business-manage-commercial-pipeline",
            "business-improve-operating-process",
            "business-assess-financial-decision",
            "business-plan-workforce-accountability",
        ):
            self.assertIn(f"`{name}`", text)
        self.assertIn("COMP-036 — Business operating pipeline", text)
        self.assertIn("`references/BUSINESS-OPERATING-PIPELINE.md`", text)
        self.assertEqual(16, text.count("- **governance domain:** business"))
        errors = check_ledger(ROOT / ".work-studio" / "objects")
        self.assertFalse([e for e in errors if "component governance" in e], errors)

    def test_runtime_handoff_carries_and_enforces_governance(self):
        fields = dict(
            handoff_id="HANDOFF-test",
            from_role="runtime",
            to_skill="implement-bounded-change",
            component_kind="skill",
            governance_domain="engineering",
            task="propose next step",
            input_refs=["2026-08-22-010"],
            expected_output="proposal",
            authority_scope="read-only-propose",
        )
        envelope = HandoffEnvelope(**fields)
        self.assertEqual("engineering", envelope.governance_domain)
        with self.assertRaises(ValidationError):
            HandoffEnvelope(**{**fields, "governance_domain": "business"})
        with self.assertRaises(ValidationError):
            HandoffEnvelope(**{**fields, "component_kind": "protocol"})
        with self.assertRaises(ValidationError):
            HandoffEnvelope(**{**fields, "governance_domain": "invented"})


if __name__ == "__main__":
    unittest.main()
