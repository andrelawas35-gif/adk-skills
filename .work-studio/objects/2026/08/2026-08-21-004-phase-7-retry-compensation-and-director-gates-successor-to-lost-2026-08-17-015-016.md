---
schema_version: 1
id: 2026-08-21-004
title: Phase 7: retry, compensation, and director gates (successor to lost 2026-08-17-015/016)
type: project
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [engineering, architecture]
created_at: 2026-08-21T13:23:46Z
updated_at: 2026-08-21T13:41:10Z
next_action: Director decision needed: close this Work Object now with the Phase 8 blocker and the untested-rejection-path gap recorded as accepted open items, or route to implement-bounded-change once more for a small test proving Command(resume=False) against research_fetch_source never calls fetch_url















---
## Intent

Continue Phase 7 of `references/architecture/langgraph-local-runtime-integrated-build-plan.md`
(line 366: "Retry, compensation, and director gates") under the design already
decided in `docs/adr/0026-phase-7-recovery-uses-node-granularity-not-a-dedicated-subgraph.md`.
That ADR's Work Object (`2026-08-17-015`, successor `2026-08-17-016`) is not
present in `.work-studio/objects/` — Work Objects only began being tracked in
this repo's git history on 2026-08-21 (`.work-studio/config.md`), so anything
created before that date and not otherwise preserved is gone from this
checkout. This object is a successor created to carry Phase 7's continuity
forward from here, not a reconstruction of the lost objects' full history.

ADR 0026's decision (still binding, unchanged by this object): compose
langgraph's native `retry_policy`/`timeout`/`error_handler` (Direction 1), an
effect journal extending `claim_idempotency_receipt` (Direction 3), and a
generalized `authority_gate(reason)` node (Direction 4) — no dedicated
compiled recovery subgraph (Direction 2, rejected). Any node performing more
than one external effect must be decomposed into one node per effect.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `authority_gate(reason)` implemented and used for at least one gate type (`runtime/graph.py:914`, used at `:724` for direction approval, `:935` for research fetch)
- [x] `RetryPolicy` + `error_handler` wired on at least one multi-attempt node (`record_note`, `runtime/graph.py:1055-1061`)
- [ ] **Blocked, deferred to Phase 8.** All four director-gate types from the build plan (direction, restricted handling, high consequence, release authority) route through `authority_gate`. `direction` is wired (`runtime/graph.py:724`, Phase 6's `direction_gate` node). The other three have no real effect or code path to attach to yet: grep across `runtime/graph.py` for restricted/high_consequence/release turns up only the docstring naming them (`:920-922`) -- no node in the Phase 4, Phase 6, or research graphs does anything a restricted-content, high-consequence-creation, or release/deployment gate would sit in front of. Release/deployment concerns first become concrete in Phase 8 (`references/architecture/langgraph-local-runtime-integrated-build-plan.md:372`), which is unbuilt. The mechanism itself (`authority_gate(reason)`) is proven and reusable the moment a real call site exists -- this item is blocked on that call site existing, not on implementation effort. Director accepted deferring to Phase 8 rather than inventing a call site now.
- [x] Effect journal carries status + attempt tracking -- **corrected**: not via a SQLite schema change. `runtime/tests/test_phase7_tracer.py` (WO `2026-08-17-015` Decision 2) already proves status via distinct `effect_name` identities (`"risky_effect:succeeded"` vs `"risky_effect:failed"`, mirrored in real code by `record_note`'s `:failed` suffix) and attempt-count via a marker file (`_effect_attempt`, mirroring `_phase6_crash_hook`), not a table column -- deliberate, since langgraph re-invokes a retrying node with no state channel to carry a counter between attempts
- [x] Hypothesis `RuleBasedStateMachine` sequences (build plan's Phase 7 exit evidence) generate pause/resume/retry/reject/replay/compensate sequences without violating invariants -- `runtime/tests/test_phase7_hypothesis.py` implemented per Decision 2; `uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis -v` ran 3 tests, 92s, OK, zero found counterexamples across reject/approve/retry-succeed/retry-exhaust/replay sequences
- [x] Irreversible effects without authority confirmed unreachable -- **by code inspection, not an executed test (gap noted).** Phase 4 and Phase 6 have zero irreversible external effects today (Phase 6's branches/join are read-only by construction, ADR 0025). The research graph's one irreversible effect (`fetch_url`'s network GET) is enforced unreachable without approval via an in-node check in `research_fetch_source` (`runtime/graph.py:938-957`), not graph topology. No existing test empirically exercises `Command(resume=False)` against this path and asserts `fetch_url` was never called -- this item rests on `[inference]` from reading the code, not `[system]` evidence from running it


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->

**Non-goals:**
<!-- Explicitly excluded work. -->

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Inherit ADR 0026's composition decision as binding; do not re-litigate

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This object continues Phase 7 build under the composition already decided in `docs/adr/0026-phase-7-recovery-uses-node-granularity-not-a-dedicated-subgraph.md`: native retry/timeout/error_handler + effect journal + generalized authority_gate, no dedicated recovery subgraph, one-effect-per-node discipline |
| **Authorization** | Director, 2026-08-17 (recorded in ADR 0026, Work Object `2026-08-17-015`) — that authority carries forward; this object does not seek fresh authorization for the same decision |
| **Confidence** | high — ADR 0026 is Accepted status, backed by direct `inspect` calls against the installed langgraph API, not superseded |
| **Actor** | director (original), inherited by this successor object |
| **Revisit trigger** | Same as ADR 0026's: a compensation case `error_handler` + conditional-edge cannot express; the three-piece composition fails end-to-end integration once built; node-granularity proves unenforceable without a mechanical check; a runtime effect needs multi-step undo beyond one compensating node |
| **Rationale** | Re-deciding an already-Accepted ADR because its tracking Work Object was lost would be authority drift in the other direction — treating a bookkeeping gap as grounds to reopen a settled design question. The ADR is the durable record; this object's job is to give lost tracking a home, not to re-grill the decision. |

### Decision 2 — Accepted tracer bullet: Hypothesis RuleBasedStateMachine over the existing self-contained tracer graph

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add `hypothesis` as a test-only dependency (`pyproject.toml`); write one new self-contained test file, sibling to `runtime/tests/test_phase7_tracer.py`, defining a `RuleBasedStateMachine` that drives the existing unmodified 3-node tracer graph (`authority_gate -> risky_effect -> record_success`) through random sequences of approve/reject/retry-fail/retry-succeed/replay-after-terminal actions. Checks: journal never holds both `:succeeded` and `:failed` for one identity; a rejected gate produces zero journal entries; the effect never runs without prior approval; attempt count in the marker file never exceeds `max_attempts`. Does not wire the three missing real gate types, does not touch `record_note`/the research graph, does not add `hypothesis` as a production dependency. Rollback: delete the new test file, revert the one dependency line -- same shape as `test_phase7_tracer.py`'s own stated rollback. |
| **Authorization** | Director: "Accept, add hypothesis as a test-only dependency" |
| **Confidence** | high that the existing tracer graph mechanism (proven in `test_phase7_tracer.py`) is what's being modeled; medium on whether Hypothesis's generated sequences will surface anything `test_phase7_tracer.py`'s four hand-written cases didn't already cover -- that uncertainty is exactly what this tracer bullet exists to resolve |
| **Actor** | director |
| **Revisit trigger** | A found counterexample (real invariant gap, route to investigation before any gate wiring proceeds); or the RuleBasedStateMachine proves unable to express one of the six named action types (pause/resume/retry/reject/replay/compensate) against this graph shape, in which case the model -- not the graph -- needs redesign |
| **Rationale** | This item was originally mis-scoped in this Work Object as a SQLite schema change (Success evidence, corrected above) -- reading `test_phase7_tracer.py` in full showed status and attempt-count are already solved without a schema change. The one genuinely unbuilt piece is the Hypothesis exit-evidence suite the build plan itself names for Phase 7; no precedent for property-based testing exists anywhere in this repo, so it gets its own bounded tracer bullet rather than folding into implementation directly. |

### Decision 3 — Defer the three missing director-gate types (restricted, high consequence, release) to Phase 8

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This Success evidence item is blocked, not implemented and not attempted now. No node in the Phase 4, Phase 6, or research graphs performs any action a restricted-content, high-consequence-creation, or release/deployment gate would sit in front of; release/deployment concerns first become concrete in the build plan's Phase 8, which is unbuilt. The `authority_gate(reason)` mechanism itself is already proven (Decision 1's inherited composition, Decision 2's Hypothesis suite) and reusable the moment a real call site exists -- nothing about the mechanism blocks this, only the absence of a target. |
| **Authorization** | Director: "Treat it as blocked/deferred to Phase 8" |
| **Confidence** | high -- grep across `runtime/graph.py` for restricted/high_consequence/release and a read of every `add_node` call in all three real graphs found zero candidate call sites, not merely an unsearched gap |
| **Actor** | director |
| **Revisit trigger** | Phase 8 work begins, or any earlier Work Object introduces a real effect for restricted-content handling, high-consequence Work Object creation, or a release/deployment action -- at that point this item un-blocks and the already-proven `authority_gate` pattern applies directly |
| **Rationale** | Wiring three `authority_gate` calls with no real effect behind them would mean inventing call sites to satisfy a checklist item, not applying an already-accepted pattern -- exactly the kind of unauthorized product/architecture decision this skill's implementer must not make alone. Deferring keeps the Success evidence honest about what's actually blocked versus merely unimplemented. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | this session, grep/find across .work-studio/objects/, docs/adr/0026, git log --all --diff-filter=D | docs/adr/0026-phase-7-recovery-uses-node-granularity-not-a-dedicated-subgraph.md names 2026-08-17-015 as Phase 7's Work Object (Accepted status, director-decided 2026-08-17). runtime/graph.py references successor 2026-08-17-016. Neither file exists under .work-studio/objects/ -- only three 2026-08-21 objects are present. .work-studio/config.md states Work Objects began being tracked in this repo's git history on 2026-08-21, so anything created before that date and not otherwise preserved is gone from this checkout. git log --all --diff-filter=D shows no deletion of these paths, confirming they were never committed rather than removed. |
| [system] | this session, grep -n across runtime/graph.py | grep across runtime/graph.py confirms Phase 7 build already partly done: authority_gate(reason) at line 914, used at :724 (direction approval) and :935 (research fetch gate); RetryPolicy + error_handler wired on record_note (retry_policy at :1060, error_handler at :1061, _make_record_note_error_handler at :1020); claim_idempotency_receipt effect-journal function present since Phase 4/6 (originally at :257). Not yet confirmed: whether restricted-handling and high-consequence/release-authority gate types (the other two of the build plan's four) also route through authority_gate, or whether claim_idempotency_receipt tracks status/attempt-count beyond claim-before-effect -- both flagged as Open questions rather than assumed either way. |
| [system] | this session, grep -n authority_gate runtime/graph.py; Read runtime/graph.py:221-300 (claim_idempotency_receipt) | Both Open questions answered by direct read. (1) Gate coverage: grep -n 'authority_gate' runtime/graph.py shows only two call sites -- line 724 (direction approval) and line 935 (research-fetch gate). Of the build plan's four gate types (direction, restricted handling, high consequence, release authority), only 'direction' is clearly covered; research-fetch does not map cleanly to any of the other three. Restricted handling, high consequence, and release authority gates are not yet built. (2) Effect journal: claim_idempotency_receipt's SQLite schema (runtime/graph.py:274-280) is (thread_id, work_object_id, effect_name, created_at) with a PRIMARY KEY on the first three columns -- a claim-before-effect boolean receipt only, no status column and no attempt-count column. The 'status + attempt-count tracking' Success evidence item is confirmed not yet done, not just unverified. |
| [system] | this session, Read runtime/tests/test_phase7_tracer.py in full; grep -rln hypothesis runtime/; python3.13 -c import hypothesis; grep -n hypothesis pyproject.toml | Full read of runtime/tests/test_phase7_tracer.py (WO 2026-08-17-015 Decision 2, self-contained, rollback = delete file). Confirms status is already tracked via distinct effect_name identities in the existing idempotency_receipts table (risky_effect:succeeded vs risky_effect:failed), mirrored in real code by record_note's :failed suffix (runtime/graph.py:1032). Confirms attempt-count is already tracked via a marker file (_effect_attempt), not a SQLite column, deliberately -- langgraph re-invokes a retrying node with no state channel to carry a counter between failed attempts. Four passing-shaped test cases exercise gate-reject/no-effect, retry-then-succeed, retries-exhausted, and journal-replay-idempotency. Docstring explicitly states it does not wire into the real Phase 6/research graphs and does not implement all four gate types. Separately confirmed: hypothesis is not installed (ModuleNotFoundError in the repo's python), not declared in pyproject.toml's dependencies, and no RuleBasedStateMachine/hypothesis usage exists anywhere in the repo -- that Success evidence item is genuinely unbuilt, unlike the schema item. |
| [system] | this session: uv sync --group test; uv run --group test python -m unittest runtime.tests.test_phase7_tracer -v; uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis -v; git status --porcelain; git diff pyproject.toml | Bounded implementation of Decision 2 complete. Baseline check: uv run --group test python -m unittest runtime.tests.test_phase7_tracer -v shows 1 pass, 3 pre-existing errors on this Windows machine -- a PermissionError on tempdir cleanup of journal.sqlite (WinError 32, file in use), unrelated to this change, not fixed (out of scope; pre-existing cross-platform gap). Implementation: pyproject.toml gained one [dependency-groups] test = [hypothesis>=6.100.0] entry (uv sync --group test installed hypothesis 6.165.10 + sortedcontainers, uv.lock updated mechanically); new file runtime/tests/test_phase7_hypothesis.py defines TracerGateRetryReplayMachine(RuleBasedStateMachine), importing build_tracer_graph/_journal_count unmodified from test_phase7_tracer.py, with rules for reject_gate, approve_gate (covering both retry-succeed and retry-exhaust via two fixed fail_until instances), and replay_after_terminal; asserts the four invariants named in Decision 2. Verification executed: uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis -v -- Ran 3 tests in 92.271s, OK, zero failures, zero errors, zero found counterexamples. git status confirms only pyproject.toml, uv.lock, and the new test file changed by this implementation; runtime/graph.py, test_phase7_tracer.py, and all pre-existing unrelated dirty/untracked files (WO 2026-08-21-003 edit, WO -005, active.md, all pre-existing before this session's implementation step) left untouched. |
| [system] | this session, grep -n restricted|high_consequence|release runtime/graph.py; grep -n builder.add_node|def build_.*_graph runtime/graph.py | grep across runtime/graph.py for restricted/high_consequence/release finds only the authority_gate docstring naming the four gate types (:920-922) and unrelated sensitivity/consequence field reads (:610, WorkObjectEnvelope frontmatter, not a gate). No node in build_phase6_graph (dispatch/branch_a/branch_b/join/direction_gate), the Phase 4 load/validate graph, or build_research_graph (propose_fetch/gate_fetch/fetch_source/record_note) does anything a restricted-content, high-consequence-creation, or release/deployment gate would sit in front of. The build plan places release/deployment concerns in Phase 8 (local production packaging, runbook), which is unbuilt. |
| [inference] | this session, Read runtime/graph.py:333-410 (Phase 4), :592-745 (Phase 6), :909-1067 (research); grep -rln for existing tests exercising the rejection path in runtime/tests/ | Read pass over all three real graphs' node bodies and edge topology (build_graph, build_phase6_graph, build_research_graph). Phase 4 (load_envelope/validate): no irreversible external effect exists -- load_envelope's marker write is a runtime-local log line (its own docstring: effectively-infallible), validate runs a read-only tools.ws validate subprocess; no gate present or needed. Phase 6 (dispatch/branch_a/branch_b/join/direction_gate): branch_a, branch_b, and join are explicitly documented read-only by construction (ADR 0025) -- they read canonical state but never mutate it; direction_gate exists but currently gates nothing consequential (no differential routing on approved/rejected, both simply complete). Zero irreversible effects exist in this graph today, so there is nothing to leak past the gate. Research graph (propose_fetch/gate_fetch/fetch_source/record_note): the one real irreversible effect (fetch_url's network GET in research_fetch_source) is enforced unreachable without approval via an in-node check (if not state.get(approved): return a failed receipt, never call fetch_url) -- not via add_conditional_edges (unlike the tracer graph's routing style). record_note appends a local audit-log entry regardless of approval outcome, by design (records what happened including rejections), not itself a consequential irreversible effect. Gap: no existing automated test empirically exercises the rejection path (Command(resume=False)) against research_fetch_source and asserts fetch_url was never called -- this claim currently rests on code inspection ([inference]), not an executed test ([system]). |
## Open questions

- **Answered.** Gate coverage: only `direction` (line 724) is clearly covered by `authority_gate`. `restricted handling`, `high consequence`, and `release authority` are not yet built; the research-fetch call site (line 935) does not map cleanly to any of them.
- **Answered.** Effect journal: `claim_idempotency_receipt`'s schema (`runtime/graph.py:274-280`) is claim-before-effect only — `(thread_id, work_object_id, effect_name, created_at)`, no status column, no attempt-count column.

## Next move

Two of six Success evidence items are done (`authority_gate` exists and is used; `RetryPolicy`/`error_handler` wired on `record_note`). Four remain, and the gate-coverage gap is now known to be real, not hypothetical: three of four director-gate types need new `authority_gate` call sites (restricted handling, high consequence, release authority), and the effect journal needs a schema change (status + attempt-count columns) before the Hypothesis `RuleBasedStateMachine` exit-evidence tests can meaningfully exercise retry/compensate sequences. Route to `alawas-engineering-implement-bounded-change` for these four items, in this order: (1) effect-journal schema first, since the gate work and the exit-evidence tests both want to observe attempt/status state; (2) the three missing gate call sites; (3) the Hypothesis test suite last, once both are in place.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T13:24:54Z — create-successor-and-resume

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Directed to 'continue Phase 7'. Original tracking Work Object (2026-08-17-015, successor -016) lost from disk -- never committed to git before the 2026-08-21 tracking cutover. ADR 0026's design decision (Accepted, unchanged) and runtime/graph.py both show Phase 7 already partway through implementation (authority_gate, RetryPolicy/error_handler, effect journal all present for at least one gate/node). Created this successor in build state, not notice/explore, because the evidence shows active partial implementation, not an unstarted idea.
### 2026-08-21T13:25:44Z — answered-open-questions-scoped-remaining-work

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Read pass over runtime/graph.py answered both Open questions: authority_gate covers only the 'direction' gate type (1 of 4); the effect journal is claim-before-effect only, no status/attempt-count tracking. Remaining Phase 7 work is now concrete: effect-journal schema extension, three missing authority_gate call sites (restricted handling, high consequence, release authority), and the Hypothesis exit-evidence test suite, in that order.
### 2026-08-21T13:26:40Z — return-to-design-for-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** implement-bounded-change correctly refused to proceed: the Work Object had a composition decision (ADR 0026) but no bounded tracer bullet -- no rollback, observability, or exit criteria scoped to a first slice. Routing to design-tracer-bullet for the smallest item (effect-journal schema extension) before any implementation.
### 2026-08-21T13:31:40Z — accepted-hypothesis-tracer-bullet-route-to-implement

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Design-tracer-bullet corrected a mis-scoped Success evidence item (no SQLite schema change needed -- status/attempt-count already proven via effect_name suffixing and a marker file in test_phase7_tracer.py) and designed a bounded tracer bullet for the one item that is genuinely unbuilt: a Hypothesis RuleBasedStateMachine suite over the existing self-contained tracer graph. Director accepted (Decision 2), including adding hypothesis as a test-only dependency. Routing to implement-bounded-change.
### 2026-08-21T13:35:40Z — hypothesis-tracer-bullet-implemented-verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 2's tracer bullet implemented and verified: hypothesis added as a test-only dependency-group, new self-contained RuleBasedStateMachine test file written, executed (3 tests, 92s, OK, zero counterexamples). Two of three remaining Success evidence items now closed (effect-journal item corrected -- no schema change needed -- and Hypothesis suite item done). Remaining: wire the three missing real authority_gate call sites (restricted handling, high consequence, release authority) and confirm irreversible-effects-without-authority unreachability.
### 2026-08-21T13:38:29Z — deferred-three-gate-types-to-phase-8

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Grep and node-inventory across all three real graphs (Phase 4 load/validate, Phase 6 dispatch/branch/join, research) found zero call sites for restricted-content, high-consequence-creation, or release/deployment gates -- those concerns are Phase 8 scope, unbuilt. Director accepted deferring rather than inventing call sites (Decision 3). Only the direction gate (of four) and the separate research-fetch gate exist in real code; both were already true before this session. Remaining scope on this object is now just the last Success evidence item: confirming irreversible effects are unreachable without authority, checked against what exists today.
### 2026-08-21T13:40:37Z — verified-irreversible-effects-item-with-noted-gap

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Read pass over all three real graphs confirmed the last Success evidence item by code inspection: Phase 4/6 have zero irreversible effects today; the research graph's one irreversible effect (network fetch) is unreachable without approval via an in-node check. Noted gap: no executed test proves the rejection path empirically. Four of five Success evidence items are now closed (one via correction, one via new implementation, two pre-existing); the fifth is blocked/deferred to Phase 8 (Decision 3). This object is as complete as it can be without either Phase 8 work or a director call on the untested-rejection-path gap.
### 2026-08-21T13:41:10Z — Closed: Director: close now. Four of five Success evidence items closed this session: effect-journal status/attempt-count tracking corrected (no schema change needed, already proven by test_phase7_tracer.py), the Hypothesis RuleBasedStateMachine exit-evidence suite built and verified (test_phase7_hypothesis.py, zero counterexamples), and irreversible-effects-unreachable-without-authority confirmed by code inspection across all three real graphs. Two accepted open items remain on the record rather than being silently closed: (1) the three missing director-gate types (restricted handling, high consequence, release authority) are blocked on Phase 8, which is unbuilt -- Decision 3; (2) the rejection-path claim for research_fetch_source rests on code inspection, not an executed test. Both are explicit, revisitable gaps, not unknowns.

- **State:** close
- **Status:** closed
- **Actor:** director
- **Rationale:** Director: close now. Four of five Success evidence items closed this session: effect-journal status/attempt-count tracking corrected (no schema change needed, already proven by test_phase7_tracer.py), the Hypothesis RuleBasedStateMachine exit-evidence suite built and verified (test_phase7_hypothesis.py, zero counterexamples), and irreversible-effects-unreachable-without-authority confirmed by code inspection across all three real graphs. Two accepted open items remain on the record rather than being silently closed: (1) the three missing director-gate types (restricted handling, high consequence, release authority) are blocked on Phase 8, which is unbuilt -- Decision 3; (2) the rejection-path claim for research_fetch_source rests on code inspection, not an executed test. Both are explicit, revisitable gaps, not unknowns.
