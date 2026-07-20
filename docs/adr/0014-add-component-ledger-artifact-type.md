# 14. Add a component-ledger artifact type for continuous component grilling

- **Status:** Accepted (approved by repository owner 2026-07-18; WO `2026-07-18-001`)
- **Date:** 2026-07-18
- **Deciders:** repository owner (approval required per the Workspace Documentation Contract)

## Context

Work Studio tracks the *journey* of building things (signal → Work Object →
build → close) but has no **standing inventory of the capabilities that now
exist and remain improvable**. Once a Work Object closes, the realized
capability it shipped (e.g., the grilling engine) loses any durable handle for
continuous improvement. WO `2026-07-18-001` designed a component ledger to
close this gap. The Workspace Documentation Contract's own rules require an ADR
and owner approval to add a new artifact type to its registry.

## Decision

Add a `component-ledger` artifact type to the Canonical Artifact Registry:

```yaml
- type: component-ledger
  path: .work-studio/component-ledger.md
  purpose: Standing per-project index of realized capabilities (components),
    each grillable toward its best-case; a derived index of pointers + status,
    not a stored copy of the components themselves.
  owner: alawas-track-components   # new skill (see WO 2026-07-18-001, decision 14)
  stage_trigger: a Work Object ships a durable new capability
  required_evidence: shipping Work Object reference and component location
  creation_update_authority: Work Object authority rules
  provenance_freshness: entry carries a last-grilled commit SHA; drift =
    pointed-at files changed since that SHA
  supersession: entries move to `retired`, never deleted (lineage preserved)
  status: canonical
  validation: ledger schema + pointer-resolves + criteria-mapping review
```

## Consequences

- **Positive:** the existing system becomes continuously grillable; component
  identity outlives its build Work Object; per-project scoping matches
  `active.md`/`inbox.md`; the sweep queues findings as inbox signals rather than
  mass-spawning Work Objects.
- **Cost:** a new owning skill (`alawas-track-components`) and a bootstrap change
  to seed an empty ledger into new projects; a backfill pass to register
  already-shipped capabilities.
- **Resolved (was open risk):** decisions 6–8 originally assumed a *versioned
  scorecard bar*, but `govern-scorecards` has no mutable version primitive
  (only `supersedes`). Resolved 2026-07-18 (WO `2026-07-18-001`) with the
  **Option-B-refined** anchor: best-case = the four dimensions as inline
  criteria + the owning skill's Grilling Profile; "settled" = no surviving
  finding; auto-reopen on git-drift / owning-skill-version-change / contrary
  govern-scorecards outcome evidence. No competing scorecard artifact is
  created, so this ADR no longer depends on unbuilt scorecard infrastructure.

## Alternatives considered

- **Central cross-project ledger** — rejected: global cross-boundary dependency
  (WO `2026-07-18-001`, decision "each project owns its own ledger").
- **Fold into `govern-scorecards` or `conduct-work-object`** — rejected:
  overloads an existing skill with sweep/queue behavior (decision 14).
- **Stored inventory of component descriptions** — rejected: a second source of
  truth that drifts from code (decision 1).
