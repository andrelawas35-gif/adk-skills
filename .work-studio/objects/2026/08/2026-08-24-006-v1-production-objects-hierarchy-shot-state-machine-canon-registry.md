---
schema_version: 1
id: 2026-08-24-006
title: V1 — Production Objects: hierarchy, shot state machine, canon registry
type: project
status: active
state: build
consequence: meaningful
sensitivity: ordinary
domain: [architecture, engineering]
created_at: 2026-08-25T00:03:45Z
updated_at: 2026-08-25T01:31:23Z
next_action: V1 mechanism complete + exit criteria met; continuation (the rest of V1 build-out) opened as 2026-08-24-010 (supersedes 006). 006 may transition toward verify/close at the director's call.











---
## Intent

Build V1 — Production Objects, the plan §7 next version of the Director
Console after V0 (foundation, verified via `2026-08-23-001` + `2026-08-24-005`).
This successor slice of WO `2026-08-23-001` builds the full production
hierarchy and the shot lifecycle, grounded entirely on existing `tools/ws`
capabilities:

- Project → Sequence → Scene → Beat → Shot hierarchy as linked Work Objects
  (`ws relation`)
- Shot object with tier classification (extended Work Object with shot
  metadata)
- Shot state machine (`ws transition` through shot-specific states:
  blocking → animation → render → review → approved)
- Canon registry (design asset records for approved artifacts)
- Hierarchy graph (`ws graph` traversal)

The V1 exit criteria from the plan: a project hierarchy exists as linked Work
Objects; a shot can be transitioned through its production states; canon is
recorded as design assets.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] A Project → Sequence → Scene → Beat → Shot hierarchy exists as linked
      Work Objects via `ws relation`
- [ ] A shot can be transitioned through its production states (blocking →
      animation → render → review → approved)
- [ ] Canon is recorded as design assets for approved artifacts
- [ ] The hierarchy is traversable via `ws graph`
- [ ] Focused regression tests for the hierarchy and shot state machine

## Constraints and non-goals

**Constraints:**
- File-first; grounded in existing `tools/ws` primitives (`ws relation`,
  `ws transition`, design-asset records, `ws graph`) — reuse, don't rebuild.
- Smallest reversible slices; each component independently verifiable.
- The shot state machine must reconcile with the existing `ws transition`
  state enum or add a clearly-bounded shot-state mechanism — no silent schema
  drift.

**Non-goals:**
- Not V2 audio (voice pipeline, TTS, takes) — the next version after V1.
- Not the creative-variant generation loop (V3/V4 ComfyUI/Blender) — the
  plan's later versions.
- Not a full production render pipeline or arbitrary shot-tracking features
  beyond the plan §7 V1 table.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Adopt the plan §7 V1 table as this slice's scope; riskiest assumption to tracer is schema/relation fit

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This Work Object builds V1 — Production Objects per the plan §7 V1 table: the Project → Sequence → Scene → Beat → Shot hierarchy (via `ws relation`), the shot object with tier classification, the shot state machine (blocking → animation → render → review → approved), the canon registry (design assets), and hierarchy graph traversal (`ws graph`). V2 audio and later versions are explicitly out of scope. |
| **Authorization** | Director: 'create a new work object for V1 production objects' (selecting V1 as the further slice after V0 completed). |
| **Confidence** | high for the scope boundary (direct director instruction naming V1); medium for the riskiest assumption — that the existing Work Object schema + `ws relation`/`ws transition` can represent the hierarchy and the shot-specific states (blocking/animation/render/review/approved are NOT in the current `ws transition` state enum, so the shot state machine's fit is a real, untested question). |
| **Actor** | director |
| **Revisit trigger** | Reopen the representation if the tracer shows the existing schema/relation cannot hold the hierarchy or the shot states without a material schema change — that would force a decision on a bounded shot-state mechanism rather than silent extension. |
| **Rationale** | V0 is complete and verified, so V1 is the plan's next self-contained version. The plan names the components and their grounding (reuse `ws relation`, `ws transition`, design assets, `ws graph`), but the concrete fit of the shot state machine against the fixed state enum is genuinely unknown and is exactly what the tracer should probe before any build. |

### Decision 2 — Accepted V1 tracer: 4-node Project → Sequence → Scene(SC030) → Shot hierarchy + shot-status metadata field

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Accepted the V1 tracer-bullet design from the design pass: hand-create a real 4-node hierarchy — Project WO → Sequence WO → Scene (reuse SC030 `2026-08-23-004`) → Shot WO — linked child→parent via `ws relation add --type depends_on`, traverse the chain via `ws graph trace`, and give the Shot WO a shot-status + tier metadata field (frontmatter) so a shot carries its production state without extending the fixed `ws transition` enum. Exit evidence: the chain traverses via `ws graph trace` and a shot carries its state. |
| **Authorization** | Director: 'i accept this v1 tracer' (accepting the immediately preceding tracer design in its stated scope). |
| **Confidence** | high that this is the smallest honest probe of the riskiest assumption; the assumption itself (hierarchy + shot state representable with the existing CLI, no material schema/enum change) is what the tracer run must test. |
| **Actor** | director |
| **Revisit trigger** | If the tracer run shows `ws graph trace` cannot traverse the linkage, or a shot's production state forces a schema/state-enum change, narrow the representation and decide on a bounded shot-state mechanism — per Decision 1's revisit trigger. |
| **Rationale** | The smallest end-to-end slice that can falsify V1's riskiest assumption before any broader build: it needs only existing `ws` primitives, produces a visible traversable hierarchy + a shot carrying state, and is reversible (seed objects can be removed). The `depends_on` child→parent verb is the honest stand-in for the missing `contains`/`part-of` semantics, which the tracer must judge. |

### Decision 3 — Confirmed canon registry: lightweight canon record (approved Shot WO + Component-Ledger-pattern canon index); plan §7 grounding corrected

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Canon registry representation for approved production artifacts (V1, plan §7). Confirmed: a lightweight canon record — the approved Shot Work Object (`shot_status: approved` + History) IS the canon record, plus a `.work-studio/canon-registry.md` index (Component-Ledger pattern) listing approved production artifacts. The plan §7 V1 grounding ('design asset records … existing design asset pipeline') is corrected: the design-asset pipeline is design-domain (`asset.design.*` ID prefix; design-only kinds/statuses/owning-skills) and cannot represent production shots. |
| **Authorization** | Director: 'accept recommendation' (accepting the immediately preceding pressure-tested recommendation, branch (b)). |
| **Confidence** | medium-high — the pipeline contract (`design_assets.py`), owning-skill map (`design_asset_routing.py` FRONTIER_OWNERS), and the Component-Ledger precedent (ADR 0014, `2026-08-23-001` Decision 6) are direct evidence; medium because the plan literally named 'design assets'. |
| **Actor** | director |
| **Revisit trigger** | Reopen if the studio later intends production artifacts to live in a unified asset system (making branch (a) — extending the design-asset pipeline — attractive), or if canon queries outgrow the prose index (a typed-pipeline need). |
| **Rationale** | Reuses the studio's proven Component-Ledger precedent for 'many small named things with declared edges'; lowest cost and highest reversibility; avoids conflating production canon with the design-domain asset pipeline. Branch (a) rejected as a category mismatch with real pipeline-governance cost (multi-file changes to a shared, design-governed pipeline). Branch (c) deferred because V2+ immediately needs canon discoverability. Edge case noted: two shots producing the same canonical artifact need a dedup/lineage rule in the index. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | plan §7 V1 table (`2026-08-23-001-director-console-implementation-plan.md`) | V1 components and grounding: hierarchy via `ws relation`, shot object with tier classification, shot state machine via `ws transition`, canon registry via design-asset records, hierarchy graph via `ws graph`; exit criteria: linked hierarchy exists, shot transitions production states, canon recorded as design assets. |
| [system] | `ws transition --help` (verified 2026-08-24) | The `ws transition` state enum is fixed: notice/explore/design/build/verify/release/observe/close — shot-specific states (blocking/animation/render/review/approved) are NOT present, so the shot state machine's fit is the V1 riskiest assumption. |
| [system] | implement-bounded-change / V1 tracer run (2026-08-25): ws create, ws relation add, ws graph trace, ws validate | V1 tracer executed (Decision 2): created seed WOs 2026-08-24-007 (Project P001), 2026-08-24-008 (Sequence SQ001), 2026-08-24-009 (Shot SH001) and linked child→parent via ws relation add --type depends_on: Shot 009 → Scene SC030 2026-08-23-004 → Sequence 008 → Project 007. ws graph trace --direction both from every node returns the chain (Shot: downstream→Scene; Scene: upstream←Shot, downstream→Sequence; Sequence: upstream←Scene, downstream→Project) — hierarchy representable and traversable via ws relation/ws graph, VALIDATED. Shot state: added shot_status: blocking + shot_tier: hero frontmatter fields to the Shot WO — ws validate passes, no schema change, VALIDATED. Note surfaced: ws graph trace requires the correct --direction (child→parent edges are downstream from the child, upstream into the parent) — navigation semantics, not a defect. Riskiest assumption (Decision 2) HOLDS. Seed WOs carry minimal Intents; left in notice, not activated. |
| [system] | implement-bounded-change run (2026-08-25): ws shot-status, ws validate, python -m unittest | V1 implementation (on the validated representation): built tools/ws/shot_status.py + wired ws shot-status --shot-status <state> (cmd + parser + FUNC_MAP). Shot state machine demonstrated end-to-end on SH001 (2026-08-24-009): blocking → animation → render → review → approved, each transition appending a History entry and bumping updated_at. Regression tests added (tests/test_shot_status.py, 5 tests: transitions, full sequence, invalid-state rejection, state set, hierarchy edge parsing) — combined with preserved_changed + scene_board_direction = 17/17 OK exit 0. Contract-drift fix: the shot-state flag was initially --status, which collided with the contract-drift check that matches --status against the WO lifecycle VALID_STATUSES; renamed to --shot-status, validate clean. Canon registry finding: the existing design-asset pipeline cannot represent approved production shots — ws asset-ingest rejects any asset ID not starting with asset.design. (kinds/statuses are design-domain only). The approved Shot WO itself (shot_status: approved + History) is the honest canon record; a production-artifact canon mechanism needs a decision (extend the asset pipeline vs. a lightweight canon index). V1 exit criteria: hierarchy exists + traverses (tracer), shot transitions production states (now a real CLI capability) — met; canon-registry representation is the open item. |
| [system] | implement-bounded-change (2026-08-25): created .work-studio/canon-registry.md; edited plan | implement-bounded-change (Decision 3): created .work-studio/canon-registry.md — a Component-Ledger-pattern index of approved production artifacts, first entry CANON-001 (Shot SH001 2026-08-24-009, shot_status approved, tier hero, placement Scene SC030→Sequence SQ001→Project P001, notes clarify it is a mechanism demonstration, not a director's creative approval of a final render). Corrected plan section 7 V1 canon-registry row from 'Design asset records for approved artifacts / Existing design asset pipeline' to 'Lightweight canon record — approved Shot WO (shot_status: approved) + .work-studio/canon-registry.md Component-Ledger-pattern index / Component-Ledger pattern (WO 2026-08-24-006 Decision 3)', and traced the correction in the plan header. V1 exit criteria now: hierarchy exists+traverses, shot transitions production states (ws shot-status), canon recorded (canon-registry index) — all met. |
## Open questions

- How are Project / Sequence / Scene / Beat / Shot represented as linked Work
  Objects — one Work Object per node, or a lighter record for Beat/Shot?
  (Tracer target.)
- How does the shot state machine reconcile with the fixed `ws transition`
  state enum (blocking/animation/render/review/approved are not in it)?
  (Tracer target.)
- Which `ws relation` edge verbs model the hierarchy (e.g., `depends_on`,
  `supports`, `implements`) and the shot→shot sequencing?

## Next move

V1 mechanism complete + exit criteria met; continuation (the rest of V1
build-out) opened as 2026-08-24-010 (supersedes 006). 006 may transition
toward verify/close at the director's call.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T00:04:51Z — Open as V1 Production Objects slice (director: 'create a new work object for V1 production objects')

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** V0 complete and verified; director opened the V1 Production Objects slice. Created this project Work Object as a successor slice of 2026-08-23-001. Decision 1 records the plan section 7 V1 scope and flags the riskiest assumption (existing schema + ws relation/ws transition fit for the hierarchy and shot-specific states). Moving to design for the tracer.
### 2026-08-25T00:10:27Z — Director: 'i accept this v1 tracer' — V1 tracer accepted (Decision 2)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** design-tracer-bullet: director accepted the V1 tracer design (Decision 2) — 4-node Project → Sequence → Scene(SC030) → Shot hierarchy linked via ws relation --type depends_on, a ws graph trace traversal check, and a shot-status + tier metadata field on the Shot WO. Moving to build to run the tracer.
### 2026-08-25T00:15:12Z — V1 tracer validated: hierarchy representable + traversable, shot state representable without schema change

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'go run it' / 'i accept this v1 tracer' (Decision 2). Ran the V1 tracer: created seed WOs 007 (Project), 008 (Sequence), 009 (Shot), linked Shot→Scene SC030→Sequence→Project via ws relation depends_on, traversed via ws graph trace (chain confirmed both directions from every node), and added shot_status/shot_tier metadata fields to the Shot WO (ws validate passes, no schema change). The riskiest assumption HOLDS — the existing schema + ws relation/ws graph represent the hierarchy and shot state without a material schema change. Note surfaced: graph trace needs the correct --direction (child→parent edges are downstream from the child).
### 2026-08-25T00:20:20Z — V1 shot state machine implemented and demonstrated; canon registry representation surfaced as a decision

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'route to implement'. Built ws shot-status --shot-status (tools/ws/shot_status.py + wiring) and demonstrated the full state machine on SH001 (2026-08-24-009): blocking → animation → render → review → approved, each with a History entry. Added tests/test_shot_status.py (5 tests); combined suites 17/17 OK. Fixed a contract-drift collision (renamed the shot-state flag from --status to --shot-status). Canon registry: the design-asset pipeline cannot represent production shots (asset-ingest requires asset.design.* IDs; design-only kinds/statuses) — the approved Shot WO is the honest canon record, and a production-artifact canon mechanism is an open decision, not silently forced.
### 2026-08-25T01:13:28Z — Decision 3 recorded: canon registry = lightweight canon record (approved Shot WO + Component-Ledger-pattern canon index); plan §7 grounding corrected

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** pressure-test-decision: director accepted branch (b) for the canon-registry representation — the approved Shot WO (shot_status: approved + History) is the canon record plus a .work-studio/canon-registry.md Component-Ledger-pattern index. The design-asset pipeline is design-domain (asset.design.* prefix; design-only kinds/statuses/owning-skills) and cannot represent production shots, so the plan §7 V1 grounding is corrected. Recorded Decision 3 with rationale, trade-offs, and revisit trigger.
### 2026-08-25T01:23:59Z — Canon registry implemented (Decision 3): canon-registry.md index created, plan §7 V1 corrected

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'route to implement'. Created .work-studio/canon-registry.md (Component-Ledger-pattern index, CANON-001 = Shot SH001 2026-08-24-009 approved) and corrected the plan section 7 V1 canon-registry row to the lightweight canon record, traced in the plan header to Decision 3. V1 exit criteria all met: hierarchy exists+traverses (ws relation/ws graph), shot transitions production states (ws shot-status), canon recorded (canon-registry index).
### 2026-08-25T01:31:23Z — Director opened successor 2026-08-24-010 for the rest of V1 (supersedes 006)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** V1 exit criteria met at the mechanism level in 006; the director opened a successor (2026-08-24-010, 'create successor for the rest of V1') for the production build-out rather than changing 006's identity or type in place. Successor is linked supersedes 006 and registered supporting.
## Relationships

  REL-2026_08_24_006-001:
    type: responds_to
    from: wo:2026-08-24-006
    to: wo:2026-08-23-001
    basis: "2026-08-23-001 Decision 1; plan section 7 V1"
    created_at: 2026-08-25T00:05:05Z
