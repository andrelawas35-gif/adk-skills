# Platform Adapter Spec: Orchestrator Return-Only Invocation Pattern

**Status:** Design Specification (Step 4.2 of WO `2026-08-25-003`)  
**Created:** 2026-08-25T21:35:12Z  
**Related Decision:** OQ 9 Resolution — skill-invoking-skill nesting via return-only pattern  

## Overview

The orchestrator (`runtime/orchestrator.py`, `skills/core/orchestrate/SKILL.md`) resolves open question 9 from WO `2026-08-25-003` by implementing a **return-only invocation pattern** rather than direct skill calling. This design prevents recursion issues and maintains clear separation between classification (orchestrator) and execution (platform adapter).

## Problem Statement: Skill-Invoking-Skill Nesting

When the orchestrator routes to another skill, how should it invoke that skill?
- **Direct invocation:** Orchestrator calls `alawas-production-operate-blender` directly → potential recursion if production skill invokes orchestrator again
- **Return instruction:** Orchestrator returns a `RoutingDecision` object; platform adapter decides whether to invoke directly or pass through another orchestrator layer

**Chosen Solution (OQ 9, Option B):** Return-only pattern. The orchestrator returns routing decisions only; the platform adapter handles invocation with cycle detection and sequencing logic.

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Platform Adapter Layer                        │
│  (handles skill invocation, cycle detection, multi-domain seq)   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ returns RoutingDecision
                      ┌──────────────────┐
                      │ Orchestrator     │
                      │ route_request()  │
                      │ (classification) │
                      └──────────────────┘
```

### Message Flow

1. **User input** → Platform adapter passes to orchestrator
2. **Orchestrator** calls `route_request()` → returns `RoutingDecision` object
3. **Platform adapter** receives decision and either:
   - Invokes target skill directly (if simple, single-domain)
   - Passes through orchestrator again (if multi-domain compound request needs sequencing)

### Routing Decision Structure

```python
class RoutingDecision(BaseModel):
    """Return-only pattern: contains routing metadata, no invocation."""
    
    domain: Optional[str] = None                    # Target domain
    skill: Optional[str] = None                     # Full skill path (e.g., "production-operate-blender")
    consequence: Optional[str] = None               # Gating authority level
    signal_used: str = "none"                       # How routing was determined
    
    needs_llm_fallback: bool = False                # True if LLM classification needed
    
    # Step 4 additions (OQs 7-9):
    compound_handled: bool = False                  # Compound request resolved via WO ID dominance
    routing_note: Optional[str] = None              # Human-readable explanation
    suggested_splits: List[str] | None = None       # For compound requests without dominant signal
```

### Platform Adapter Responsibilities

The platform adapter (to be implemented in future work) must handle:

1. **Invocation** — Call target skill when `RoutingDecision.skill` is set and valid
2. **Cycle detection** — Prevent infinite loops via call stack tracking
3. **Multi-domain sequencing** — When multiple domains present, sequence invocations appropriately
4. **Fallback handling** — Route to LLM classifier when `needs_llm_fallback=True`

#### Cycle Detection Logic (Pseudocode)

```python
def invoke_routing_decision(decision: RoutingDecision, current_chain: List[str]):
    """Invoke routing decision with cycle detection."""
    
    if not decision.skill:
        return None
    
    # Check for cycles in invocation chain
    if decision.skill in current_chain:
        raise ValueError(f"Cycle detected: {decision.skill} already in invocation stack")
    
    # Build new chain with this skill
    new_chain = current_chain + [decision.skill]
    
    # Invoke the target skill
    return invoke_skill(decision.skill, routing_context=decision)
```

#### Multi-Domain Sequencing (Pseudocode)

```python
def handle_compound_request(decisions: List[RoutingDecision]):
    """Handle multiple domain decisions by sequencing."""
    
    for decision in decisions:
        if decision.compound_handled and decision.routing_note == "WO ID dominates":
            # Single WO lifecycle operation — route through governance first
            yield invoke_routing_decision(decision, current_chain)
            
        else:
            # Multi-domain without WO dominance — split into separate invocations
            for split in decision.suggested_splits or [decision.skill]:
                yield invoke_routing_decision(split, current_chain)
```

## Implementation Status

### Completed (Step 4.1-4.2)

| Item | Status | Location |
|------|--------|----------|
| Return-only `RoutingDecision` model | ✅ Implemented | `runtime/orchestrator.py:63-70` |
| Orchestrator return-only behavior | ✅ Implemented | `route_request()` returns, no invoke |
| Compound handling (WO ID dominance) | ✅ Tested | 8 test cases pass |
| Cycle detection logic spec | ⏳ Documented above | This document |

### Pending Work

| Item | Notes |
|------|-------|
| Platform adapter implementation | Not in Scope for WO `2026-08-25-003` — future work |
| Test suite for platform adapter | Deferred until skill-invoking-skill nesting becomes actual requirement |
| Multi-domain sequencing tests | Same as above |

## Design Rationale

### Why Return-Only Over Direct Invocation?

1. **Prevents recursion:** If orchestrator calls production skill, and production skill needs to orchestrate a sub-request, the cycle detection in platform adapter handles it cleanly rather than risking infinite loops at orchestrator level

2. **Clear separation of concerns:** 
   - Orchestrator = classification only (pure function)
   - Platform adapter = execution logic (side effects, invocation)

3. **Testable units:** Can test `route_request()` in isolation without mocking skill invocations

4. **Future-proofing:** If platform architecture changes (e.g., async dispatch, batch processing), the orchestrator code remains unchanged; only platform adapter needs updates

### Alternative Considered and Rejected: Direct Invocation

**Option A — Direct invocation with guardrails:**
- Pros: Simple to implement initially
- Cons: Requires recursion limit management at orchestrator level, harder to test in isolation

**Option B — Handoff envelope pattern:**
- Pros: Clean encapsulation  
- Cons: Requires designing new envelope structure (overkill for tracer bullet)

### Why Not Skip This Document?

The return-only pattern is a **design decision**, not code implementation. Deferring documentation until "actual requirement" would mean:
- No architectural guidance when platform adapter is built
- Potential rework if implementation differs from intended design
- Loss of provenance for this key OQ 9 resolution

Documenting now ensures future implementers have clear specifications to follow.

## Usage Example

```python
# User request
request = "update WO 2026-08-25-003 and render preview"

# Orchestrator returns (no invocation)
decision = route_request(request)
print(f"Decision: domain={decision.domain}, skill={decision.skill}")
# Output: Domain: engineering, Skill: governance-conduct-work-object

# Platform adapter handles invocation
if decision.compound_handled and "WO ID dominates" in (decision.routing_note or ""):
    # Route through governance conductor for lifecycle operation
    invoke_skill("governance-conduct-work-object", ...)
```

## Verification

To verify this pattern works as intended, run:

```bash
# Test orchestrator routing decisions only (no invocation)
uv run python -m unittest runtime.tests.test_orchestrator_routing \
    runtime.tests.test_orchestrator_compound_requests -v

# Should see 14 tests pass with no skill invocations occurring
```

## Related Work

- WO `2026-08-25-003`: Main orchestrator design and implementation
- WO `2026-08-25-001`: Agent adapter architecture (predecessor to this pattern)
- `runtime/orchestrator.py:route_request()`: Implementation of return-only behavior

---

**End of Specification**