---
schema_version: 1
id: "2026-07-15-005"
title: "Qualify PKM Project Adapter and operational scenarios"
type: "change"
status: "active"
state: "verify"
consequence: "meaningful"
sensitivity: "ordinary"
created_at: "2026-07-15T15:00:00Z"
updated_at: "2026-07-15T15:00:00Z"
next_action: "Review the qualification evidence before authorizing any live Personal Institution integration, deployment, or export."
---

# Qualify PKM Project Adapter and operational scenarios

## Intent

Qualify the released PKM Project Adapter surface through the installed shared
protocol and the three Slice 3 operational scenarios. This record preserves
only approved, minimum-necessary cross-package context: no Personal Institution
record, credential, production log, deployment result, or exported artifact is
included.

## Success evidence

- [system] The released adapter exposes `investigate-live-question`,
  `deploy-with-recovery`, and `diagnose-production-incident` on Codex, Claude
  Code, and GitHub Copilot, each with the released `SHARED-PROTOCOL.md`.
- [system] The qualification contract verifies the inquiry, recovery, and
  incident-follow-up scenario evidence as durable Work Studio records.
- [system] The record identifies verified paths, manual or unsupported gaps,
  and unresolved assumptions without claiming an external deployment or export.
- [system] This is artifact-level verification of released adapter contracts;
  live runtime behavior remains an explicit gap rather than an implied result.

## Constraints and non-goals

- [decision] Use only the released shared protocol and Approved Evidence
  Bridges; every handoff retains provenance, sensitivity, relevance, and
  limits.
- [decision] Do not scan, read, copy, mutate, synchronize, or export a
  Personal Institution archive.
- [decision] Do not contact an external system, execute a production change,
  create a real deployment, or export evidence.
- [decision] This qualification checks behavioral artifacts and generated
  adapters; it is not a live Personal Institution or production exercise.

## Operational qualification scenarios

### Scenario 1 — Inquiry outcome routing

- **Given**: An activated PKM Project Inquiry receives an Approved Evidence
  Bridge containing a minimum-necessary summary, user approval, provenance
  `lived`, sensitivity `ordinary`, a receiving Work Object reference,
  relevance, and limits.
- **When**: `investigate-live-question` reaches attributable evidence and an
  explicit uncertainty boundary.
- **Then**: It records the evidence summary, selected outcome, rationale, and
  next action; routes `answered` to an informed decision, `reframed` to a
  replacement Inquiry with history preserved, `prototype-ready` to `design`
  with a linked successor when required, or `unresolved` with the smallest safe
  next move.
- **Verification**: Verified inquiry path — the released core and every
  generated adapter retain the Approved Evidence Bridge gate, provenance and
  sensitivity requirements, and durable outcome-routing contract.

### Scenario 2 — Deployment recovery

- **Given**: A verified release Work Object has explicit authority for one
  incremental deployment, a runbook, readiness evidence, a reversible
  migration, rollback, and named reality checks.
- **When**: A required post-deployment check reports unsafe behavior.
- **Then**: `deploy-with-recovery` stops further rollout, executes and verifies
  the authorized rollback when capability exists, records sanitized system
  evidence and remaining gaps, and routes incomplete recovery to investigation
  or decision rather than `observe`.
- **Verification**: Verified deployment recovery path — the fixture and
  released adapters distinguish failed verification, rollback attempt, and
  verified rollback without presenting production evidence or a successful
  deployment claim.

### Scenario 3 — Incident follow-up Change creation

- **Given**: An Incident has verified affected-path recovery and an accepted,
  bounded prevention action.
- **When**: `diagnose-production-incident` reaches the prevention boundary.
- **Then**: The Incident retains its evidence history and the conductor creates
  a linked Change Work Object with `responds_to`, one bounded outcome, owner,
  acceptance evidence, and its own authority boundary; it does not implement or
  deploy the prevention action during diagnosis.
- **Verification**: Verified incident follow-up path — the fixture and
  released adapters require a linked follow-up Change Work Object and preserve
  the Incident as the durable operational record.

## Evidence ledger

- 2026-07-15T15:00:00Z — [system] Issue #21 requires PKM Project Adapter
  qualification across inquiry routing, deployment recovery, and incident
  follow-up Change creation.
- 2026-07-15T15:00:00Z — [decision] The user confirmed the public test seam:
  a qualification contract that reads released adapter artifacts and this
  durable operational evidence record.
- 2026-07-15T15:00:00Z — [system] The red qualification test failed because
  this Work Object record was absent; the released adapter artifact check
  already passed.
- 2026-07-15T15:00:00Z — [system] The generated adapters carry the released
  shared protocol beside each of the three operational skills, preserving the
  compatibility, ownership, Evidence Bridge, provenance, and sensitivity rules
  at every adapter handoff.

## Manual or unsupported gaps

- Platform execution of a deployment runbook may be `manual-fallback` or
  `unsupported`; in either case the affected path must pause or stop with an
  explicit gap, never claim verification, deployment, or healthy production.
- Reality contact, live production checks, and external dependency recovery
  require separately scoped authority and observed sanitized evidence. They
  were not exercised here.
- This record does not provide an Approved Evidence Bridge for a real Personal
  Institution record; the scenario validates the released bridge boundary only.

## Unresolved assumptions

- live Personal Institution runtime remains explicitly unverified.
- A real platform may expose a different capability classification for
  deployment execution or incident observation; the adapter must use its
  declared degradation route.
- A future PKM Project Adapter implementation may need a machine-validated
  Evidence Bridge schema, which this text-and-artifact qualification does not
  supply.

## Verification and release evidence

- [system] Focused qualification contract: `python3 -m unittest
  tests/test_pkm_project_adapter_qualification.py -v` — verifies the released
  adapter surface and all three operational evidence paths.
- [system] The complete suite, conformance gate, and generator drift check are
  required before this qualification is accepted.
- [decision] This qualification does not authorize an external deployment or export.
- [inference] The released instructions make the bounded paths available, but
  real runtime compliance depends on a platform loading and following its
  generated adapter under the applicable authority boundary.

## Next move

Review the qualification evidence before authorizing any live Personal
Institution integration, deployment, or export.

## History

- 2026-07-15T15:00:00Z — Captured and activated this qualification Change;
  state `notice`; status `active`; actor `agent`; platform `codex`; rationale:
  issue #21 requests bounded evidence without external operational authority.
- 2026-07-15T15:00:00Z — Accepted qualification seam recorded; state `design`;
  status `active`; actor `agent`; platform `codex`; rationale: the user
  confirmed the released-adapter and durable-record contract boundary.
- 2026-07-15T15:00:00Z — Added the qualification record; state `build`;
  status `active`; actor `agent`; platform `codex`; rationale: the red contract
  showed that the operational evidence was missing.
