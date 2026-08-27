---
name: alawas-orchestrate
description: "Use when a request needs default domain or skill routing; returns routing decisions and never invokes target skills directly."
default_tier: low
platform: github-copilot
---
# Orchestrate

## Status Update: Promoted to Default Entry Point (Step 5)

This skill is now the **default entry point** for all incoming requests. Previously it was an explicit skill (`/orchestrate <request>`); now it handles routing implicitly through the platform adapter layer (WO `2026-08-25-003` Step 5). See [platform-adapter-return-only-spec.md](../../deliverables/2026-08-25-003-platform-adapter-return-only-spec.md) for architectural details.

## Governing principle

One place to bring a request without knowing which of the 8 domains or 49
skills handles it. This skill classifies the request and names the target —
it never executes the target itself. Routing and execution stay separated so
a misclassification is a wrong suggestion, not a wrong action.

## Personal working lens

This skill wraps `runtime/orchestrator.py`'s `route_request()` tracer (WO
`2026-08-25-003` Decision 5). It implements the return-only invocation pattern
from open question 9: returns routing decisions for platform adapter to invoke,
never calls skills directly.

**Step 5 change:** Now invoked by default through platform adapter for all
messages (not just explicit `/orchestrate` calls), promoting it as the single
entry point per Decision 4's end state.

## Boundaries and non-goals

**This skill does:**
- Call `route_request()` against every incoming request text
- Report domain, skill (if determined), consequence, and routing metadata
- When no deterministic signal found, reason directly about which of the 8
  domains and their skills best fits — session model IS the fallback classifier
  (Decision 6)
- Log every fallback reasoning decision to `runtime/traces/orchestrator_fallback_log.jsonl`

**This skill does NOT:**
- Invoke target skills directly — returns `RoutingDecision` for platform adapter
  to handle invocation with cycle detection (OQ9 resolution, see spec doc above)
- Dispatch to separate model process for fallback (Decision 6 — session reasons directly)
- Assess or enforce consequence beyond reporting WO's existing field (Decision 3)

## Routing capabilities

**Signal precedence (WO 2026-08-25-003 Decision 2):**
1. **Work Object ID reference** — extracts domain/consequence from referenced WO frontmatter, routes to governance conductor for lifecycle operations
2. **Explicit skill name mention** — e.g., "run alawas-production-operate-blender"
3. **COMP reference (COMP-042 through COMP-047)** → maps to production/production-plan-scene
4. **Domain-specific keywords** — "render," "implement," "pricing," etc.
5. **No signal** → triggers LLM fallback classification

**Compound request handling (OQ7 resolution):** When multiple WOs referenced, highest consequence dominates. WO ID present with other domain signals routes to governance conductor for lifecycle authority.

## Fallback logging

When `route_request()` determines no deterministic signal exists (`needs_llm_fallback=True`), this skill reasons directly about the best-fit domain and logs:

```json
{
  "request": "<user input>",
  "reasoned_domain": "production",
  "reasoned_skill": "production-operate-blender",
  "rationale": "Request mentions lighting, shots, render preview — all production signals",
  "timestamp": "2026-08-25T21:35:00Z"
}
```

This creates evidence for extracting new deterministic rules later (Decision 2's requirement).

## Inputs and preconditions

**Required input:** the natural-language request text to classify.

**Preconditions:** `runtime/orchestrator.py` is importable with all Step 4 features implemented (consequence handling, compound requests, priority ordering).

## Outputs

Returns a `RoutingDecision` object containing:
- `domain`: Target domain or null if unresolved
- `skill`: Full skill path (e.g., "production-operate-blender") or null for informational queries
- `consequence`: WO consequence level or default "low"
- `signal_used`: How routing was determined ("wo_id", "keyword", "none", etc.)
- `confidence`: Routing confidence level ("high", "medium", "low")
- `needs_llm_fallback`: True if session model reasoning required
- `compound_handled`: True if compound request resolved via WO ID dominance
- `routing_note`: Human-readable explanation of routing choice

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read `skills/core/` directory names and Work Object
  frontmatter via `route_request()`.
- `structured_output` — report the `RoutingDecision` fields plainly.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

Per WO `2026-08-25-003` and `references/CONSEQUENCE-AUTHORITY.md`:

**Default consequence:** "low" for requests without WO reference (assessed at WO creation time by downstream components).

**WO-referenced:** Reads current frontmatter at routing time, never caches stale values. If a referenced WO has `consequence: high`, applies appropriate gating before routing.

**Authority gates:** Downstream components enforce their own authority checks independently; orchestrator does not pre-screen consequences for requests without explicit WO reference.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate only when
the routing choice could send consequential work to the wrong owner, hide a
compound request, or bypass a Work Object authority boundary.

## Skill Grilling Profile

Apply the `alawas-orchestrate` profile in `references/SKILL-AWARE-GRILLING.md`.
Challenge signal precedence, compound request handling, fallback rationale,
and whether routing remains return-only instead of executing target skills.

## Workflow (default entry point mode)

1. **Receive request** → Platform adapter passes message to this skill
2. **Call route_request()** → Extract signals in priority order
3. **Return RoutingDecision** → Pass decision object back to platform adapter
4. **Platform adapter invokes** → Handles skill invocation with cycle detection and sequencing

Example: User says "update WO 2026-08-25-003 and render preview"
- Skill extracts WO ID, reads frontmatter (domain: engineering, consequence: meaningful)
- Detects compound request with production keyword ("render")
- Routes to governance conductor for lifecycle authority (WO ID dominates)
- Returns decision object to platform adapter

## History

<!-- Append-only chronological record of state transitions -->

### 2026-08-25T20:01:56Z — Activated for design; routing to pressure-test-decision

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director requested general orchestrator for cross-domain dispatch. Existing dispatch layer and governance conductor are components but neither serves as a general entry point. Key design decisions needed before implementation plan can be produced.

### 2026-08-25T21:35:12Z — Step 4 complete; promoted to default entry point (Step 5)

- **State:** verify → ready for deployment
- **Status:** active
- **Actor:** system
- **Rationale:** All Step 4 work completed with comprehensive test coverage. Step 5 promotion implemented: skill now serves as default entry point through platform adapter layer. Open questions 7-9 resolved (compound handling, priority ordering, return-only pattern documented). Remaining: implement platform adapter invocation logic when needed.

## Related deliverables

- [General orchestrator plan](../../deliverables/2026-08-25-003-general-orchestrator-plan.md) — Original design
- [Platform adapter spec (OQ9)](../../deliverables/2026-08-25-003-platform-adapter-return-only-spec.md) — Return-only invocation pattern

## Related Work Objects

- `2026-08-25-001` — Agent-type dispatch layer (predecessor architecture)
- `2026-08-25-002` — Multi-agent proposal evaluation (rejected, consumed by this design)
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (low).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: low`.
The platform overlay resolves this to `claude-haiku-3-5-20241022`.
The prompt budget for this tier is approximately 15000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `structured_output` | `—` | native |
