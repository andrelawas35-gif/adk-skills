---
schema_version: 1
id: 2026-08-24-005
title: Add PRESERVED / CHANGED reporting to ws for Work Object version diffs
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [architecture, engineering]
created_at: 2026-08-24T23:35:31Z
updated_at: 2026-08-25T00:05:26Z
next_action: V0 PRESERVED/CHANGED verified; further slice V1 opened as 2026-08-24-006. 005 may transition toward observe/close (outcome review) at the director's call.









---
## Intent

Build the plan §7 V0 table's last unbuilt component — PRESERVED / CHANGED
reporting: a `ws` command that generates a PRESERVED/CHANGED report from a
Work Object's version data, grounded in the existing `updated_at` + History
(per the plan's grounding). This is a successor slice of WO `2026-08-23-001`
(Director Console), completing the V0 foundation. It also connects to plan
§6.4 (via `2026-08-23-001` Decision 5), where the PRESERVED/CHANGED/PROPOSED
report is named as the Revision capture format — so the PRESERVED/CHANGED
portion built here is the shared mechanism a Revision will later use.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] A `ws` subcommand generates a PRESERVED/CHANGED report for a Work Object
      from its History/version data
- [ ] The report distinguishes preserved vs changed content correctly on a
      real Work Object (e.g., `2026-08-23-001` or SC030 `2026-08-23-004`)
- [ ] Read-only projection — never mutates the source Work Object
- [ ] Focused regression test added

## Constraints and non-goals

**Constraints:**
- File-first, read-only projection (same pattern as `command_center.py` /
  `scene_board.py`); never writes to the source Work Object or any other
  canonical file.
- Grounded in existing `updated_at` + History — the studio has no body-level
  baseline snapshot (the `ws validate` no-baseline note), so the report must
  be derivable from History/version data alone, not a new diff baseline.
- Smallest reversible change; follows the existing read-only projection
  pattern; registered as a `ws` subcommand.

**Non-goals:**
- Not building the PROPOSED channel or Evaluator-driven output (deferred per
  `2026-08-23-001` Decision 4 / plan §6.4).
- Not introducing a body-snapshot/diff-baseline mechanism.
- Not V1 production objects (Project → Sequence → Scene hierarchy, shot state
  machine) — that is a separate later slice.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Adopt the plan §7 V0 PRESERVED/CHANGED reporting component as this slice; PROPOSED and a diff baseline are out of scope

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This Work Object builds only the plan §7 V0 'PRESERVED / CHANGED reporting' row: a `ws`-grounded report generated from Work Object version data using existing `updated_at` + History, following the read-only projection pattern. The PROPOSED channel (plan §6.4, Evaluator output) and any new body-snapshot/diff-baseline mechanism are explicitly excluded. |
| **Authorization** | Director: 'open a next work slice', then selected 'PRESERVED / CHANGED reporting' from the offered slices (completes the last unbuilt plan §7 V0 row). |
| **Confidence** | high for the scope boundary (direct director selection of this specific slice); medium for the concrete report shape — what exactly counts as 'preserved' vs 'changed' for a Work Object given there is no body baseline is not yet pinned and is the tracer's job. |
| **Actor** | director |
| **Revisit trigger** | Reopen if the design tracer shows the report cannot honestly classify preserved/changed from History alone (e.g., History lacks the granularity), which would require either a narrower report or a decision on a lightweight version marker. |
| **Rationale** | The director chose this as the next slice to complete V0; the plan already names the component and its grounding (updated_at + History). Keeping PROPOSED and a diff-baseline out of scope preserves the smallest reversible change and avoids re-opening Decision 4's deferral. |

### Decision 2 — Accepted tracer-bullet design: read-only `ws preserved-changed <id>` tested against `2026-08-23-001`

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Accepted the tracer-bullet design from the design pass: a new read-only `ws preserved-changed <id>` subcommand (scene-board/command-center projection pattern) that reads a Work Object's frontmatter `updated_at` + append-only History and emits a PRESERVED/CHANGED report — what stayed the same across recorded transitions (unchanged fields/sections) vs. what changed (state/status moves, decisions recorded, next-action edits, evidence added). Tracer run: execute against `2026-08-23-001` (rich History: 12+ entries, 10 decisions) and read the output against the real record. |
| **Authorization** | Director: 'accept' (accepting the immediately preceding tracer design in its stated scope). |
| **Confidence** | high that this is the smallest honest shape; the riskiest assumption — that History/updated_at alone can support an honest preserved-vs-changed classification (no body baseline) — is not yet proven and is exactly what the tracer execution must test. |
| **Actor** | director |
| **Revisit trigger** | If the tracer run against `2026-08-23-001` shows History cannot honestly support the preserved/changed classification (sparse or ambiguous transitions), narrow the report shape or decide on a lightweight version marker — per Decision 1's revisit trigger. |
| **Rationale** | This is the smallest end-to-end slice that can falsify the riskiest assumption before any broader build: it needs only the existing History + updated_at, produces a visible read-only report, and can be rolled back by deleting one file. The 'preserved' side is an inverse inference (absence of change across transitions) whose trustworthiness is exactly what the tracer observes. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | `2026-08-23-001` Decision 5 + plan §6.4 | The PRESERVED/CHANGED/PROPOSED report is the Revision capture format; the PRESERVED/CHANGED portion built here is the shared mechanism. |
| [system] | plan §7 V0 table (`2026-08-23-001-director-console-implementation-plan.md`) | PRESERVED / CHANGED reporting row: 'Generated from diff between Work Object versions \| Existing updated_at + History' — the component this slice builds. |
| [system] | implement-bounded-change; tracer runs: ws preserved-changed 2026-08-23-001 / 2026-08-23-004 | implement-bounded-change (tracer executed): built tools/ws/preserved_changed.py and wired ws preserved-changed <id> (cmd function + parser + FUNC_MAP in __main__.py). Ran against real data: 2026-08-23-001 → State explore -> design -> build -> verify, Status active, Decisions 10, Evidence 29, Next-action updates 4, 29 History entries; SC030 2026-08-23-004 → State explore, Decisions 1, Evidence 6, 2 History entries. Honest classification from History alone — the riskiest assumption (Decision 2) is validated. Found + fixed pre-existing pattern bug: History bullets are '**Field:** value' (colon inside bold, the format generate_history_entry writes), same root cause as the scene_board thesis bug; parser now accepts both forms. Regression tests tests/test_preserved_changed.py (2) pass; combined with test_scene_board_direction 12/12 OK, exit 0. Broader test_ws_cli.py: only pre-existing failures (CHECK_REGISTRY drift, Windows path-separator); the flaky clock-race test did not trigger this run. No release claim. |
| [system] | verify-release-evidence pass (2026-08-25), executed checks on ws preserved-changed | verify-release-evidence (ws preserved-changed, meaningful/ordinary): claim 1 subcommand generates a PRESERVED/CHANGED report from History/version data — verified, ran on 2026-08-23-001, SC030 2026-08-23-004, and the slice itself; claim 2 distinguishes preserved vs changed on a real WO — verified (001: State explore->design->build->verify, Decisions 10, Evidence 29; SC030: State explore, Decisions 1, Evidence 6); claim 3 read-only — verified: target WO updated_at unchanged before/after run (READONLY_UNCHANGED=True), module has no write path; claim 4 regression test added — tests/test_preserved_changed.py passes, combined with test_scene_board_direction 12/12 OK exit 0. Failure behavior: nonexistent id → clean 'Work Object not found for ID', exit 1; insufficient History → 'Insufficient History to classify' (regression-tested). Privacy/security: ordinary sensitivity, local-only reads of .work-studio/objects/**/*.md, no secrets/external access crossed. Gaps (accepted, not verification failures): preserved is an inverse inference (absence of change across History) per Decision 2's accepted trade-off; next-action count derived from History action wording (labeled as such in output). Exit criteria MET. No release claim. |
## Open questions

- What exactly counts as 'preserved' vs 'changed' for a Work Object given the
  studio has no body-level baseline? (Resolved by the design tracer; Decision 1
  flags this as medium-confidence.)
- Which Work Object(s) serve as the honest test corpus for the report —
  `2026-08-23-001` (rich History) and/or SC030 `2026-08-23-004`?

## Next move

V0 PRESERVED/CHANGED verified; further slice V1 opened as 2026-08-24-006.
005 may transition toward observe/close (outcome review) at the director's
call.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-24T23:36:32Z — Open as next Director Console work slice (PRESERVED/CHANGED reporting)

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected PRESERVED/CHANGED reporting as the next work slice (option 2: open a next work slice). Created this change Work Object as a successor slice of 2026-08-23-001 completing plan section 7 V0. Decision 1 records the scope (PRESERVED/CHANGED only; PROPOSED channel and diff-baseline out of scope). Moving to design for the report-shape tracer.
### 2026-08-24T23:39:47Z — Director: 'accept' — tracer-bullet design accepted (Decision 2)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** design-tracer-bullet: director accepted the recommended tracer design (Decision 2) — a read-only ws preserved-changed <id> subcommand tested against 2026-08-23-001. Moving to build to implement the bounded tracer.
### 2026-08-24T23:50:03Z — implement-bounded-change: ws preserved-changed built; tracer validated on real data

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'route to implement'. Built tools/ws/preserved_changed.py + wired ws preserved-changed <id>. Tracer executed against real Work Objects: 2026-08-23-001 (State explore->design->build->verify, Decisions 10, Evidence 29) and SC030 2026-08-23-004 (State explore, Decisions 1, Evidence 6) — honest preserved/changed classification from History alone, validating Decision 2's riskiest assumption. Found+fixed the '**Field:** value' (colon inside bold) History bullet parsing bug (same root cause as the scene_board thesis fix). Regression tests 12/12 pass; broader suite unchanged (pre-existing failures only).
### 2026-08-25T00:01:31Z — Director: 'route to verify'

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Tracer exit criteria met (ws preserved-changed produces honest preserved/changed classification on real data; regression tests 12/12 pass). Director confirmed the route to verify. Moving out of build into verify for the verification pass.
### 2026-08-25T00:02:18Z — verify-release-evidence pass: all acceptance criteria met (director: 'route to verify')

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Executed verify-release-evidence on ws preserved-changed (director routed to verify). All four acceptance criteria verified with direct evidence: report generated from History/version data, preserved vs changed distinguished on real Work Objects (2026-08-23-001, SC030), read-only confirmed (target updated_at unchanged), regression test 12/12. Failure behavior exercised (nonexistent id clean error exit 1; insufficient History note). Gaps named, not hidden: preserved is an inverse inference per Decision 2's accepted trade-off; next-action count is a History-wording heuristic. Exit criteria MET; no release claim made.
### 2026-08-25T00:05:26Z — Director chose 'open a further slice' → V1 opened as 2026-08-24-006

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** The director's next decision after 005 verified resolved to opening the further slice: V1 Production Objects (2026-08-24-006). 005's PRESERVED/CHANGED component remains verified at verify. 005 itself may transition toward observe/close at the director's call.
## Relationships

  REL-2026_08_24_005-001:
    type: responds_to
    from: wo:2026-08-24-005
    to: wo:2026-08-23-001
    basis: "2026-08-23-001 Decision 5; plan section 7 V0"
    created_at: 2026-08-24T23:37:01Z
