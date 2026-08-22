---
schema_version: 1
id: 2026-08-22-026
title: Connect business pipeline into the graph system
type: inquiry
status: active
state: design
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T14:45:15Z
updated_at: 2026-08-22T15:13:02Z
next_action: Extend section 9 with more business skills using the now-proven pattern, or begin Direction 2 (loop reducer) to close the empirical loop on WO 2026-08-22-029's revisit trigger (confirm 08-30 receivable / 09-01 rent land as predicted).


















---
## Intent

Connect the studio's pipelines (governance, design, engineering, business) into
the graph system by making decisions emit typed edges the graph can traverse.
The selected path is Direction 1 (conform to the typed-edge vocabulary) then
Direction 2 (close the empirical loop). This Work Object's current slice builds
the minimal missing tooling — `ws relation add` (write a typed edge) and
`ws graph trace` (traverse edges) — because both are proposed-but-unbuilt today,
which blocks every downstream connective step.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `ws relation add <from> --type <type> --to <to> --basis <ref>` appends a schema-valid, append-only REL record to a Work Object's `## Relationships` section
- [x] `ws graph trace <ref>` reads `## Relationships` across the corpus and prints edges touching `<ref>` (upstream/downstream)
- [x] Demo edge `2026-08-22-026 responds_to 2026-08-21-006` is written and printed by trace (executed, not planned)
- [x] One real business edge from `business-manage-liquidity-and-cash-runway` is written and traced — WO `2026-08-22-029` Decision 1 (real rent/receivable liquidity call), edge confirmed via `ws graph trace`


## Constraints and non-goals

**Constraints:**
- Follow the graph invariants: endpoint refs must resolve or be marked external; `type` must be in the fixed edge vocabulary; Relationships records are append-only; a missing edge means "not recorded," never "false."
- All writes go through `python3 -m tools.ws` with `--expect-updated`; add unit tests alongside the new commands.

**Non-goals:**
- NO NetworkX, no in-memory graph engine — a `## Relationships` section parser is the whole projection for this slice.
- NO loop reducer / loop-state (that is Direction 2, the next build).
- NO `ws decision|verification|outcome|handoff` commands; NO runtime/LangGraph plane.
- NO graph-check invariants beyond endpoint-resolves and type-in-vocabulary.
- NO §9 model refresh for the other 14 business skills yet.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted tracer: build minimal `ws relation add` + `ws graph trace`

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Build two commands in `tools/ws`: `ws relation add` (append-only typed edge into `## Relationships`) and `ws graph trace` (read-only projection over `## Relationships` across the corpus). Demo on one WO↔WO edge and one business edge from `business-manage-liquidity-and-cash-runway`. |
| **Authorization** | Director chose Option B ("build the minimal edge/graph tooling") after design-tracer-bullet surfaced that the framed emit+trace tracer could not run — `ws graph|relation|decision|verification|outcome|handoff` are all absent. |
| **Confidence** | high for the tooling gap being the true first blocker (basis: [system] all six commands error, [documented] they are proposed/unbuilt); medium for a section-parser projection being sufficient (basis: [inference] — this is the risk the tracer buys evidence on). |
| **Actor** | design-tracer-bullet (director-accepted) |
| **Revisit trigger** | If a `## Relationships` section-parser projection cannot resolve/scale past a handful of edges, revisit toward the NetworkX projection from the LangGraph build plan. |
| **Rationale** | Both write path and traversal path for typed edges are unbuilt; every downstream connective step (business edge, §9 refresh, Direction 2 loop reducer) depends on them. Building the smallest write+trace pair proves the projection approach before any graph engine, loop reducer, or runtime plane. |

**Riskiest assumption (falsifiable):** a `## Relationships` section parser is enough to write and traverse a typed edge with deterministic ref resolution and no schema migration beyond the Relationships writer/reader.
**Failure behavior:** if append-only append to a body section cannot be done safely via the CLI, or refs cannot be resolved deterministically across the corpus, the slice fails — route to pressure-test-decision on the projection design; do not claim the graph works if `trace` cannot resolve the demo edge.
**Rollback:** new code removable via source control; the demo edges revert via `ws backup`/`ws restore`.
**Exit → route:** on success, route to the §9 model refresh (now with working tooling) and Direction 2 (loop reducer) as the next build; on failure, route to `pressure-test-decision`/`investigate-live-question` on the projection approach.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | develop-idea selection, director-confirmed | Selected develop-idea Direction 1 (conform to typed-edge vocabulary) sequenced into Direction 2 (close the empirical loop), gated on refreshing the stale graph/loop architecture to cover all 42 canonical skills including the 15-skill business family. Directions 3 (runtime execution) and 4 (handoff-first) deferred; Direction 5 (business-as-lens) rejected-for-now. |
| [system] | ls skills/core; grep -c business epistemic-graph-loop architecture doc | Business is already a canonical peer family: 15 business skills in skills/core/ (42 canonical skills total). The graph/loop architecture doc says 22 skills and references business 0 times, so the model defining the graph system is stale and never covered business. |
| [system] | grep counts over .work-studio/objects and .work-studio | Edge substrate is empty: 0 of 36 Work Objects have a populated Relationships section; 0 handoff/HOF receipts exist; 0 of 15 business skills reference any typed record or graph write-path. Typed-edge vocabulary is defined but used nowhere, so the graph has nothing to traverse today for any pipeline. |
| [system] | ls docs/adr | grep runtime; src/work_studio_runtime absent | Runtime plane is authorized but unbuilt: ADR 0025 (runtime/truth boundary + single-writer) and ADR 0026 accepted; pyproject.toml and uv.lock exist; but src/work_studio_runtime/ does not exist. Supports deferring Direction 3 runtime execution. |
| [system] | python3 -m unittest tests.test_relation_graph_tracer -v | Riskiest assumption CONFIRMED: ws relation add (tools/ws/relation.py) and ws graph trace (tools/ws/graph.py) built and wired additively into tools/ws/__main__.py. A ## Relationships section-parser projection is sufficient for deterministic ref resolution with no schema migration -- endpoint validation (fixed edge-type vocabulary, WO-existence check on --to, explicit external: escape hatch) works as designed. 6 unit tests in tests/test_relation_graph_tracer.py, all pass. |
| [system] | ws relation add 2026-08-22-026 --type responds_to --to 2026-08-21-006; ws graph trace 2026-08-22-026; ws graph trace 2026-08-21-006 --direction upstream; ws validate | Live demo executed (not just tested): edge 2026-08-22-026 responds_to 2026-08-21-006 written via ws relation add and confirmed via ws graph trace from both directions. ws validate shows no new errors on the object. Repository inspection preserved all pre-existing dirty work untouched (git diff --stat clean, only intended files changed). |
| [gap] | grep -rli liquidity/runway/business-manage over .work-studio/objects -> no matches | Exit criteria item 'one real business edge from business-manage-liquidity-and-cash-runway' NOT met: no business-decision Work Object exists anywhere in the corpus to attach it to. implement-bounded-change correctly declined to fabricate one -- inventing a business decision would exceed its authority. This is the one remaining unresolved item before the tracer's exit criteria are fully satisfied. |
| [decision] | director confirmation 'write it'; edit to references/architecture/epistemic-graph-loop-system-improvement-architecture.md section 9 | Director confirmed and wrote the section-9 model extension: one new row for business-manage-liquidity-and-cash-runway added to references/architecture/epistemic-graph-loop-system-improvement-architecture.md section 9 table (first business-family entry). Recommended change names ws relation add as the real available mechanism, not the aspirational ws decision/verification/outcome commands the rest of the table assumes. Disposition: Amend now, pilot business skill. |
| [system] | WO 2026-08-22-029 Decision 1; ws graph trace 2026-08-22-026 | 4th exit-criteria item now MET: WO 2026-08-22-029 (business-manage-liquidity-and-cash-runway) reached a real Decision 1 (pay rent on schedule; $30,000 rent clears against $100k-150k cash in both scenarios). It carries a real responds_to edge to this WO, written before the decision existed and now backed by it -- confirmed via ws graph trace. Tracer bullet exit criteria fully satisfied: all 4 items done. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Route to `engineering-implement-bounded-change` to build `ws relation add` and
`ws graph trace` per Decision 1, with unit tests, staying within the stated
non-goals. Demo edges: `2026-08-22-026 responds_to 2026-08-21-006`, then one
business edge from `business-manage-liquidity-and-cash-runway`.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T14:45:15Z — Started via ws start (created + evidence + explore + activate primary)

- **State:** explore
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Director confirmed recommendation: conform then close, refresh model first.
### 2026-08-22T14:46:42Z — Director selected develop-idea recommendation: Direction 1 (conform business skills to the typed-edge vocabulary) sequenced into Direction 2 (close the empirical loop via the loop reducer), gated on a precondition of refreshing the stale graph/loop architecture to cover all 42 canonical skills incl. the business family. Directions 3 (runtime execution) and 4 (handoff-first) deferred until edges are a lived habit; Direction 5 (business-as-lens) rejected-for-now because business is an accepted peer family, not a lens. New capabilities to build now: typed_reference_resolution, graph_projection, graph_trace_query; handoff_receipt deferred to Direction 4.

- **State:** explore
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Empty edge substrate (0 relationships, 0 handoffs) and stale architecture make runtime/seam automation premature; conform-then-close is the lowest-risk connective path and matches the architecture's repair-before-expand priority.
### 2026-08-22T14:48:33Z — Advance explore->design to author the business-family extension of the graph/loop model

- **State:** design
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Selected precondition (refresh architecture section 9 for the business family) is domain-modeling of the target model. Ideal owner design-model-domain (architecture section 10.1) is not built; proceeding reduced-capability with conductor-authored draft pending director confirmation.
### 2026-08-22T14:49:58Z — Director chose smallest-slice-first for the model refresh: model ONE business skill (business-manage-liquidity-and-cash-runway) before generalizing to the family. Routing to design-tracer-bullet.

- **State:** design
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Tracer-first matches the studio's repair-before-expand ethos and avoids authoring a speculative 15-skill model before the first business edge is proven.
### 2026-08-22T14:57:49Z — Accepted tracer (Decision 1): build minimal ws relation add + ws graph trace. Routing to engineering-implement-bounded-change.

- **State:** build
- **Status:** active
- **Actor:** design-tracer-bullet
- **Rationale:** Director accepted Option B. Both typed-edge write path and traversal are unbuilt and block every downstream connective step; smallest write+trace pair proves the section-parser projection before any graph engine, loop reducer, or runtime plane.
### 2026-08-22T15:03:40Z — engineering-implement-bounded-change completed Decision 1: built ws relation add + ws graph trace, 6 unit tests passing, live demo edge (2026-08-22-026 responds_to 2026-08-21-006) written and traced both directions. Riskiest assumption confirmed. 3 of 4 success-evidence items checked. Remaining item (real business edge) correctly not fabricated -- no business-decision Work Object exists yet.

- **State:** build
- **Status:** active
- **Actor:** engineering-implement-bounded-change
- **Rationale:** Bounded implementation stayed within Decision 1 non-goals; all pre-existing dirty work preserved untouched. The tooling proof is genuinely done; the demo's business-edge item surfaced a real fork rather than being forced.
### 2026-08-22T15:04:10Z — Director chose: advance the section-9 model refresh now that ws relation add + ws graph trace are real tooling. The 4th exit-criteria item (a real business edge) will be satisfied naturally once a real business skill starts using the model, not forced ahead of it.

- **State:** design
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Tooling proof is sufficient evidence to generalize from; deferring further on the missing business decision would block real progress on a fact (no business Work Object exists yet) that the model refresh itself doesn't depend on.
### 2026-08-22T15:05:44Z — Wrote the section-9 model extension for business-manage-liquidity-and-cash-runway (one table row, first business-family entry) to the architecture doc, per director confirmation. The doc's stale '22 skills' framing elsewhere was deliberately left untouched -- flagged as a separate, larger scope item, not silently expanded into.

- **State:** design
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Precondition (section-9 coverage for the business family) is now started with one real, tooling-grounded entry rather than a speculative 15-skill draft. Business's first typed-edge path (ws relation add via observes/hands_off_to) is now modeled and documented, closing the original gap: business had zero representation in the graph/loop architecture.
### 2026-08-22T15:13:02Z — Tracer bullet exit criteria fully satisfied (4/4): tooling built and tested, demo WO-to-WO edge traced, and now a real business edge from WO 2026-08-22-029 (business-manage-liquidity-and-cash-runway, a real $100k cash / $50k receivable / $30k rent decision). Direction 1 (conform to typed-edge vocabulary) is proven end to end for one business skill.

- **State:** design
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** The whole point of Option B was to prove the tooling could carry a real business decision, not just a demo. It now has, with a genuine decision behind it rather than a fabricated one.
## Relationships

  REL-2026_08_22_026-001:
    type: responds_to
    from: wo:2026-08-22-026
    to: wo:2026-08-21-006
    basis: "Decision 1: continues the runtime/HandoffEnvelope question this tracer's non-goals defer"
    created_at: 2026-08-22T15:01:18Z
