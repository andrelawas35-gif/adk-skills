# Workspace Documentation Contract

This is the canonical documentation contract for this workspace. It is the
single discovery source for canonical project records; an absent registered
artifact is a **Missing Artifact Gap**, never evidence or permission to invent
content.

## Operating rules

- Inspect this contract and the exact registered location before reading or
  creating an artifact. Do not search plausible alternatives and select one.
- `conduct-work-object` is the sole custodian for bootstrap, persistence, and
  contract conflicts. Specialists return a recommendation and one next
  question; they do not write this contract.
- Explicit `bootstrap` authority creates this file and, after the
  `component-ledger` artifact type is accepted, its empty per-project ledger.
  Every other creation, update, migration, cleanup, or deletion needs
  separately scoped authority.
- A stage trigger is explicit user intent, an accepted decision, or registered
  evidence. Inference may recommend a mutation but cannot activate one.
- Consequential claims declare provenance as `system`, `decision`,
  `testimony`, `inference`, or `gap`. Compare conflicts by owner, provenance,
  freshness, and canonical status; surface material conflicts for a decision.
- Supersession names the predecessor and rationale. Do not erase predecessors.
- Generated artifacts are deterministic non-canonical copies. Regenerate them
  only after source validation and drift checking; do not edit them directly.

## Canonical Artifact Registry

```yaml
schema_version: 1
artifacts:
  - type: workspace-documentation-contract
    path: WORKSPACE-DOCUMENTATION-CONTRACT.md
    purpose: Declares documentation discovery and lifecycle rules.
    owner: conduct-work-object
    stage_trigger: explicit bootstrap authority
    required_evidence: user decision
    creation_update_authority: scoped user authority
    provenance_freshness: owner-approved; review on taxonomy or schema change
    supersession: ADR-backed successor link
    status: canonical
    validation: tests/test_workspace_documentation_contract.py
  - type: domain-context
    path: CONTEXT.md
    purpose: Defines canonical domain language.
    owner: domain-modeling
    stage_trigger: resolved domain term
    required_evidence: accepted terminology decision
    creation_update_authority: scoped user authority
    provenance_freshness: decision-backed; review when language conflicts
    supersession: explicit replacement link
    status: canonical
    validation: glossary term and conflict review
  - type: work-object
    path: .work-studio/objects/YYYY/MM/<id>-<slug>.md
    purpose: Records activated work, evidence, decisions, and continuity.
    owner: conduct-work-object
    stage_trigger: accepted work intent
    required_evidence: user signal or accepted outcome
    creation_update_authority: Work Object authority rules
    provenance_freshness: current lifecycle state; review on material transition
    supersession: typed successor relationship
    status: canonical
    validation: Work Object schema validation
  - type: architecture-decision-record
    path: docs/adr/<number>-<slug>.md
    purpose: Records a hard-to-reverse architectural trade-off.
    owner: accountable decision owner
    stage_trigger: accepted hard-to-reverse trade-off
    required_evidence: alternatives and owner decision
    creation_update_authority: scoped user authority
    provenance_freshness: decision-backed; review when assumptions change
    supersession: explicit ADR supersession link
    status: canonical
    validation: ADR trade-off review
  - type: plan-or-design
    path: docs/design/<slug>.md
    purpose: Records an accepted bounded plan or design.
    owner: design-tracer-bullet
    stage_trigger: accepted design boundary
    required_evidence: decision and constraints
    creation_update_authority: scoped user authority
    provenance_freshness: review when accepted boundary changes
    supersession: explicit successor link
    status: canonical
    validation: bounded-path verification
  - type: evidence-ledger
    path: .work-studio/objects/YYYY/MM/<id>-<slug>.md#evidence-ledger
    purpose: Records attributable evidence, conflicts, inferences, and gaps.
    owner: conduct-work-object
    stage_trigger: activated Work Object or Grilling Session
    required_evidence: attributable source or explicit gap
    creation_update_authority: Work Object authority rules
    provenance_freshness: source-specific; review on evidence change
    supersession: append-only correction or successor link
    status: canonical
    validation: provenance-lane review
  - type: component-ledger
    path: .work-studio/component-ledger.md
    purpose: Standing per-project index of realized capabilities (components),
      each grillable toward its best-case; a derived index of pointers + status,
      not a stored copy of the components themselves.
    owner: track-components
    stage_trigger: a Work Object ships a durable new capability
    required_evidence: shipping Work Object reference and component location
    creation_update_authority: Work Object authority rules
    provenance_freshness: entry carries a last-grilled commit SHA; drift =
      pointed-at files changed since that SHA
    supersession: entries move to retired, never deleted (lineage preserved)
    status: canonical
    validation: ledger schema + pointer-resolves + criteria-mapping review
  - type: runbook
    path: docs/runbooks/<slug>.md
    purpose: Records an approved operational procedure.
    owner: deploy-with-recovery
    stage_trigger: accepted recurring or operational procedure
    required_evidence: verified procedure and owner decision
    creation_update_authority: scoped user authority
    provenance_freshness: review after operational change or failed use
    supersession: explicit successor link
    status: canonical
    validation: procedure exercise or explicit gap
  - type: verification-record
    path: docs/verification/<slug>.md
    purpose: Records executed verification evidence and gaps.
    owner: verify-release-evidence
    stage_trigger: verification claim or release decision
    required_evidence: executed check or explicit unverified gap
    creation_update_authority: scoped user authority
    provenance_freshness: review when the verified artifact changes
    supersession: explicit successor link
    status: canonical
    validation: command-result traceability
  - type: outcome-review
    path: docs/outcomes/<slug>.md
    purpose: Compares observed outcome with an accepted hypothesis.
    owner: review-outcome-and-adapt
    stage_trigger: outcome observation or review trigger
    required_evidence: attributable observation and prior hypothesis
    creation_update_authority: scoped user authority
    provenance_freshness: review when new outcome evidence arrives
    supersession: explicit successor link
    status: canonical
    validation: hypothesis-to-observation traceability
  - type: generated-adapter
    path: adapters/<platform>/skills/<skill>/
    purpose: Distributes a deterministic non-canonical skill copy.
    owner: tools/generate-adapters.py
    stage_trigger: validated canonical source change
    required_evidence: canonical source and drift check
    creation_update_authority: deterministic generation
    provenance_freshness: current when checksum matches source generation
    supersession: regeneration; cleanup needs scoped authority
    status: generated
    validation: python3 tools/generate-adapters.py --check
  - type: kernel-manifest
    path: work-studio/kernel-manifest.yaml
    purpose: >
      Declares the portable kernel — the minimum set of source-of-truth files
      required to bootstrap Work Studio on any supported platform. Platform
      capability mappings and path-boundary integrity rules are co-located.
      Generated adapters, installed skill copies, and .work-studio/ runtime
      state are outputs, not kernel.
    owner: conduct-work-object
    stage_trigger: accepted kernel migration decision
    required_evidence: grilling-converged migration shape
    creation_update_authority: scoped user authority
    provenance_freshness: review when kernel entries or platform mappings change
    supersession: explicit successor link
    status: canonical
    validation: python3 tools/verify-kernel.py
  - type: agents-operating-contract
    path: AGENTS.md
    purpose: Thin, pointer-only operating contract orienting any agent
      working in this repository.
    owner: conduct-work-object
    stage_trigger: accepted design decision (2026-08-15-010 Decision 4)
    required_evidence: user decision
    creation_update_authority: scoped user authority
    provenance_freshness: owner-approved; review if canonical locations it
      points to move
    supersession: explicit replacement link
    status: canonical
    validation: manual pointer-only check (no restated policy)
```

Changing this registry's schema or taxonomy requires an ADR and explicit owner
approval. Its validation includes empty, docs-only, code-without-docs,
missing-reference, conflicting-record, stale-record, and partially-generated
adapter scenarios.
