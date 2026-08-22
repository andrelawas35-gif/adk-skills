---
schema_version: 1
id: 2026-08-22-007
title: Repair stale skill corpus verification expectations
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T11:11:54Z
updated_at: 2026-08-22T11:14:10Z
next_action: Review the verified test repair; resolve the unrelated empty Claude adapter reference in its owning workstream before checkout-wide adapter verification
responds_to: 2026-08-22-005








---
## Intent

Restore repository-native verification by deriving the skill-map test's expected corpus size from canonical `skills/core/*/SKILL.md` files and verify the concurrently added `research-produce-report` kernel registration.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] The skill-map test contains no stale fixed corpus count.
- [x] Skill-map generation and its focused tests pass for the current corpus.
- [x] Kernel integrity verification passes.
- [x] The four business skills and project dependencies remain unchanged.


## Constraints and non-goals

**Constraints:**
- Edit only `tests/test_ws_cli.py`; treat the existing kernel-manifest change as concurrent work to verify, not rewrite.
- Preserve all unrelated dirty-worktree changes.
- Use corpus-derived expectations that still detect missing generated entries.

**Non-goals:**
- Changing any canonical skill or project dependency.
- Modifying the external generic validator.
- Deploying, exporting, staging, or committing changes.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accept bounded verification repair

| Field | Value |
|-------|-------|
| **Decision type** | authority |
| **Result** | pass |
| **Scope** | Replace the stale fixed skill-count expectation in `tests/test_ws_cli.py` and verify the existing kernel registration. |
| **Authorization** | User directed “do next action” after the exact bounded repair was proposed. |
| **Confidence** | high — executable investigation isolated these two verification gaps. |
| **Actor** | user |
| **Revisit trigger** | The focused repair requires changes to production code, canonical skills, dependencies, or unrelated files. |
| **Rationale** | A corpus-derived test preserves verification as the skill set evolves; the kernel registration is already present and needs only verification. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | Conversation, 2026-08-22 | User authorized the proposed bounded repair by directing do next action; scope is the stale skill-count test and verification of the existing kernel registration. |
| [system] | tests/test_ws_cli.py | Replaced the fixed 22-skill expectation with a count derived from canonical skills/core/*/SKILL.md files; no canonical skill or dependency was changed. |
| [system] | Focused verification, 2026-08-22 | Skill-map, kernel-test, and business-management suites passed: 9 tests. tools/verify-kernel.py passed path existence, boundary integrity, version consistency, and bootstrap completeness. |
| [gap] | Generated adapter checksum regression, 2026-08-22 | A broader checksum test observed an unrelated concurrently created empty Claude adapter reference after generate-adapters --check had passed. The file is outside this change boundary and was not modified or regenerated. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
## Open questions

- None within the accepted boundary.

## Next move

Review the verified bounded change. The unrelated concurrent empty Claude
adapter reference remains outside scope and requires its owning workstream to
restore or regenerate it before checkout-wide adapter verification can pass.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:12:39Z — Created accepted bounded change

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** User authorized the exact verification repair identified by inquiry 2026-08-22-005.
### 2026-08-22T11:12:39Z — Accepted tracer routed to bounded implementation

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Scope is limited to one test expectation plus verification of the already-present kernel registration.
### 2026-08-22T11:14:10Z — Bounded implementation verified

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** The stale fixed count was replaced by a canonical-corpus-derived expectation; nine focused tests and kernel integrity pass. Unrelated concurrent adapter-reference damage is preserved as an explicit gap.
### 2026-08-22T11:14:10Z — Implementation ready for verification review

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Accepted exit criteria are met within scope; broader adapter failure is unrelated and not concealed.
