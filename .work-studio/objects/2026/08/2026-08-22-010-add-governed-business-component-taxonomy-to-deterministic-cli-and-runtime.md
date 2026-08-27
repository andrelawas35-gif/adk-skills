---
schema_version: 1
id: 2026-08-22-010
title: Add governed business component taxonomy to deterministic CLI and runtime
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, engineering, governance]
created_at: 2026-08-22T11:29:59Z
updated_at: 2026-08-22T11:40:52Z
responds_to: 2026-08-22-008
next_action: Route verified business-governance change toward release review; separately triage Windows SQLite handle and SIGKILL test failures





---
## Intent

Add an orthogonal component-governance taxonomy that makes business capabilities visible and enforceable in both the dependency-free deterministic layer and the runtime handoff contract, without changing the semantic meaning of Work Object `type`.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Canonical `component_kind` and `governance_domain` values exist in the dependency-free deterministic layer.
- [x] Runtime handoff envelopes reject invalid taxonomy values and routed-skill/domain mismatches.
- [x] The component ledger declares the taxonomy and registers all four accepted business skills as governed business components.
- [x] Focused tests prove deterministic, ledger, runtime, routing, and drift behavior.


## Constraints and non-goals

**Constraints:**
- Keep Work Object `type` as work shape: `change | inquiry | project | incident`.
- Keep the deterministic CLI dependency-free and the runtime read-only with respect to canonical state.
- Preserve strict Pydantic contracts and fail closed on invalid or mismatched governance metadata.

**Non-goals:**
- Creating additional business skills.
- Inferring governance from free-form task text or assigning multiple domains implicitly.
- Deployment or migration of Work Object frontmatter.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Add orthogonal component governance across deterministic and runtime planes

| Field | Value |
|-------|-------|
| **Decision type** | authority |
| **Result** | pass |
| **Scope** | Canonical enums `component_kind = skill | protocol | runtime | tooling | artifact-schema | integration` and `governance_domain = business | design | engineering | governance | operations | research | thinking | cross-cutting`; runtime projection; handoff enforcement; ledger schema and four business registrations; focused tests. |
| **Authorization** | User explicitly accepted the pressure-tested four-skill implementation on 2026-08-22. |
| **Confidence** | high — the taxonomy is orthogonal to Work Object lifecycle type and matches existing skill-family boundaries. |
| **Actor** | user (authority), Codex (recommendation and implementation) |
| **Revisit trigger** | A component legitimately needs multiple accountable domains, or a routed capability cannot be represented by the canonical taxonomy. |
| **Rationale** | Separating work shape from component ownership avoids type overloading while giving business capabilities deterministic and runtime-visible governance. |

### Decision 2 — Use a narrow end-to-end tracer bullet

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Canonical enum source, strict runtime handoff projection, component-ledger registration, and focused verification only. |
| **Authorization** | User acceptance of the recommended pressure-test result. |
| **Confidence** | high — it tests the riskiest cross-plane contract with a reversible, bounded change. |
| **Actor** | Codex |
| **Revisit trigger** | Focused tests expose an incompatible legacy envelope or ledger consumer. |
| **Rationale** | Riskiest assumption: one dependency-free taxonomy can govern ledger metadata and runtime dispatch without changing Work Object `type`. Failure must reject invalid values or routed-skill/domain mismatches; no silent inference. Rollback removes the projection, registrations, and tests without migrating canonical Work Objects. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | User acceptance, 2026-08-22 | Accepted the exact four-skill business governance implementation recommended by the pressure test. |
| [system] | `tools/ws/schema.py`; `runtime/handoff.py`; `.work-studio/component-ledger.md` | Baseline has Work Object lifecycle enums and strict runtime handoffs, but no orthogonal component governance fields. |
| [system] | `tools/ws/component_governance.py`; `runtime/handoff.py`; `runtime/graph.py` | Canonical enums now project into strict handoff fields; dispatch derives a declared domain for its routed skill and validation rejects mismatches. |
| [system] | `.work-studio/component-ledger.md` COMP-025 through COMP-028 | All four accepted business skills are registered as `component kind: skill` and `governance domain: business`. |
| [system] | `uv run --python 3.11 python -m unittest tests.test_component_governance -v` | Four focused tests passed, covering exact enums, route/domain mismatch rejection, strict Pydantic values, and ledger registration. |
| [system] | direct `phase6_dispatch` smoke test for WO 2026-08-22-010 | Runtime emitted `skill / thinking / turn-signal-into-work`, proving the governed route is present in serialized runtime state. |
| [gap] | `runtime.tests.test_handoff_graph` | Fourteen pre-existing graph tests cannot locate their deleted/missing fixture WO `2026-07-27-001`; failure occurs before the changed dispatch contract. |
| [gap] | `ws validate ledger` | Component governance and reciprocity pass; the command remains red only for pre-existing COMP-001 grill staleness at SHA `f4cddbf`. |
| [system] | runtime fixture repair, 2026-08-22 | Replaced absent hard-coded 2026-07-27-001 target with dedicated schema-valid build-state fixture 2026-08-22-011 across runtime suites; focused handoff and tracer tests passed 4/4. |
| [system] | COMP-001 regrill and ledger validation, 2026-08-22 | Reviewed Agreement Loop drift through HEAD 0de476b; director convergence authority and plain-language additions strengthen applicable dimensions with no surviving finding. COMP-001 re-stamped and ws validate ledger passed. |
## Open questions

None blocking.

## Next move

Route the verified change toward release review; retain the unrelated missing-fixture and COMP-001 staleness gaps for their owning Work Objects.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:34:21Z — Implemented accepted business component governance tracer

- **State:** verify
- **Status:** active
- **Actor:** Codex
- **Rationale:** Canonical deterministic taxonomy, strict runtime handoff enforcement, four governed business ledger registrations, and focused tests are implemented.
### 2026-08-22T11:34:47Z — Recorded focused verification evidence

- **State:** verify
- **Status:** active
- **Actor:** Codex
- **Rationale:** All accepted business-governance success evidence passed; two unrelated repository gaps are explicitly retained.
### 2026-08-22T11:40:52Z — Repaired recorded runtime fixture and COMP-001 staleness gaps

- **State:** verify
- **Status:** active
- **Actor:** Codex
- **Rationale:** Dedicated build-state fixture now satisfies focused runtime lookup/routing tests, and COMP-001 passed regrill and ledger validation at HEAD.
