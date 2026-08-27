---
schema_version: 1
id: 2026-08-22-014
title: Add canonical business operating pipeline
type: change
status: active
state: observe
consequence: meaningful
sensitivity: ordinary
domain: [business, architecture]
created_at: 2026-08-22T12:41:14Z
updated_at: 2026-08-22T12:47:27Z
next_action: Observe real business Work Object use for routing ambiguity; if global installation is desired, route to alawas-engineering-verify-release-evidence before install.





---
## Intent

Add a canonical business operating pipeline to Work Studio so the installed
business skills share one routing spine while the Work Object lifecycle remains
the governing work pipeline.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A canonical business operating pipeline reference exists and distinguishes
      business routing from the Work Object lifecycle.
- [x] The eleven business skills reference the pipeline without replacing their
      own decision boundaries.
- [x] Deterministic generation/validation checks pass for the touched surface.


## Constraints and non-goals

**Constraints:**
- Preserve the Work Object lifecycle as the governing work pipeline.
- Keep the pipeline as a routing/reference artifact, not a new omnibus skill.
- Preserve each business skill's existing authority gates and non-goals.
- Do not install globally, deploy, contact external parties, mutate live
  business systems, move money, or change personnel/supplier/customer records.

**Non-goals:**
- Creating a new business skill.
- Replacing `business-manage-commercial-pipeline`, which remains the sales
  opportunity pipeline owner.
- Adding runtime orchestration behavior before a separate accepted design.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Add business operating pipeline as a routing reference

| Field | Value |
|-------|-------|
| **Decision type** | implementation-boundary |
| **Result** | pass |
| **Scope** | Add `references/BUSINESS-OPERATING-PIPELINE.md` and wire the eleven business skills to consult it for business-domain routing; excludes new skill creation, runtime orchestration, global installation, deployment, and external/live business actions. |
| **Authorization** | Director asked to "go add the operating pipeline" after accepting the recommendation that the business skills need a routing model inside the Work Object lifecycle. |
| **Confidence** | medium — basis: current skill-map and business skill contracts already contain the required skill boundaries; the useful missing piece is a shared routing artifact, but real-use telemetry has not yet tested the route order. |
| **Actor** | director |
| **Revisit trigger** | Real Work Object use shows recurring ambiguity, a missing domain such as pricing/quality/continuity blocks routing, or runtime orchestration needs more than a reference map. |
| **Rationale** | A canonical operating pipeline prevents the word "pipeline" from collapsing sales opportunities, recurring operations, and Work Object lifecycle into one overloaded concept. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | bounded implementation checks, 2026-08-22 | Added references/BUSINESS-OPERATING-PIPELINE.md as the canonical business routing spine; wired all eleven skills/core/business-*/SKILL.md contracts to reference it; registered BUSINESS-OPERATING-PIPELINE.md in tools/generate-adapters.py shared references; regenerated Codex, Claude Code, and GitHub Copilot adapters; registered COMP-036 as a business governance protocol. Focused checks passed: unittest tests.test_business_management_skills tests.test_component_governance; tools/generate-adapters.py --check; ws validate ledger. |
| [system] | references/BUSINESS-OPERATING-PIPELINE.md and skills/core/business-*/SKILL.md | The canonical reference distinguishes Work Object lifecycle, commercial pipeline, and business operating pipeline; each of the eleven core business skills now includes a Business operating pipeline section pointing to references/BUSINESS-OPERATING-PIPELINE.md while preserving its own decision frontier and authority boundaries. |
| [system] | adapter and ledger verification commands, 2026-08-22 | Generated adapters include the pipeline reference through the registered shared-reference scanner. Focused verification passed: tools/generate-adapters.py --check; unittest tests.test_business_management_skills tests.test_component_governance; ws validate ledger. |
## Open questions

- Should the pipeline later become a deterministic `ws` command or runtime
  router after observed use?

## Next move

Route to `alawas-engineering-verify-release-evidence` only if global
installation or runtime-router promotion is requested; otherwise observe real
business Work Object use and revisit on routing ambiguity.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T12:41:51Z — Accepted business operating pipeline boundary

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Director authorized adding the operating pipeline; the Work Object now records a bounded routing-reference implementation and excludes runtime orchestration, global install, deployment, and live business actions.
### 2026-08-22T12:47:03Z — Business operating pipeline added and verified

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** The accepted routing-reference implementation is complete: canonical pipeline reference added, eleven business skills wired to it, adapters regenerated, component ledger registered, and focused checks passed.
