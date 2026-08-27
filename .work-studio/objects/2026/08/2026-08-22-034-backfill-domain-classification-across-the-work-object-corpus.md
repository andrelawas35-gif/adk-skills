---
schema_version: 1
id: 2026-08-22-034
title: Backfill domain classification across the Work Object corpus
type: change
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [governance, engineering]
created_at: 2026-08-22T19:46:01Z
updated_at: 2026-08-22T19:52:26Z
next_action: Both this object and its parent (2026-08-22-031) are now substantially complete. Recommend routing both through review-outcome-and-adapt for formal outcome review and close, once the director confirms. The one remaining deferred item across the whole domain-axis effort -- a live ws list --domain query flag / command-center grouping -- was explicitly not scoped here and would need its own successor if wanted.









---
## Intent

Apply the domain classification mechanism proven in WO 2026-08-22-031 to the
35 corpus objects that don't yet carry a `domain:` field, so the "tell at a
glance what kind of work this is" goal covers the whole history, not just
the 8-object demo set.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Every one of the currently-unclassified objects has been read and either given a confident `domain:` list or explicitly flagged as resisting classification — 35 objects classified, 1 (`2026-08-22-027`) deliberately left unclassified because it carries a known pre-existing validation error unrelated to domain work; every other object resolved confidently, none genuinely resisted classification
- [x] `ws validate` shows no new errors introduced by the backfill — confirmed by diff: only a single `domain:` line was added to each touched file
- [x] `ws domain sync` re-run and its output spot-checked against a few of the newly classified objects — `business.md` and `architecture.md` verified directly


## Constraints and non-goals

**Constraints:**
- Use only the controlled vocabulary from WO 2026-08-22-031 (business, architecture, asset, design, governance, engineering, research, ideation, operations); do not invent a new domain value here.
- Classification is a judgment call per object's title/intent — do not guess when genuinely unclear; flag instead (see Decision 1's revisit trigger).

**Non-goals:**
- NOT adding a live `ws list --domain` query flag or command-center grouping — that is the other deferred successor, not this one.
- NOT touching the mechanism itself (schema, `ws domain sync` logic) — this is pure application of the already-built tooling.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Reuse the parent's settled mechanism; skip explore/design as no new design question exists

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This successor makes no new design decision. It inherits WO 2026-08-22-031 Decision 3 in full: domain as a list-shaped, controlled-vocabulary field; classification via direct-edit; `ws domain sync` as the read tooling. Scope here is purely applying that settled mechanism to the 35 remaining corpus objects. |
| **Authorization** | Director requested a successor Work Object and selected "backfill the remaining objects" as its scope. |
| **Confidence** | high (basis: [decision] the mechanism was already tested against real hard cases in the parent WO — 11 passing unit tests, a live 8-object demo confirming multi-domain edges; reapplying it at scale carries no new mechanism risk, only classification-judgment risk per object). |
| **Actor** | governance-conduct-work-object |
| **Revisit trigger** | If any of the 35 remaining objects resists confident classification the way none of the original 8 hard cases did, that is new evidence the vocabulary itself (not just its application) needs revisiting — reopen via WO 2026-08-22-031's own revisit triggers rather than inventing a new domain value here. |
| **Rationale** | Routing straight to `build` avoids stage theater (re-running explore/design for a decision that's already made), but skipping a Decision record entirely was wrong — the automated build-gate audit correctly caught it. Recording explicitly that "no new decision" is itself the decision, so the record stays honest and the gate is satisfied by fact, not by suppressing the check. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | Director request, successor scope selection | Successor to WO 2026-08-22-031 Decision 3. Domain tooling (schema, --domain flags, ws domain sync) is built and proven on an 8-object demo set; 35 of 44 corpus objects remain unclassified. This object scopes classifying the remainder using the already-proven mechanism -- no open design question remains, this is applying a settled decision at scale. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | python3 script applying classifications dict; grep verification | Classified 35 of 35 target objects via the sanctioned direct-edit path, controlled vocabulary only. One deliberate exclusion: 2026-08-22-027 left unclassified per explicit instruction (pre-existing unrelated validation error) -- confirmed via direct grep it carries no domain: line. |
| [system] | ws domain sync; ws validate; git diff .work-studio/objects/2026/08/2026-08-21-006*.md; python3 -m unittest tests.test_domain_axis tests.test_relation_graph_tracer | ws domain sync run for real: 44 of 45 corpus objects now carry a classification. Spot-checked business.md (14 entries incl. 013/016/029) and architecture.md (16 entries incl. 001/031) directly against assignments -- correct. ws validate shows no NEW errors: the errors on 2026-08-21-006 and 2026-08-22-027 are confirmed pre-existing (git diff on 006 shows only the added domain: line; 027 was never written to). 17/17 relevant unit tests pass as regression check. |
| [system] | review-outcome-and-adapt outcome review; director accepted stop | Outcome review (review-outcome-and-adapt): mechanism/coverage hypothesis CONFIRMED -- 44 of 45 corpus objects classified, spot-checked correct, no new validate errors, 17/17 regression tests pass. Value hypothesis (whole-corpus browsability actually helps in real use) is INSUFFICIENT OBSERVATION, same as parent WO 2026-08-22-031 -- not blocking closure since recorded Success Evidence was coverage-level. Director accepted stop. WO 2026-08-22-027's outstanding classification carried forward as a revisit trigger, not a blocker. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T19:46:01Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Mechanism is settled (Decision 3); this is bounded application work, not exploration. Routing directly toward implementation rather than re-running design/explore stages that would be stage theater.
### 2026-08-22T19:46:17Z — Skip explore/design: no open design question remains, WO 2026-08-22-031 Decision 3 already settled the mechanism (list-shaped domain field, ws domain sync). Routing directly to engineering-implement-bounded-change.

- **State:** build
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Applying an already-accepted decision at scale is bounded implementation work, not exploration -- treating it as design theater would violate the anti-pattern this studio explicitly warns against.
### 2026-08-22T19:46:45Z — Recorded Decision 1 after the build-transition audit correctly flagged its absence: no new design decision, this successor inherits WO 2026-08-22-031 Decision 3's mechanism in full and applies it at scale.

- **State:** build
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** The automated gap-audit caught a real omission rather than a false positive; recording the decision honestly (as 'no new decision, explicit reuse') satisfies the gate by fact instead of suppressing the check.
### 2026-08-22T19:50:27Z — Backfill complete: 35 objects classified, 1 (2026-08-22-027) deliberately excluded and noted, ws domain sync spot-checked, ws validate clean of new errors, 17/17 regression tests pass. All 3 success-evidence items met.

- **State:** observe
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Completed, demonstrated implementation with no open questions -- moving to observe rather than remaining in build, matching the same pattern applied to the parent WO 2026-08-22-031.
### 2026-08-22T19:52:26Z — Closed: Coverage hypothesis confirmed with direct evidence (44/45 classified, spot-checked, no regressions). Value hypothesis unobserved but not blocking, same reasoning as parent WO 2026-08-22-031. Director accepted stop after outcome review. WO 027's outstanding classification carried forward as revisit trigger.

- **State:** close
- **Status:** closed
- **Actor:** governance-review-outcome-and-adapt
- **Rationale:** Coverage hypothesis confirmed with direct evidence (44/45 classified, spot-checked, no regressions). Value hypothesis unobserved but not blocking, same reasoning as parent WO 2026-08-22-031. Director accepted stop after outcome review. WO 027's outstanding classification carried forward as revisit trigger.
## Relationships

  REL-2026_08_22_034-001:
    type: responds_to
    from: wo:2026-08-22-034
    to: wo:2026-08-22-031
    basis: "Successor scoping the corpus-wide backfill deferred by WO 2026-08-22-031"
    created_at: 2026-08-22T19:46:08Z
