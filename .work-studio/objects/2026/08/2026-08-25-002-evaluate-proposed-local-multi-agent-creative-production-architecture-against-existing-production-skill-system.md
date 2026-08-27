---
schema_version: 1
id: 2026-08-25-002
title: Evaluate proposed local multi-agent creative production architecture against existing production skill system
type: inquiry
status: active
state: design
consequence: meaningful
sensitivity: ordinary
domain: [production, governance]
created_at: 2026-08-25T19:51:27Z
updated_at: 2026-08-25T19:56:09Z
next_action: Evaluation complete. Token-budget/compaction ideas may warrant a separate Work Object; animation capability gap noted for future design.


---
## Intent

Evaluate a proposed "Local Multi-Agent Creative Production Architecture" (20-section
document proposing a Qwen3.5 9B orchestrator, 6 specialist agents, progressive
disclosure, Pydantic schemas, authority enforcement, and a 6-week phased
implementation) against the existing production skill system (COMP-042 through
COMP-047, 3-layer architecture, `runtime/agents.py` dispatch layer). Determine
whether the proposal replaces, supplements, or consumes the existing system, and
record the decision with enough context that future work can proceed without
replaying the evaluation.

## Success evidence

- [x] Proposal mapped against existing production skills with provenance tags
- [x] Each proposed agent matched to its existing skill equivalent (or gap identified)
- [x] Schema differences between proposal and `runtime/agents.py` contracts surfaced
- [x] Decision recorded: relationship between proposal and existing system
- [ ] Token-budget/compaction ideas from proposal evaluated for standalone value (deferred)

## Constraints and non-goals

**Constraints:**
- Evaluation only — no implementation of the proposal or modification of existing skills
- Decision must be evidence-backed against the actual codebase, not the proposal's claims
- Existing production skills (COMP-042 through COMP-047) and `runtime/agents.py` are the ground truth

**Non-goals:**
- Not implementing the proposed architecture
- Not designing a migration path from existing to proposed
- Not evaluating Qwen3.5 9B model suitability (separate concern, WO 2026-08-23-002 Decision 9)
- Not reconciling schemas between proposal and `runtime/agents.py` (future work if needed)

## Decisions and revisit triggers

### Decision 1 — Treat proposal as future execution-model description consuming existing skills, not a replacement

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Relationship between the 20-section "Local Multi-Agent Creative Production Architecture" proposal and the existing production skill system (COMP-042 through COMP-047, `runtime/agents.py`, 3-layer architecture from WO 2026-08-23-001). |
| **Authorization** | Director explicitly accepted: "accept this recommendation" in response to Branch B recommendation from pressure test. |
| **Confidence** | Medium-high for the core relationship claim (5 of 6 proposed agents directly duplicate existing skills, verified by file reads); medium for schema reconciliation cost (proposal schemas are unimplemented, so real integration cost is unknown). |
| **Actor** | Director (acceptance), alawas-thinking-pressure-test-decision (recommendation) |
| **Revisit trigger** | (1) If existing production skills turn out to be structurally incompatible with local-model orchestration — i.e., they require frontier-model reasoning and cannot function under Qwen3.5 9B or equivalent local models. (2) If the proposal targets a genuinely different runtime environment not served by the existing `runtime/agents.py` dispatch layer. (3) If token-budget/compaction ideas from the proposal prove essential and cannot be added incrementally to the existing architecture. |
| **Rationale** | [inference] Evidence-backed mapping shows 5 of 6 proposed agents directly duplicate existing skills: Layout Agent = COMP-045 Scene Planner + COMP-046 Blocking Composition, Critic Agent = COMP-047 Visual Critic, Blender Operator = COMP-042 Blender Operator. The existing system already has a provider-neutral dispatch layer (`runtime/agents.py` with `AgentAdapter` Protocol, `AgentResolver`, `AgentRequest`/`AgentResult`), a 3-layer architecture (Tool Operators / Creative Reasoning / Evaluation), and authority enforcement via `protect` fields and consequence gates. The proposal's schemas (`may_modify`/`may_not_modify`/`requires_approval_for`) are unreconciled with the existing `AuthorityEnvelope` (`inspect`/`modify_code`/`deploy`) and would require schema reconciliation before any integration. Branch B preserves all existing verified work while allowing the proposal's execution-model ideas (progressive disclosure, token budgets, local-model orchestration) to be evaluated as consumers of the existing skills rather than replacements. |

**Alternatives considered:**
- **Branch A — Accept proposal as-is and rebuild:** Rejected. Would discard verified, tested production skills (COMP-042 in verify state with live Blender smoke test, COMP-045 with 3/3 tracer tests passing) and the `runtime/agents.py` dispatch layer (13 accepted Decisions on WO 2026-08-25-001). No evidence that rebuilding produces better results.
- **Branch C — Reject proposal entirely:** Rejected. The proposal contains genuinely useful ideas (token-budget management, progressive disclosure, compaction strategy) that have no equivalent in the existing architecture and should not be lost.

**Trade-offs accepted:**
- Token-budget/compaction ideas from the proposal risk being lost if not separately evaluated. The proposal's context-management strategy (orchestrator under 8K, agents under their budgets) addresses a real concern not yet handled by the existing architecture.
- Schema reconciliation between proposal's authority model and existing `AuthorityEnvelope` is deferred — real cost is unknown until someone attempts integration.
- The proposal's 6-week phased implementation plan is abandoned as written. Any future implementation would follow the existing Work Object lifecycle, not the proposal's timeline.

**Edge cases noted:**
- The proposal's "Animation Agent" (8-12K token context, character motion and timing) has no direct equivalent in the existing system — it is a genuine gap, not a duplication. If animation work proceeds, this is new capability to design, not an existing skill to consume.
- Local-model compatibility is untested. The existing skills were designed for frontier-model reasoning (Claude/Codex/Copilot). Whether Qwen3.5 9B can drive Scene Planner or Visual Critic effectively is an open question outside this decision's scope.

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | File reads: COMP-042, COMP-045, COMP-046, COMP-047 WOs | 5 of 6 proposed agents map to existing production skills. Layout Agent = COMP-045 (Scene Planner, state: verify) + COMP-046 (Blocking Composition, state: design). Critic Agent = COMP-047 (Visual Critic, state: design). Blender Operator = COMP-042 (Blender Operator, state: verify, live smoke test passed). Research Agent maps loosely to existing `alawas-research-investigate-live-question` skill. Visual Dev Agent has no direct equivalent but overlaps with ComfyUI operator (planned). |
| [system] | File read: `runtime/agents.py` | Existing dispatch layer: `AgentRequest`, `AgentResult`, `AgentAdapter` (Protocol), `AgentResolver`, `CodexAgentAdapter`. Authority model: `AuthorityEnvelope` with `inspect`/`modify_code`/`deploy` booleans. Provider-neutral — any adapter implementing the Protocol can be registered. |
| [system] | File read: deliverable `2026-08-23-001-production-skill-architecture-implementation-plan.md` | Existing 3-layer architecture: Layer 1 (Tool Operators: Blender/ComfyUI/TTS — deterministic executors), Layer 2 (Creative reasoning: Scene Planner/Blocking Composition — LLM reasoning), Layer 3 (Evaluation: Visual Critic — vision model feedback). |
| [inference] | Provenance sorting of proposal claims | Proposal's authority model (`may_modify`/`may_not_modify`/`requires_approval_for` per-agent) is structurally different from existing `AuthorityEnvelope` (`inspect`/`modify_code`/`deploy` per-request). Both enforce boundaries but at different granularities and with different field sets. Reconciliation cost is real but unknown. |
| [gap] | Proposal sections 5, 9 | Token-budget management (orchestrator under 8K, agents under per-agent budgets) and compaction strategy (progressive context reduction) have no equivalent in the existing architecture. These are genuinely novel ideas worth separate evaluation. |
| [gap] | Proposal section 1 | Animation Agent (character motion, timing, action blocking, 8-12K context) has no existing skill equivalent. This is a genuine capability gap in the current system. |
| [decision] | Director acceptance, 2026-08-25 | Director accepted Branch B recommendation from pressure test: "accept this recommendation." Branch B treats the proposal as a future execution-model description that consumes existing production skills, not a replacement for them. |

## Open questions

- Should token-budget/compaction ideas from the proposal be evaluated as a standalone Work Object? They address a real concern (context management for local models) not handled by existing architecture.
- When animation capability is needed, should it follow the existing 3-layer pattern (new COMP for animation) or the proposal's agent-shaped design?

## Next move

Route to `alawas-governance-conduct-work-object` to record the decision and close the pressure-test workflow. No further decisions needed at this stage — the evaluation is complete.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T19:51:45Z — Activated and advanced to design

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Proposal received for evaluation; pressure test completed with Branch B accepted (treat proposal as future execution-model input that consumes existing production skills, not a replacement). Decision ready to record.
### 2026-08-25T19:56:09Z — Decision 1 recorded: treat proposal as future execution-model consuming existing skills

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** [decision] Director accepted Branch B from pressure test. 5 of 6 proposed agents duplicate existing production skills (COMP-042 through COMP-047). Proposal's execution-model ideas (progressive disclosure, token budgets, local-model orchestration) preserved as future input, not a replacement. Evidence ledger, alternatives, trade-offs, edge cases, and revisit triggers recorded on the Work Object.
