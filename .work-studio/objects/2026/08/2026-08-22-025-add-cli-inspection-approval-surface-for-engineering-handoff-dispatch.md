---
schema_version: 1
id: 2026-08-22-025
title: Add CLI inspection/approval surface for engineering handoff dispatch
type: change
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [engineering, governance]
created_at: 2026-08-22T14:12:08Z
updated_at: 2026-08-22T14:30:42Z
next_action: Review the verified local CLI engineering-handoff tracer outcome via review-outcome-and-adapt: decide close versus next slice; do not deploy.














---
## Intent

Successor of Work Object `2026-08-22-024` (verified Phase 6 engineering
dispatch). Bounded outcome: add a CLI inspection/approval surface so a
proposed engineering handoff -- already computed and propagated by the
verified dispatch as `engineering_route_result` and
`engineering_handoff_envelope` -- can be inspected and approved or rejected
by the director. The verified dispatch in `runtime/graph.py` /
`runtime/engineering.py` is the source; this slice adds the actionable
surface, preserving business dispatch and generic lifecycle routing.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] A `ws` command can inspect the proposed engineering handoff for an
      engineering-scoped Work Object (read-only, no dispatch change)
- [ ] The command can approve or reject the proposed handoff and records the
      result without mutating canonical Work Object state outside
      governance/CLI
- [ ] Verified Phase 6 dispatch behavior and tests from `2026-08-22-024`
      still pass unchanged
- [ ] No deployment, schema migration, adapter regeneration, or
      checkpointed engineering router

## Constraints and non-goals

**Constraints:**
- Preserve the verified Phase 6 engineering dispatch behavior from
  `2026-08-22-024` (37 passing tests must remain green).
- Canonical Work Object writes stay under governance/CLI control.
- Use the verified `inspect_phase6` engineering payload exposure as the
  source for inspection.

**Non-goals:**
- No deployment or release.
- No schema migration, adapter regeneration, or checkpointed engineering
  LangGraph router.
- No changes to the engineering routing logic itself (already verified).

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted tracer: ws engineering-handoff inspect/approve/reject

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Implement the smallest CLI inspection/approval surface for engineering handoffs: `ws engineering-handoff inspect|approve|reject <id>` over the verified Phase 6 payloads, recording decisions via governance append; no dispatch or schema change. |
| **Authorization** | Director accepted the tracer design 2026-08-22 ("record then implement"). |
| **Confidence** | high for the read/record seam (verified inspect_phase6 exposure + existing governance append + claim-inspect CLI precedent); medium for WO-to-checkpoint mapping — basis: 2026-08-22-024 verified dispatch, tools/ws claim-inspect precedent |
| **Actor** | human (director) |
| **Revisit trigger** | Revisit if approval requires dispatch changes, schema migration, adapter regeneration, a checkpointed router, or deployment. |
| **Rationale** | The verified dispatch already computes and propagates engineering_handoff_envelope / engineering_route_result; the smallest useful slice is a CLI surface to inspect and approve/reject it, recording the decision through the existing governance path. |

- **Riskiest assumption**: A `ws` command can inspect and approve/reject the already-computed Phase 6 engineering handoff payload through the verified `inspect_phase6` exposure, recording the decision via governance append, without changing dispatch or canonical schema.
- **Bounded path**: `ws engineering-handoff inspect <id>` (read-only print of the proposed handoff; reports "no proposed engineering handoff" when absent), `approve|reject <id>` (records the decision via append-history/append-evidence), preserving the 37 verified tests.
- **Failure behavior**: no payload -> report no-handoff and do not approve; if the decision cannot be recorded through governance, stop and route to design/governance.
- **Observability**: tests for inspect output, approve records, reject records, no-payload stop; the 37 existing tests stay green.
- **Non-goals**: no dispatch/routing changes, no schema migration, no adapter regeneration, no checkpointed router, no deployment.
- **Rollback**: remove the new subcommands + tests; verified dispatch untouched.
- **Exit criteria**: inspect/approve/reject work against an engineering-scoped WO; no-payload path stops cleanly; 37 tests still green.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | director, 2026-08-22 | Director accepted the tracer-bullet design for the CLI inspection/approval surface (ws engineering-handoff inspect/approve/reject over verified Phase 6 payloads) and requested implementation; recorded as Decision 1. |
| [system] | implementation of Decision 1, 2026-08-22 | Implemented ws engineering-handoff inspect/approve/reject <id>: tools/ws/engineering_handoff.py (resolves WO by ID, checks engineering_scope, reads Phase 6 payload via runtime.graph.inspect_phase6, records approve/reject via governance append: History + [decision] evidence, concurrency-checked); wired into tools/ws/__main__.py (nested subcommand + dispatch). No dispatch/schema change. Tests: tests/test_engineering_handoff_cli.py (6 pass); existing 37 tests still pass. |
| [system] | verify-release-evidence, 2026-08-22 (executed) | Verified: 6 new CLI tests pass (uv run --python 3.11 python -m unittest tests.test_engineering_handoff_cli); 37 existing engineering/business/component-governance tests pass unchanged; boundary check - git diff confirms runtime/graph.py and runtime/engineering.py unmodified, only tools/ws/__main__.py modified + 2 new files; ws validate --files 2026-08-22-025 passes all default checks (append-only unverifiable - no baseline snapshot, expected for new object); no deployment/schema/adapters. |
| [decision] | director, outcome review 2026-08-22 | Director selected stop (close) after outcome review. Assessment: hypothesis confirmed at bounded local scope (6 new + 37 existing tests, boundary check, validation); real-world value insufficiently observed (no lived use of the CLI against a real engineering WO). No successor. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T14:12:28Z — Created successor for CLI engineering-handoff approval surface

- **State:** notice
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Director selected create-successor after outcome review of 2026-08-22-024 (verified Phase 6 engineering dispatch). Successor adds a CLI inspection/approval surface so proposed engineering handoffs can be acted on; 024's verified dispatch remains the source.
### 2026-08-22T14:12:35Z — Activated for design: CLI engineering-handoff approval surface

- **State:** design
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Successor of verified 2026-08-22-024; bounded outcome is a CLI surface to inspect and approve/reject proposed engineering handoffs, preserving verified dispatch behavior.
### 2026-08-22T14:15:08Z — Design accepted and recorded: CLI engineering-handoff surface

- **State:** design
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Director accepted the tracer-bullet design (Decision 1) and requested implementation; assumption, bounded path, failure behavior, observability, non-goals, rollback, and exit criteria recorded.
### 2026-08-22T14:15:14Z — State to build for CLI tracer implementation

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Tracer accepted (Decision 1); implementing ws engineering-handoff inspect/approve/reject over the verified Phase 6 payloads.
### 2026-08-22T14:22:54Z — Tracer bullet implemented and verified locally

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Implemented ws engineering-handoff inspect/approve/reject per Decision 1; 6 new CLI tests pass and the 37 existing engineering/business/component-governance tests remain green; no dispatch/schema change.
### 2026-08-22T14:23:00Z — State to verify for release-evidence check

- **State:** verify
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Implementation verified locally (6 new + 37 existing tests green); routing to verify-release-evidence for the formal evidence classification; no deployment.
### 2026-08-22T14:27:56Z — Verified CLI engineering-handoff tracer evidence

- **State:** verify
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Release-evidence verification: acceptance criteria met (inspect/approve/reject work, no-handoff path stops, 37 tests green), boundary preserved (no dispatch/schema/deployment), WO validates. Local evidence only; no release or deployment claim.
### 2026-08-22T14:28:03Z — State to observe: verified local tracer

- **State:** observe
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Verified evidence recorded; routing to review-outcome-and-adapt for close-vs-next-slice decision. Local release evidence only; no deployment.
### 2026-08-22T14:30:34Z — Review outcome: stop - close as resolved

- **State:** observe
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Outcome review: hypothesis confirmed at bounded local scope; value unobserved (no lived use). Director chose stop (close); no successor.
### 2026-08-22T14:30:42Z — Closed: Inquiry resolved: CLI engineering-handoff tracer verified at bounded local scope (6 new + 37 existing tests, boundary check, validation); director selected stop (close). No successor. Revisit: real-world value unobserved until the CLI is used against a real engineering-scoped WO; thread-id convention (WO id default) unvalidated in live Phase 6 use.

- **State:** close
- **Status:** closed
- **Actor:** system
- **Rationale:** Inquiry resolved: CLI engineering-handoff tracer verified at bounded local scope (6 new + 37 existing tests, boundary check, validation); director selected stop (close). No successor. Revisit: real-world value unobserved until the CLI is used against a real engineering-scoped WO; thread-id convention (WO id default) unvalidated in live Phase 6 use.
