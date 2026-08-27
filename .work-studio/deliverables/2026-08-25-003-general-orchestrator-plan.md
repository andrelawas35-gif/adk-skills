# General orchestrator plan

**Work Object:** `2026-08-25-003` — Build general orchestrator for cross-domain task dispatch
**Deliverable type:** plan — synthesis only. Every claim below is attributed to a specific Decision (1–5, all recorded on this Work Object) or to predecessor Work Objects. This document authors **no new architecture, no new decisions, and no invented steps.**
**Produced:** 2026-08-25

---

## A. What exists today

`[system]` Three independent orchestration components handle different domains:

1. **`conduct-work-object`** (governance) — classifies signals, creates/transitions Work Objects, routes to specialist skills (`pressure-test-decision`, `design-tracer-bullet`, `implement-bounded-change`, `verify-release-evidence`), enforces consequence gates per `CONSEQUENCE-AUTHORITY.md`. Domain-scoped to governance lifecycle.

2. **`AgentResolver` + `AgentAdapter`** (agent dispatch, `runtime/agents.py`) — matches `required_type` + `required_capabilities` to registered adapters, dispatches to external AI agents via subprocess. One working adapter (`CodexAgentAdapter`, read-only). Provider-neutral. No concept of Work Objects, domains, or consequence. (WO `2026-08-25-001`, 13 Decisions)

3. **Production skills** (COMP-042 through COMP-047) — 3-layer architecture: Tool Operators (Blender, planned ComfyUI/TTS), Creative Reasoning (Scene Planner, Blocking Composition), Evaluation (Visual Critic). Invoked directly by name from the conductor or director. Domain-scoped to production. (WO `2026-08-23-001`)

`[system]` The skill directory (`skills/core/`) contains **49 skills across 8 domain prefixes**: business (15), design (11), engineering (2), governance (4), operations (2), production (4), research (2), thinking (9). All skill directories are prefixed by domain name.

`[gap]` No cross-domain routing exists. A request must be manually directed to the right skill or domain. There is no single entry point.

## B. What the orchestrator is

`[decision]` **Decision 1:** A new top-level component that sits above both `conduct-work-object` and `AgentResolver`. It is a thin routing layer — it classifies intent, picks the domain, and delegates to the right existing component. Each existing component keeps its current role unchanged. The orchestrator is additive and reversible — removing it leaves everything else intact.

What the orchestrator is NOT (per Decision 1 alternatives, and WO `2026-08-25-001` Decision 2):
- Not an extension of `conduct-work-object` (would conflate governance with execution)
- Not an extension of `AgentResolver` (would conflate subprocess dispatch with in-process skill routing)
- Not an agent marketplace, scoring router, or autonomous hierarchy

## C. How routing works

`[decision]` **Decision 2:** Hybrid — deterministic matching first, LLM classification fallback.

**Deterministic path** (zero LLM overhead, fires for most requests):
- **WO ID pattern** (`2026-08-XX-NNN`) → read WO frontmatter `domain` field → route to that domain
- **Skill name** (e.g., `conduct-work-object`, `operate-blender`) → extract domain from prefix
- **COMP reference** (`COMP-042`, etc.) → map to production domain
- **Domain keywords** (recognizable terms like "render", "implement", "pricing") → map to domain + candidate skill

**LLM fallback** (fires only for genuinely ambiguous requests with no structured signal):
- Sends request to a model with available domains/skills as context
- Returns structured routing decision
- Every fallback is logged for review — creates training data for new deterministic rules

**Priority order for mixed signals:** Not yet decided (open question 8). Default heuristic: WO reference takes priority (the WO's own domain field is authoritative) over keyword matching.

## D. How authority works

`[decision]` **Decision 3:** The orchestrator inherits consequence from the routed Work Object — no independent assessment.

- If the request references a WO, read its `consequence` field at routing time. Apply the matching gate from `CONSEQUENCE-AUTHORITY.md` before routing ("this WO is high-consequence — confirm before I route?").
- If no WO exists, default to "low." Downstream components run their own consequence assessment at WO creation time.
- The orchestrator never duplicates consequence logic — it reads an existing field, not re-derives it.
- Downstream components must continue to enforce their own gates independently (the orchestrator's "low" default for WO-less requests is only safe if no component assumes pre-screening happened).

## E. How you call it

`[decision]` **Decision 4:** Starts as an explicit skill (`/orchestrate <request>` or equivalent), promoted to default entry point after routing reliability is proven.

- **Phase 1 (tracer):** Explicit invocation only. The orchestrator is a skill like any other (`skills/core/orchestrate/SKILL.md`), loaded by the platform adapter. Users call it when they want cross-domain routing.
- **Phase 2 (after evidence):** Every message without a `/skill` prefix goes through the orchestrator first. The orchestrator either routes it or responds directly for conversational requests.
- **Promotion gate:** Reliable routing across at least 2 domains demonstrated via the tracer and subsequent real usage.
- **Both invocation paths coexist during Phase 1:** `/orchestrate <request>` (routed) and `/alawas-*` (direct skill invocation). Users can always bypass the orchestrator for familiar tasks.

## F. Tracer bullet

`[decision]` **Decision 5:** Dry-run deterministic routing function with 6 test cases.

**Scope:** `route_request(request_text: str) -> RoutingDecision` in `runtime/orchestrator.py`. Deterministic path only — no LLM fallback, no skill invocation, no authority forwarding.

**`RoutingDecision` schema:**
```python
class RoutingDecision(BaseModel):
    domain: Optional[str]           # e.g. "production", "governance", "business"
    skill: Optional[str]            # e.g. "production-operate-blender"
    consequence: Optional[str]      # from WO frontmatter if available
    signal_used: str                # "wo_id", "skill_name", "comp_ref", "keyword", "none"
    confidence: str                 # "high", "medium", "low"
    needs_llm_fallback: bool        # True when no deterministic signal found
```

**Test cases:**

| # | Input | Expected signal | Expected domain | Expected skill |
|---|-------|-----------------|-----------------|----------------|
| 1 | "transition WO 2026-08-24-014 to verify" | wo_id | production (from WO frontmatter) | conduct-work-object |
| 2 | "render a preview for shot 14" | keyword | production | production-operate-blender |
| 3 | "implement the scene planner tracer" | keyword | engineering | engineering-implement-bounded-change |
| 4 | "what's the status of COMP-042?" | comp_ref | production | None |
| 5 | "help me with pricing strategy" | keyword | business | business-design-pricing-and-packaging |
| 6 | "make the lighting more dramatic" | none | None | None (needs_llm_fallback=True) |

**Files:** `runtime/orchestrator.py`, `tests/test_orchestrator_routing.py`

**Exit criteria:** All 6 pass. Cases 1-5 via deterministic path. Case 6 correctly flags fallback.

## G. What to build and in what order

`[inference]` Sequencing derived from Decisions 1-5's own dependencies:

**Step 1 — Tracer bullet** (Decision 5)
- Implement `runtime/orchestrator.py` with `RoutingDecision` model and `route_request` function
- Implement `tests/test_orchestrator_routing.py` with 6 test cases
- Prove deterministic routing works against real WO frontmatter reads and skill directory structure
- Route to `implement-bounded-change`

**Step 2 — Skill shell** (Decision 4)
- Create `skills/core/orchestrate/SKILL.md` — the orchestrator as an invokable skill
- Wire `route_request` into the skill body: receive request → route → return routing instruction
- Decide how skill-invoking-skill nesting works at the platform adapter level (open question 9)
- Test with real requests across at least 2 domains

**Step 3 — LLM fallback** (Decision 2, resolved by Decision 6) — **done**
- `[decision]` Decision 6 resolved open question 6: no separate model dispatch is needed. `orchestrate` is a skill (Decision 4), loaded directly into the invoking session's model — when `route_request()` returns `needs_llm_fallback=True`, that same model reasons directly against the 8-domain skill list rather than a dedicated classifier being dispatched.
- Wired into `skills/core/orchestrate/SKILL.md`: reasoning instructions replace the "not built yet" stop condition.
- Every fallback decision is logged to `runtime/traces/orchestrator_fallback_log.jsonl` (`request`, `reasoned_domain`, `reasoned_skill`, `rationale`, `confidence`, `timestamp`).
- Demonstrated against two cases the tracer originally could not resolve: "audit the accessibility of the dashboard" → design/design-audit-accessibility (high confidence) and "make the lighting more dramatic" → production/production-plan-scene (medium confidence, correctly flagged as ambiguous rather than auto-routed).

**Step 4 — Consequence integration** (Decision 3)
- Wire WO frontmatter reads into routing for consequence-level gating
- Verify downstream components enforce gates independently
- Test mixed-consequence scenarios

**Step 5 — Promotion evaluation** (Decision 4)
- Review routing accuracy across real usage
- Decide whether to promote to default entry point
- If promoted: wire platform adapter to route all non-`/skill` messages through orchestrator

## H. What NOT to build

`[decision]` Per Decisions 1-5 and predecessor WOs:

- No autonomous agent hierarchy or agent-to-agent protocols (WO `2026-08-25-001` Decision 2)
- No scoring/AI-routing resolver (WO `2026-08-25-001` Decision 8)
- No multi-agent proposal as-written (WO `2026-08-25-002` Decision 1)
- No token-budget enforcement (identified as gap, separate concern)
- No LLM fallback in the tracer bullet (Step 3, after deterministic path is proven)
- No skill invocation in the tracer (Step 2, after routing accuracy is proven)
- No authority forwarding mechanism (Decision 3: inherit, don't forward)

## I. Open questions carried into implementation

| # | Question | Blocks |
|---|----------|--------|
| ~~6~~ | ~~LLM fallback model choice~~ | **Resolved — Decision 6: no dispatch needed, invoking model reasons directly** |
| 7 | Compound multi-domain requests (sequence, split, or reject) | Step 4 |
| 8 | Deterministic matcher priority order for mixed signals | Resolved in practice by Decision 5's precedence order (WO ID > skill name > COMP ref > keyword); not yet formally re-decided for conflicting multi-signal cases |
| 9 | Skill-invoking-skill nesting at platform adapter level | Step 5 (promotion to default entry point) |

## J. Predecessor context

This plan consumes and builds on:
- **WO `2026-08-25-001`** (13 Decisions): Agent-type dispatch layer contracts (`AgentRequest`/`AgentResult`/`AgentAdapter`/`AgentResolver`/`CodexAgentAdapter`). The orchestrator delegates to `AgentResolver` for agent-type dispatch; it does not replace or modify these contracts.
- **WO `2026-08-25-002`** (Decision 1): The multi-agent proposal's execution-model ideas (progressive disclosure, token budgets, local-model orchestration) are future inputs that consume existing skills, not replacements. The orchestrator is the consumption layer the proposal describes.
- **Schema reconciliation** (session 2026-08-25): Authority model mapping (`AuthorityEnvelope` vs `may_modify`/`may_not_modify`), token-budget gap, progressive-disclosure gap. These inform future decisions but are not resolved in this plan.

---

## Provenance summary

Every claim traces to Decisions 1-5 on `2026-08-25-003`, predecessor Work Objects (`2026-08-25-001`, `2026-08-25-002`, `2026-08-23-001`), or a direct read of `runtime/agents.py` and `skills/core/`. The implementation sequence (Section G) is `[inference]` — derived from the decisions' own dependencies, not a new architecture. Open questions are named explicitly (Section I), not papered over.
