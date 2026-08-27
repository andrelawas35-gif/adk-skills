---
schema_version: 1
id: 2026-08-22-022
title: Prefer explicit business_scope metadata in Phase 6 dispatch
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, engineering]
created_at: 2026-08-22T13:29:32Z
updated_at: 2026-08-22T13:31:51Z
next_action: Recommended next slice: add validator support for optional business_scope after resolving or isolating overlapping tools/ws edits.










---
## Intent

Make Phase 6 business routing prefer explicit Work Object metadata over text
heuristics by recognizing a `business_scope` frontmatter key. This reduces
accidental business routing while keeping the previous heuristic as a backward
compatibility fallback for older Work Objects.

## Success evidence

- [x] `business_scope: true` forces Phase 6 business routing even when body text is generic.
- [x] `business_scope: false` disables Phase 6 business routing even when business words appear.
- [x] Existing heuristic remains available when `business_scope` is absent.
- [x] Business dispatch tests cover explicit true, explicit false, and existing business heuristic routing.
- [x] Non-business Phase 6 lifecycle regression remains green.
- [x] Phase 6 concurrent checks pass on standalone rerun.


## Constraints and non-goals

**Constraints:**
- Keep this slice runtime-only; do not change Work Object schema validation
  while `tools/ws/__main__.py` and `tools/ws/validate.py` have pre-existing
  unrelated edits.
- Preserve canonical non-writer behavior in Phase 6.
- Preserve fallback routing for existing business Work Objects that do not yet
  declare `business_scope`.
- Preserve unrelated dirty work in the repository.

**Non-goals:**
- No schema migration.
- No bulk modification of existing Work Objects.
- No adapter regeneration or global skill installation.
- No deployment or release.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Prefer explicit `business_scope` with fallback heuristic

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Phase 6 dispatch business-scope detection only. |
| **Authorization** | User requested "do next slice" after the prior Work Object recommended explicit business-scope metadata. |
| **Confidence** | high for runtime precedence behavior; medium for long-term schema shape — basis: tests cover explicit true, explicit false, fallback heuristic, lifecycle regression, and concurrent Phase 6 behavior. |
| **Actor** | Codex |
| **Revisit trigger** | Revisit when Work Object schema validation can safely add `business_scope` as a formally governed optional field. |
| **Rationale** | Explicit metadata gives directors/operators a deterministic override. Keeping the fallback avoids breaking existing business Work Objects before migration. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/graph.py | Phase 6 business-scope detection now checks explicit business_scope frontmatter before falling back to title, next_action, and open-questions heuristics. |
| [system] | runtime/graph.py | business_scope boolean true enables business routing; boolean false disables business routing. |
| [system] | runtime/graph.py | business_scope string values true/yes/business/business-operating enable business routing; false/no/none/generic disable it. |
| [system] | runtime/tests/test_business_graph.py | Added Phase 6 dispatch tests proving explicit business_scope true routes and explicit business_scope false suppresses routing despite business terms. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph -v completed successfully: 19 tests passed. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_handoff_graph.Phase6HandoffTests.test_multi_state_determinism_across_lifecycle -v completed successfully: 1 test passed. |
| [gap] | command | Broad 55-test seam run completed all assertions but ended with one Windows SQLite temp-file cleanup WinError 32 in runtime.tests.test_phase6_concurrent.test_two_concurrent_runs_complete_independently. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_phase6_concurrent -v rerun completed successfully: 2 tests passed. |
## Open questions

- Should `business_scope` become a validator-known optional frontmatter field
  in a later schema slice?
- Should existing business Work Objects be migrated to declare
  `business_scope: true` explicitly?

## Next move

Route to verification evidence review. Recommended next slice: add validator
support for optional `business_scope` once the pre-existing `tools/ws` edits are
no longer overlapping.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:31:25Z — Entered verification after explicit business_scope runtime integration

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Phase 6 dispatch now gives business_scope frontmatter precedence while preserving heuristic fallback for older Work Objects.
### 2026-08-22T13:31:51Z — Completed explicit business_scope Phase 6 dispatch slice

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Phase 6 dispatch now respects business_scope frontmatter before heuristic fallback, with focused and concurrent verification passing.
