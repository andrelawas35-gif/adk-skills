"""General orchestrator deterministic routing tracer (WO 2026-08-25-003 Decision 5).

Tracer-bullet scope only: proves the deterministic signal-extraction path
(Work Object ID, skill name, COMP reference, domain keyword) before any LLM
fallback, skill invocation, or authority forwarding is built (Decision 5
non-goals). Does not call conduct-work-object, AgentResolver, or any
production skill -- this module only decides WHERE a request would go.

Domain registry is derived from the skill directory prefix convention
(skills/core/<domain>-<name>/SKILL.md) rather than a separate declarative
file, matching WO 2026-08-25-001 Decision 8's "in-code, no config file"
precedent for the agent registry.

Step 4 (WO 2026-08-25-003): Extended to handle compound requests with WO ID
dominance and return-only pattern for skill-invoking-skill nesting (OQs 7-9).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, List, Dict

from pydantic import BaseModel, ConfigDict

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills" / "core"
WORK_OBJECTS_DIR = REPO_ROOT / ".work-studio" / "objects"

KNOWN_DOMAINS = frozenset(
    {"business", "design", "engineering", "governance", "operations", "production", "research", "thinking"}
)

WO_ID_PATTERN = re.compile(r"\b(20\d\d-\d\d-\d\d-\d{3})\b")
COMP_PATTERN = re.compile(r"\bCOMP-(\d{3})\b")

# Op-level component-to-domain map for the ranges verified in this session
# (COMP-042 through COMP-047, WO 2026-08-23-001 section 4). Extending this
# beyond the tracer's tested range is future work, not part of Decision 5.
COMP_DOMAIN_MAP = {
    "042": "production",
    "043": "production",
    "044": "production",
    "045": "production",
    "046": "production",
    "047": "production",
}

# Keyword -> (domain, skill) map covering the tracer's 6 test cases only.
# This is a starter table, not an exhaustive classifier -- requests that
# miss every entry correctly fall through to needs_llm_fallback (Decision 2).
KEYWORD_ROUTES = [
    (re.compile(r"\brender\b", re.IGNORECASE), "production", "production-operate-blender"),
    (re.compile(r"\bshot\b", re.IGNORECASE), "production", "production-operate-blender"),
    (re.compile(r"\bimplement\b", re.IGNORECASE), "engineering", "engineering-implement-bounded-change"),
    (re.compile(r"\bpricing\b", re.IGNORECASE), "business", "business-design-pricing-and-packaging"),
    (re.compile(r"\bstrategy\b", re.IGNORECASE), "business", "business-formulate-strategy"),
]


class RoutingDecision(BaseModel):
    """Normalized routing outcome. Return-only pattern (Step 4, OQ 9) -- nothing dispatched directly here."""

    model_config = ConfigDict(extra="forbid")

    domain: Optional[str] = None
    skill: Optional[str] = None
    consequence: Optional[str] = None
    signal_used: str = "none"
    confidence: str = "low"
    needs_llm_fallback: bool = False
    
    # Step 4 additions (OQs 7-9):
    compound_handled: bool = False       # True if compound request was resolved via WO ID dominance
    routing_note: Optional[str] = None   # Human-readable explanation of routing choice
    suggested_splits: List[str] | None = None  # For compound requests without dominant signal


def _skill_domain_from_name(skill_name: str) -> Optional[str]:
    """Extract the domain prefix from a skill directory name.

    Skill directories are named ``<domain>-<rest>`` (e.g.
    ``production-operate-blender``). The domain is the first hyphen-delimited
    segment, validated against KNOWN_DOMAINS rather than trusted blindly.
    """
    prefix = skill_name.split("-", 1)[0]
    return prefix if prefix in KNOWN_DOMAINS else None


def _find_skill_by_name(request_text: str) -> Optional[str]:
    """Return a skill directory name mentioned verbatim in the request."""
    if not SKILLS_DIR.is_dir():
        return None
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and skill_dir.name in request_text:
            return skill_dir.name
    return None


def _read_wo_domain(wo_id: str) -> Optional[str]:
    """Read the first ``domain:`` frontmatter value for a Work Object ID.

    Returns None if no matching Work Object file exists or the frontmatter
    has no domain field -- callers treat that as "signal found, domain
    unknown" rather than falling back to keyword matching.
    """
    matches = list(WORK_OBJECTS_DIR.glob(f"**/{wo_id}-*.md"))
    if not matches:
        return None
    text = matches[0].read_text(encoding="utf-8")
    domain_match = re.search(r"^domain:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if not domain_match:
        return None
    first_domain = domain_match.group(1).split(",")[0].strip()
    return first_domain or None


def _read_wo_consequence(wo_id: str) -> Optional[str]:
    """Read the ``consequence:`` frontmatter value for a Work Object ID."""
    matches = list(WORK_OBJECTS_DIR.glob(f"**/{wo_id}-*.md"))
    if not matches:
        return None
    text = matches[0].read_text(encoding="utf-8")
    consequence_match = re.search(r"^consequence:\s*(\S+)", text, re.MULTILINE)
    return consequence_match.group(1).strip() if consequence_match else None


def _extract_wo_ids_from_request(request_text: str) -> List[str]:
    """Extract all Work Object IDs from request text.

    Returns list of WO ID strings in order of appearance (for tie-breaking by recency if needed).
    """
    return WO_ID_PATTERN.findall(request_text)


def _get_max_consequence(consequences: List[Optional[str]]) -> str:
    """Get maximum consequence from a list of consequences.

    Priority: None < low < meaningful < high
    
    Returns "low" if all are None (default for Step 4).
    """
    consequence_priority = {None: 0, "low": 1, "meaningful": 2, "high": 3}
    
    max_consequence = "low"  # Default for WO-less requests per Decision 3
    max_priority = consequence_priority[max_consequence]
    
    for c in consequences:
        if c and consequence_priority.get(c, 0) > max_priority:
            max_consequence = c
            max_priority = consequence_priority[c]
    
    return max_consequence


def route_request(request_text: str) -> RoutingDecision:
    """Classify a natural-language request into a routing decision.

    Signal precedence (OQ 8): WO ID > skill name > COMP reference > domain keyword > no signal.
    
    Compound handling (OQ 7, Option C - WO dominance): When multiple WOs are referenced,
    the highest consequence dominates and lifecycle operations route through governance conductor.
    
    Return-only pattern (OQ 9): This function returns RoutingDecision objects; skill invocation
    is handled by platform adapter layer to avoid recursion issues.
    """
    # Step 4: Extract all WO IDs from request for compound handling
    wo_ids = _extract_wo_ids_from_request(request_text)
    
    if len(wo_ids) >= 2:
        # Compound request with multiple WOs - check for high consequence
        consequences = [_read_wo_consequence(wo_id) for wo_id in wo_ids]
        
        # If any WO has "high" consequence, use that as gating authority
        max_conseq = _get_max_consequence(consequences)
        
        if max_conseq == "high":
            return RoutingDecision(
                domain=None,  # Will be resolved by governance conductor for high-consequence WOs
                skill="governance-conduct-work-object",
                consequence="high",
                signal_used="wo_id_compound_high",
                confidence="high",
                compound_handled=True,
                routing_note=f"Compound request with {len(wo_ids)} WOs; using maximum consequence 'high' for gating",
            )
    
    # Single WO or no compound concerns - use standard priority order
    
    wo_match = WO_ID_PATTERN.search(request_text)
    if wo_match:
        wo_id = wo_match.group(1)
        domain = _read_wo_domain(wo_id)
        consequence = _read_wo_consequence(wo_id)
        
        # Step 4: Handle single WO with compound keyword signals (WO ID dominates)
        # Check if there are other domain keywords present
        has_other_signals = any(p.search(request_text) for p, _, _ in KEYWORD_ROUTES)
        
        if has_other_signals and wo_id:
            return RoutingDecision(
                domain=domain or "governance",  # Default to governance if WO domain unknown
                skill="governance-conduct-work-object",
                consequence=consequence,
                signal_used="wo_id_dominates",
                confidence="high",
                compound_handled=True,
                routing_note=f"WO ID dominates compound request (lifecycle operation)",
            )
        
        if domain is not None:
            return RoutingDecision(
                domain=domain,
                skill="governance-conduct-work-object",
                consequence=consequence,
                signal_used="wo_id",
                confidence="high",
            )

    skill_name = _find_skill_by_name(request_text)
    if skill_name is not None:
        domain = _skill_domain_from_name(skill_name)
        return RoutingDecision(
            domain=domain,
            skill=skill_name,
            signal_used="skill_name",
            confidence="high",
        )

    comp_match = COMP_PATTERN.search(request_text)
    if comp_match:
        comp_domain = COMP_DOMAIN_MAP.get(comp_match.group(1))
        return RoutingDecision(
            domain=comp_domain,
            skill=None,
            signal_used="comp_ref",
            confidence="high" if comp_domain else "low",
        )

    for pattern, domain, skill in KEYWORD_ROUTES:
        if pattern.search(request_text):
            return RoutingDecision(
                domain=domain,
                skill=skill,
                signal_used="keyword",
                confidence="medium",
            )

    # No signal found - trigger LLM fallback (OQ 6 resolution)
    return RoutingDecision(
        domain=None,
        skill=None,
        signal_used="none",
        confidence="low",
        needs_llm_fallback=True,
        routing_note="No deterministic signal found; invoke session model for intent classification",
    )