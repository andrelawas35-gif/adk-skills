"""Dependency-free component governance taxonomy shared with runtime."""

from typing import FrozenSet


VALID_COMPONENT_KINDS: FrozenSet[str] = frozenset({
    "skill", "protocol", "runtime", "tooling", "artifact-schema", "integration",
})

VALID_GOVERNANCE_DOMAINS: FrozenSet[str] = frozenset({
    "business", "design", "engineering", "governance", "operations",
    "research", "thinking", "cross-cutting",
})

_ROUTED_SKILL_DOMAINS = {
    "business-formulate-strategy": "business",
    "business-manage-market-intelligence": "business",
    "business-build-driver-based-plan-and-forecast": "business",
    "business-manage-enterprise-risk": "business",
    "business-source-and-govern-suppliers": "business",
    "business-direct-project-delivery": "business",
    "business-manage-customer-success": "business",
    "business-govern-initiative-portfolio": "business",
    "business-design-pricing-and-packaging": "business",
    "business-manage-liquidity-and-cash-runway": "business",
    "business-balance-demand-supply-capacity": "business",
    "business-manage-commercial-pipeline": "business",
    "business-assess-financial-decision": "business",
    "business-plan-workforce-accountability": "business",
    "business-improve-operating-process": "business",
    "design-manage-assets": "design",
    "turn-signal-into-work": "thinking",
    "develop-idea": "thinking",
    "design-tracer-bullet": "design",
    "implement-bounded-change": "engineering",
    "engineering-implement-bounded-change": "engineering",
    "verify-release-evidence": "engineering",
    "engineering-verify-release-evidence": "engineering",
    "deploy-with-recovery": "operations",
    "operations-deploy-with-recovery": "operations",
    "operations-diagnose-production-incident": "operations",
    "governance-govern-scorecards": "governance",
    "governance-review-outcome-and-adapt": "governance",
    "review-outcome-and-adapt": "governance",
    "await-director": "governance",
}


def governance_domain_for_skill(skill_name: str) -> str:
    """Return the declared domain for a routed skill; never guess from task text."""
    try:
        return _ROUTED_SKILL_DOMAINS[skill_name]
    except KeyError as exc:
        raise ValueError(f"no governance domain declared for routed skill: {skill_name}") from exc


def validate_skill_governance_domain(skill_name: str, domain: str) -> None:
    """Reject invalid domains and routed-skill/domain drift."""
    if domain not in VALID_GOVERNANCE_DOMAINS:
        raise ValueError(f"invalid governance domain: {domain}")
    expected = governance_domain_for_skill(skill_name)
    if domain != expected:
        raise ValueError(
            f"governance domain mismatch for {skill_name}: expected {expected}, got {domain}"
        )
