# Phase 7 Recovery Uses Node Granularity, Not a Dedicated Subgraph

- **Status:** Accepted
- **Date:** 2026-08-17
- **Component:** `runtime/graph.py` (Phase 7, not yet built)
- **Decision owners:** Human-approved (director, 2026-08-17; develop-idea → pressure-test-decision)
- **Related Work Object:** `2026-08-17-015` — Phase 7: retry, compensation, and director gates
- **Related ADRs:**
  - depends on: ADR 0025 (canonical/runtime truth boundary — compensation here never means undoing a canonical write, since the runtime never makes one)
  - complements: none yet — first Phase 7 ADR
  - constrains: any future Phase 7/8 ADR proposing recovery-path graph structure
- **Supersedes:** None
- **Superseded by:** None

## Context

`references/architecture/langgraph-local-runtime-integrated-build-plan.md` (line 366) names a "recovery subgraph" as one of Phase 7's required pieces, alongside error classes, bounded retry policies, timeouts, an effect journal, and interrupts for four director-gate types (direction, restricted handling, high consequence, release authority).

`develop-idea` generated four directions for how these pieces compose: node-level retry/timeout as native configuration (Direction 1), a dedicated compiled recovery subgraph taking the plan's wording literally (Direction 2), an effect-journal-first approach extending Phase 4's idempotency table (Direction 3), and a generalized director-gate extending the already-working `research_gate_fetch` interrupt pattern (Direction 4).

Directions 1, 3, and 4 cover distinct, non-overlapping parts of Phase 7's scope and compose without conflict. Direction 2 was the only expensive one, and its necessity was untested until this decision.

## Decision

Phase 7 does **not** build a standalone compiled recovery subgraph. It composes:

1. **Direction 1** — langgraph's native `retry_policy` and `timeout`, attached directly via `StateGraph.add_node(..., retry_policy=..., timeout=...)`.
2. **Direction 3** — an effect journal, extending the existing `claim_idempotency_receipt` SQLite table (`runtime/graph.py:221-256`) with status and attempt-count tracking.
3. **Direction 4** — a generalized `authority_gate(reason)` node, extracted from the already-working `research_gate_fetch` `interrupt()`/`Command(resume=True)` pattern (`runtime/graph.py:788-796`), parameterized for all four gate types.

One additional constraint, surfaced by testing a concrete scenario, is part of this decision: **any node performing more than one external effect must be decomposed into one graph node per effect**, not bundled inside a single function body. Cross-node compensation — cleaning up an earlier node's effect because a later one failed — is handled by an ordinary node reached via `add_conditional_edges` within the *same* graph, consulting the effect journal to see what already completed. No second compiled graph and no second checkpointed thread are introduced.

## Scope

This decision applies to:

- How Phase 7 nodes are structured in `runtime/graph.py` (and any future Phase 8 nodes)
- Any node in the runtime performing more than one external effect
- Compensation/rollback logic for a multi-node sequence

This decision does not apply to:

- Whether a `RetryableError`/`TerminalError`/`AuthorityRequiredError` exception hierarchy is warranted (a smaller, separate design question)
- The effect journal's exact schema (deferred to design)
- The `authority_gate` node's exact signature (deferred to design)
- Phase 8 production packaging

## Rationale

The scenario tested was the sharpest available: a node that fetches external content, then writes a derived artifact, where the fetch succeeds and the write exhausts its retries. If both effects are bundled in one function body, the node raises before returning any state update — the graph checkpoint never learns the fetch happened, only the real world does. This is a genuine gap, but it is a **node-granularity** gap, not a **graph-topology** gap: splitting fetch and write into two separate nodes connected by a plain edge means fetch's result is checkpointed the moment it completes, so write's `error_handler` — confirmed via direct source inspection (`inspect.getsource(StateGraph.add_node)`) to be a real auto-wired fallback node with full access to graph state — can see exactly what happened and act on it.

A standalone recovery subgraph would not have closed this gap either; the failure mode is about when state becomes checkpoint-visible, which is a property of node boundaries, not of how many compiled graphs exist. Building one would mean re-solving, at higher cost, a problem the library already solves natively.

## Alternatives Considered

### Direction 2 as originally scoped — dedicated compiled recovery subgraph

A separate `build_recovery_graph()`, mirroring Phase 6's dispatch/branch/join shape, that a failed node's error handler routes into.

Rejected because the concrete scenario tested showed the actual blocker (orphaned sub-effects on mid-node failure) is solved by node granularity, not graph topology. A second compiled graph adds a second thing to crash-test and keep synchronized with Phase 6's pattern, for a job `error_handler` and `add_conditional_edges` — both confirmed present in the installed langgraph 1.2.11 API — already do inside the same graph.

### Defer the choice until compensation semantics are fully pinned down

Keep Direction 2 as a fallback, build only if a future case proves `error_handler` insufficient.

Superseded, not rejected outright — the deferred question ("does compensation ever need real orchestration?") was answered directly by testing a scenario rather than left open. If a future case genuinely needs more than a conditional-edge compensating node, this ADR's revisit trigger covers it.

## Consequences

### Positive

- Every piece of Phase 7's composition (native retry/timeout/error_handler, effect journal, generalized gate) has direct precedent already proven in this codebase or the installed library — nothing here is unbuilt territory
- No second compiled graph, no second checkpointed thread, no new crash-test surface beyond what Phase 6 already established
- The node-granularity constraint is a design rule applicable to all future nodes, not just Phase 7's

### Negative

- Deviates from the build plan's literal "recovery subgraph" wording (line 366) — a future reader checking the plan against the code would find no such subgraph and needs this ADR to understand why
- The node-granularity constraint is a discipline, not an enforced mechanism yet — nothing currently stops a future node author from bundling multiple effects in one function body
- The three composed pieces have not been run together end to end; first genuine integration risk is deferred to design/build

### New obligations

- Phase 7 design work should record the node-granularity constraint explicitly in any new node's design (per this ADR), not rely on this ADR being independently rediscovered
- `references/architecture/langgraph-local-runtime-integrated-build-plan.md` should eventually note this deviation from its Phase 7 line, so the plan and the ADR do not silently diverge (not required before Phase 7 build begins)

### Risks

- A future node author bundles multiple effects in one function body anyway, reintroducing the orphaned-sub-effect gap this ADR closed by convention, not enforcement. Mitigation: the revisit trigger below covers a lint/check for this if it recurs in practice.
- The three-piece composition, once built, may reveal an integration problem none of the individually-proven pieces predicted. Mitigation: this is exactly what Phase 7's own tracer/exit-evidence testing (Hypothesis `RuleBasedStateMachine` sequences) is for.

## Enforcement

Current enforcement: none mechanical — no Phase 7 code exists yet.

Planned enforcement, when Phase 7 is built:

- Any node in `runtime/graph.py` performing more than one external effect (network call, file write, subprocess) is flagged in review against this ADR's node-granularity constraint
- Cross-node compensation logic uses `add_conditional_edges` to an ordinary node within the same graph, never a second `StateGraph`/`build_*_graph()` function for recovery purposes

## Validation

- No Phase 7 node function performs two or more external effects without an intervening node boundary
- No second compiled graph or second checkpointed thread exists solely for recovery/compensation purposes
- `error_handler` and `add_conditional_edges` usage in Phase 7 code is traceable to this ADR's rationale

## Migration

None. No code changes are required by this ADR on its own — it constrains Phase 7 code that does not yet exist.

## Revisit Triggers

Revisit this ADR when:

- Phase 7 design or build finds a compensation case that `error_handler` plus a conditional-edge compensating node genuinely cannot express
- The three-piece composition (native retry/timeout/error_handler, effect journal, generalized gate) fails an end-to-end integration test once built
- The node-granularity constraint proves unenforceable in practice and needs a mechanical check rather than convention
- A future runtime effect is not read-only and genuinely needs multi-step undo logic beyond what a single compensating node can express

## Evidence

### Observed

- `references/architecture/langgraph-local-runtime-integrated-build-plan.md:366-370` — Phase 7's stated scope, including "recovery subgraph"
- `runtime/graph.py:221-256` (`claim_idempotency_receipt`) — existing effect-journal precedent
- `runtime/graph.py:466-489` (`Phase6Crash`/`_phase6_crash_hook`) — existing crash-injection test convention
- `runtime/graph.py:788-796` (`research_gate_fetch`) — existing `interrupt()`/`Command(resume=True)` director-gate precedent
- `.venv/bin/python3 -c "from langgraph.types import RetryPolicy; ..."` — confirmed `RetryPolicy` fields directly
- `.venv/bin/python3 -c "... inspect.signature(StateGraph.add_node)"` — confirmed `retry_policy`, `timeout`, `error_handler` as native `add_node` kwargs
- `.venv/bin/python3 -c "... inspect.getsource(StateGraph.add_node)"` — confirmed `error_handler` is wired as an auto-generated `__error_handler__{node}` node with the same input schema, connected as the fallback destination after retries exhaust
- `.venv/bin/python3 -c "... inspect.signature(StateGraph.add_conditional_edges)"` — confirmed the method exists in the installed langgraph 1.2.11
- `grep -n "add_conditional_edges" runtime/graph.py` — zero matches; this runtime has never used conditional routing before Phase 7

### Inferred

- Node granularity (one effect per node), not graph topology (one subgraph vs. many), is the property that determines whether a mid-sequence failure leaves an orphaned, untracked effect. This is an inference drawn from walking the bundled-node vs. separate-node cases against the same scenario, not a directly observed fact about langgraph's internals beyond what the two `inspect` calls confirmed.
- The three composed pieces (retry/timeout/error_handler, effect journal, generalized gate) will integrate cleanly. Not yet tested end to end — flagged explicitly as the main residual risk.

### Decided

- Director, 2026-08-17 (Work Object `2026-08-17-015`, Decision recorded 2026-08-17T11:05:00Z): Branch B selected — compose Directions 1, 3, and 4; no dedicated recovery subgraph; node-granularity constraint added after testing a concrete fetch-then-write compensation scenario.
