---
schema_version: 1
id: 2026-08-22-005
title: Determine whether validator failures reveal canonical skill defects or contract incompatibilities
type: inquiry
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
domain: [governance, engineering]
created_at: 2026-08-22T11:07:50Z
updated_at: 2026-08-22T11:10:53Z
next_action: Await authorization for a bounded repair of the stale skill-count test and missing research-produce-report kernel registration; make no changes to the four business skills
responds_to: 2026-08-22-004









---
## Intent

Determine whether the observed generic-validator and repository-test failures
identify defects in the four canonical business-management skills or only
incompatibilities and stale expectations in the validation contracts.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Each failure is reproduced independently and attributed to its owning contract.
- [x] The four canonical skills are checked with the repository's authoritative parser, generator, kernel, and behavioral contracts.
- [x] Contradictory or stale validation expectations are recorded without treating them as skill defects.
- [x] The inquiry reaches an evidence-backed `answered` route.


## Constraints and non-goals

**Constraints:**
- Keep investigation read-only except for this Work Object's durable record.
- Do not add project dependencies to accommodate an external validator.
- Separate canonical-skill defects from validator packaging and schema compatibility.

**Non-goals:**
- Fixing the validator, changing project dependencies, or implementing repository repairs.
- Reopening or mutating the closed predecessor `2026-08-22-004`.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Route the verification gap to a successor Inquiry

| Field | Value |
|-------|-------|
| **Decision type** | delegation |
| **Result** | pass |
| **Scope** | Investigate validator-contract compatibility as a bounded successor to `2026-08-22-004`. |
| **Authorization** | User directed “route to investigate” in conversation. |
| **Confidence** | high — the predecessor is closed and cannot be reopened; a successor preserves immutable history. |
| **Actor** | user and Codex |
| **Revisit trigger** | Evidence shows the question belongs to an existing active Work Object instead. |
| **Rationale** | The generic validator and stale repository expectation require attribution before release evidence can be interpreted correctly. |

### Decision 2 — Answer: no canonical business-skill defect is evidenced

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Attribution of the observed validator, kernel, skill-map, adapter, and focused behavioral results. |
| **Authorization** | Investigation and Work Object recording are within the user-directed route. |
| **Confidence** | high for the four business skills; high for validator incompatibility; high for the two unrelated repository gaps — basis: independently reproduced executable checks. |
| **Actor** | Codex |
| **Revisit trigger** | A repository-authoritative check reports a failure whose path or assertion names one of the four canonical business skills. |
| **Rationale** | Adapter generation and focused contracts pass for all four skills. The remaining failures identify the external validator's missing dependency and closed schema, an undeclared research skill in the kernel manifest, and a stale 22-skill test expectation. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | quick_validate.py standalone execution, 2026-08-22 | Execution stops at import yaml with ModuleNotFoundError, proving the validator runtime does not supply its own PyYAML dependency. |
| [system] | quick_validate.py with ephemeral PyYAML, 2026-08-22 | Execution reaches schema validation and rejects canonical default_tier because its fixed allowlist contains only allowed-tools, description, license, metadata, and name. |
| [system] | tools/generate-adapters.py --check and focused pytest, 2026-08-22 | All 27 skills across three adapters, manifests, checksums, authority blocks, and capability classifications match; nine focused business, kernel-test-module, and adapter tests pass. |
| [system] | tools/verify-kernel.py, 2026-08-22 | Kernel verification fails only because skills/core/research-produce-report/SKILL.md is undeclared in kernel-manifest.yaml; the four business-management skills are declared and no business-skill defect is reported. |
| [system] | tests/test_ws_cli.py::TestSkillMapCommand, 2026-08-22 | The test fails because it hard-codes 22 skills while the authoritative generator discovers and writes 27; generation itself exits successfully. |
## Open questions

- None within the bounded attribution question. Repair scope remains a separate change decision.

## Next move

If desired, authorize a bounded change to replace the stale 22-skill assertion
with a corpus-derived expectation and register `research-produce-report` in
`work-studio/kernel-manifest.yaml`. No change is required to the four business skills.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:08:20Z — Created successor inquiry

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** User routed the closed package inquiry's validator compatibility gap to investigation; successor responds_to 2026-08-22-004.
### 2026-08-22T11:08:29Z — Activated live-question investigation

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** Investigate the falsifiable question: do observed validation failures identify canonical skill defects, or only external and stale contract incompatibilities?
### 2026-08-22T11:08:48Z — Set investigation frontier

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** The smallest discriminating move is to compare each failing check's declared schema and corpus assumptions with the repository-authoritative contracts.
### 2026-08-22T11:10:53Z — Investigation outcome: answered

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** Executable evidence attributes no failure to the four canonical business skills: adapter and focused checks pass; failures belong to the generic validator environment/schema, an undeclared research-produce-report kernel entry, and a stale 22-skill assertion.
