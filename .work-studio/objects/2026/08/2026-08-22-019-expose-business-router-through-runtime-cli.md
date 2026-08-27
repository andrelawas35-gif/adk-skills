---
schema_version: 1
id: 2026-08-22-019
title: Expose business router through runtime CLI
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, engineering]
created_at: 2026-08-22T13:15:15Z
updated_at: 2026-08-22T13:17:10Z
next_action: Route to alawas-engineering-verify-release-evidence for release-evidence review of the module-local business-router CLI; broader runtime.graph command integration and Phase 6 integration remain separate future slices.







---
## Intent

Expose the checkpointed business operating router from Work Object
`2026-08-22-018` through a narrow runtime CLI on `python -m runtime.business`.
The command surface should let a user start a router proposal, inspect the
checkpointed proposal, and resume the paused director gate with approval or
rejection. This is a runtime interface slice only; it does not integrate the
router into the broader Phase 6 graph or mutate canonical Work Studio records.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `python -m runtime.business run-router ...` starts a fresh business-router
      proposal and pauses at the director gate.
- [x] `python -m runtime.business inspect-router ...` reports checkpointed
      router state.
- [x] `run-router --approve` resumes a paused thread and records approval.
- [x] Fresh `run-router` rejects missing `--next-gap` instead of creating a
      blank proposal.
- [x] Focused tests pass for business CLI, business router, component
      governance, and existing NetworkX projection behavior.


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->
- Keep the command surface local to `runtime.business`.
- Preserve the runtime/canonical truth boundary: CLI may checkpoint runtime
  state and print JSON, but must not write `.work-studio/` or touch live
  business systems.
- Preserve the checkpointed router semantics from Work Object `2026-08-22-018`.
- Keep output machine-readable JSON.

**Non-goals:**
<!-- Explicitly excluded work. -->
- No integration into `runtime.graph`'s larger command surface.
- No Phase 6 handoff graph integration.
- No canonical Work Object mutation from the runtime CLI.
- No live CRM, supplier, customer, pricing, money, personnel, or external-system
  action.
- No adapter regeneration, global install, release, or deployment.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Add narrow runtime.business CLI

| Field | Value |
|-------|-------|
| **Decision type** | bounded-change |
| **Result** | pass |
| **Scope** | Add `run-router` and `inspect-router` commands to `python -m runtime.business`; excludes broader runtime CLI integration, Phase 6 integration, canonical writes, live business effects, adapters, install, release, and deployment. |
| **Authorization** | Director said "do next slice" after the checkpointed LangGraph business router completed and identified CLI command-surface wiring as the next clean slice. |
| **Confidence** | high for narrow command surface; medium for long-term interface placement — basis: direct runtime.business helpers already existed and tests exercise the subprocess CLI path, while broader command placement remains unchosen. |
| **Actor** | director |
| **Revisit trigger** | The router needs to be invoked from `runtime.graph`, installed tooling, scripts, or a higher-level Work Studio command rather than `python -m runtime.business`. |
| **Rationale** | A module-local CLI is the smallest useful access layer over the checkpointed router without coupling it into Phase 6 or changing canonical write behavior. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/business.py | Added a module-local CLI main for python -m runtime.business with run-router and inspect-router subcommands; output is JSON and the CLI delegates to the existing checkpointed business-router helpers. |
| [system] | runtime/business.py | run-router starts a fresh proposal when --next-gap is provided, or resumes a paused router thread with mutually exclusive --approve/--reject flags; missing --next-gap on a fresh run exits with code 2. |
| [system] | runtime/tests/test_business_graph.py | Added subprocess CLI tests proving run-router pauses with a business handoff proposal, inspect-router reports awaiting_approval and has_handoff_envelope, run-router --approve resumes successfully, and missing --next-gap is rejected. |
| [system] | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph -v | Focused business suite passed: 12 tests ran successfully, including module-local CLI subprocess coverage. |
| [system] | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph tests.test_component_governance runtime.tests.test_projection -v | Focused compatibility set passed: 43 tests ran successfully across business CLI/router behavior, component-governance runtime enforcement, and existing NetworkX Work Object projection behavior. |
## Open questions

- Should the next integration move promote this module-local CLI into
  `runtime.graph`, or wire the business router into Phase 6 handoff flow?

## Next move

Route to `alawas-engineering-verify-release-evidence` for release-evidence
review of the module-local business-router CLI. Broader runtime CLI integration
and Phase 6 integration remain separate future slices.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:17:07Z — Created accepted business router CLI slice

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director asked to do the next slice after the checkpointed business router; this object bounds the next move to a module-local runtime.business CLI.
### 2026-08-22T13:17:08Z — Implemented module-local business router CLI

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Added run-router and inspect-router commands on python -m runtime.business; focused subprocess and compatibility tests passed.
