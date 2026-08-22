# Routing / handoff system audit

Report-type deliverable for Work Object `2026-08-22-009`. Grounded in the
real code (`runtime/handoff.py`, `runtime/graph.py`, the conductor's
`SKILL.md` routing table, `tools/ws/validate.py`) and one executed test run.
No architecture is authored here — improvements are surfaced as findings, not
decisions.

## The system has two distinct routing layers

`[system]` **Layer 1 — skill-level routing (authoritative).** The conductor's
8-row `state -> skill` table in
`skills/core/governance-conduct-work-object/SKILL.md` (`### 6. Route to
specialist`), plus each skill's own `## Routing and termination` section, is
the routing that actually happens — executed by a human or agent moving a Work
Object between skills.

`[system]` **Layer 2 — runtime handoff (proposal-only mirror).**
`runtime/handoff.py` + `graph.py`'s Phase 6 dispatch/branch/join derive a
*proposed* next skill deterministically and record it on a `HandoffReceipt`,
but never execute a route. `WO 2026-08-21-006` already confirmed the runtime
never invokes a skill or an LLM. This layer is a read-only projection, not a
router.

Keeping these straight matters: "is the routing logic right?" has a different
answer per layer — Layer 1 is where routing *decisions* live; Layer 2 only
*mirrors* them.

## What is correct

`[system]` **The two routing tables are in sync.** Row-by-row comparison of
`runtime/handoff.py`'s `_STATE_ROUTING_TABLE` against the conductor's table:
identical across all 8 states.

`[system]` **The sync is guarded by a passing test.**
`test_state_routing_table_stays_in_sync_with_conductor`
(`runtime/tests/test_handoff_graph.py`) parses the conductor's SKILL.md table
and asserts the runtime copy matches. Executed during this audit: **PASS**.

`[system]` **The derivation logic is sound where it exists.**
`derive_proposal` defaults an unknown or empty state to `await-director` — a
safe deferral, not a silent wrong route. `merge_proposals` deduplicates and
sorts deterministically. The documented nuance that `explore` routes to
`develop-idea` (and reaches `investigate-live-question` only downstream, never
directly) is consistent between the runtime table and the conductor's note.

## Gaps and improvements

### G1 — `to_skill="specialist"` is an inert placeholder `[system]`

`phase6_dispatch` hardcodes `to_skill="specialist"` on the `HandoffEnvelope`.
The real proposal is computed later, per-branch, by `derive_proposal(state)`
on the `HandoffReceipt`. So the envelope's `to_skill` field carries no routing
meaning — it's a dead field a future consumer could mistake for a real target.
This is the clearest concrete improvement: either derive the real proposal at
dispatch too, or rename/document the field as a deliberate placeholder.
(Already known from `WO 2026-08-21-006`; restated here with its routing
consequence.)

### G2 — no `next_action` ↔ state routing consistency check `[gap]`

The conductor says routing is "Based on current state and next_action," but
the table is state-keyed and `next_action` is unconstrained free text.
`tools/ws/validate.py` has no check that a Work Object's `next_action` agrees
with its state's canonical route (it has an `incident-routing` successor
check, but nothing general). A `next_action` that contradicts the state's
route — e.g. state `build` but `next_action` pointing at
`design-tracer-bullet` — would pass validation silently. Potential improvement:
an advisory validator check, not a hard gate, since `next_action` legitimately
carries more specificity than the state alone.

### G3 — the drift-guard comment undersells its own protection `[system]`

`handoff.py:48-50` warns "no automatic sync exists." True for *sync*, but
misleading: there *is* automatic drift *detection* (G-above test). A
maintainer reading only the comment might over-trust manual vigilance or
duplicate the guard. One-line comment fix.

### G4 — mixed skill-reference naming in core files `[gap]`

Core `SKILL.md` files mix `alawas-`-prefixed and bare references (both
`alawas-governance-conduct-work-object` and `conduct-work-object` appear). The
generator's `namespace_skill_references` normalizes *backticked* references of
either form via aliases, so generated adapters are consistent — but
non-backticked prose references ship un-normalized. Low consequence
(readability, not routing logic); worth a lint if consistency is wanted.

## Scope note

This audit covered routing *logic* and *consistency*. It did not re-verify the
Phase 6 crash/resume matrix (two of those tests error on this platform for a
pre-existing SQLite/langgraph reason unrelated to routing) — that reliability
question is separate from whether the routing decisions are correct.

## Gaps carried forward

- G1–G4 are surfaced, not fixed. Each would need its own decision/tracer
  before any change.
- Whether Layer 2 (runtime) should ever drive real routing rather than only
  propose is already owned by `WO 2026-08-21-006` (answered: no) and
  `WO 2026-08-21-011` (MCP agency mode, in design) — out of scope here.
