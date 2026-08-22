"""Handoff contract records (Phase 6, WO 2026-08-17-008).

Runtime-plane records per Direction A and build plan lines 201-202: they live in
the langgraph checkpoint (runtime state), never canonical state -- ADR 0025 line
45 and build plan line 239 forbid a runtime inference from creating a canonical
claim. A ``HandoffEnvelope`` is recorded before dispatch; a ``HandoffReceipt``
after a branch completes. Both are strict Pydantic models (``extra="forbid"``)
so the runtime contract and any future consumer cannot silently disagree.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tools.ws.component_governance import (
    VALID_COMPONENT_KINDS,
    VALID_GOVERNANCE_DOMAINS,
    validate_skill_governance_domain,
)

ComponentKind = Literal[
    "skill", "protocol", "runtime", "tooling", "artifact-schema", "integration"
]
GovernanceDomain = Literal[
    "business", "design", "engineering", "governance", "operations",
    "research", "thinking", "cross-cutting",
]

if set(ComponentKind.__args__) != set(VALID_COMPONENT_KINDS):
    raise RuntimeError("runtime ComponentKind drifted from deterministic taxonomy")
if set(GovernanceDomain.__args__) != set(VALID_GOVERNANCE_DOMAINS):
    raise RuntimeError("runtime GovernanceDomain drifted from deterministic taxonomy")


class HandoffEnvelope(BaseModel):
    """Dispatch record: what one specialist is asked to do (build plan 201)."""

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    from_role: str
    to_skill: str
    component_kind: ComponentKind
    governance_domain: GovernanceDomain
    task: str
    input_refs: List[str] = Field(default_factory=list)
    expected_output: str
    authority_scope: str

    @model_validator(mode="after")
    def validate_governed_route(self) -> "HandoffEnvelope":
        if self.component_kind != "skill":
            raise ValueError("runtime specialist handoffs must target component_kind=skill")
        validate_skill_governance_domain(self.to_skill, self.governance_domain)
        return self


class HandoffReceipt(BaseModel):
    """Completion record from one specialist branch (build plan 202)."""

    model_config = ConfigDict(extra="forbid")

    status: str
    output_refs: List[str] = Field(default_factory=list)
    verification_gaps: List[str] = Field(default_factory=list)
    proposed_next_skill: str
    started_at: datetime
    completed_at: datetime


# Mirrors the canonical state->skill routing table in
# skills/core/governance-conduct-work-object/SKILL.md ("### 6. Route to
# specialist"). Kept as a manually-synced copy (WO 2026-08-17-001 Decision 6):
# if the conductor's table changes, this dict must be updated to match by
# hand -- there is no automatic sync. There IS automatic drift detection,
# though: runtime/tests/test_handoff_graph.py's
# test_state_routing_table_stays_in_sync_with_conductor parses the
# conductor's table directly and fails if this dict disagrees (routing
# audit WO 2026-08-22-009, G3).
_STATE_ROUTING_TABLE = {
    "notice": "turn-signal-into-work",
    "explore": "develop-idea",
    "design": "design-tracer-bullet",
    "build": "implement-bounded-change",
    "verify": "verify-release-evidence",
    "release": "deploy-with-recovery",
    "observe": "review-outcome-and-adapt",
    "close": "review-outcome-and-adapt",
}


def derive_proposal(state: str, role: str) -> str:
    """Derive a real next-skill proposal from a Work Object's state.

    Pure and read-only by construction: maps a canonical ``state`` value to
    the real skill name the conductor would route to, per
    ``_STATE_ROUTING_TABLE``, and never touches canonical state (ADR 0025 /
    build plan 239). Connects a real named studio skill (WO 2026-08-17-001
    Decision 6), replacing Decision 5's generic "implement"/"verify"
    stand-in strings. ``role`` no longer affects the return value -- the
    source table is state-keyed only, not role-keyed; an unrecognized state
    still defers to the director.
    """
    return _STATE_ROUTING_TABLE.get(state, "await-director")


def derive_authority_scope(consequence: str) -> str:
    """Derive the envelope's authority scope from a Work Object's consequence.

    Pure and read-only: maps a canonical ``consequence`` value to the authority
    scope carried on the runtime HandoffEnvelope (Decision 7), grounded in
    references/CONSEQUENCE-AUTHORITY.md. It is a runtime label describing the
    handoff record's disposition, never a canonical write or an authority grant.
    """
    if consequence == "low":
        return "read-only"
    if consequence == "meaningful":
        return "read-only-propose"
    if consequence == "high":
        return "governed"
    return "unknown"


def derive_verification_gaps(
    has_checked_success_evidence: bool,
    has_evidence_ledger_entries: bool,
) -> List[str]:
    """Derive deterministic verification gaps from a WO's verification signals.

    Pure and read-only (Decision 8): maps whether a WO's success-evidence
    checklist has any checked item and whether its evidence ledger is populated
    to a possibly-empty list of gap strings recorded on the verify branch's
    HandoffReceipt. Never touches canonical state.
    """
    gaps: List[str] = []
    if not has_checked_success_evidence:
        gaps.append("no checked success evidence")
    if not has_evidence_ledger_entries:
        gaps.append("no evidence ledger entries")
    return gaps


def merge_proposals(receipts: List[dict]) -> str:
    """Merge branch proposals into one deterministic handoff proposal.

    Pure and read-only (Decision 11): collects each receipt's
    proposed_next_skill, deduplicates, and joins the sorted result with "; ".
    Since proposals are state-keyed (WO-001 Decision 6), identical branch
    proposals collapse to a single skill name; distinct proposals stay sorted.
    Never touches canonical state.
    """
    skills = sorted(
        {
            r.get("proposed_next_skill", "")
            for r in receipts
            if r.get("proposed_next_skill")
        }
    )
    return "; ".join(skills)
