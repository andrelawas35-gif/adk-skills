---
schema_version: 1
id: 2026-08-22-015
title: Design next business skill slice from portfolio report
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, governance]
created_at: 2026-08-22T12:49:15Z
updated_at: 2026-08-22T13:00:19Z
revisit_trigger: Director accepts, rejects, or changes the four-skill next-slice boundary.
next_action: Route to alawas-engineering-verify-release-evidence for release evidence review of the four-skill implementation and completed global install.










---
## Intent

Design the next bounded business-skill slice from the comprehensive portfolio
report, after the completed seven-skill tranche and the new business operating
pipeline. The slice should be small enough to implement safely while filling
the highest-leverage remaining business-management gaps.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] The next slice is selected from the remaining Wave 1 candidates with a
      clear rationale.
- [x] Boundary cards define trigger, governing question, minimum evidence,
      output, non-goals, authority gates, routes, and overlap tests.
- [x] Implementation remains gated behind an accepted boundary and excludes
      global install, deployment, and live business actions.


## Constraints and non-goals

**Constraints:**
- Preserve the Work Object lifecycle as the governing pipeline.
- Preserve the business operating pipeline as a routing spine, not a runtime
  orchestrator.
- Keep the next slice bounded to four remaining Wave 1 skills unless the
  director accepts a different boundary.
- Use the portfolio report and existing business skill contracts as evidence.

**Non-goals:**
- Implementing the four skills in this design pass.
- Global installation.
- Contacting external people or systems.
- Moving money, changing prices in market, changing staffing, issuing purchase
  orders, or mutating live business systems.
- Implementing quality/CAPA, organizational change, data governance, or
  continuity in this slice.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Select four-skill operating-control slice

| Field | Value |
|-------|-------|
| **Decision type** | tracer-design |
| **Result** | pass |
| **Scope** | Boundary-card design for `business-govern-initiative-portfolio`, `business-design-pricing-and-packaging`, `business-manage-liquidity-and-cash-runway`, and `business-balance-demand-supply-capacity`. Excludes implementation, runtime orchestration, global install, deployment, and live business actions. |
| **Authorization** | Director requested work on the next slice from `.work-studio/deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md`. |
| **Confidence** | medium — basis: the portfolio report names all four as Wave 1 candidates with distinct decision frontiers; no real-use telemetry yet proves their frequency. |
| **Actor** | director |
| **Revisit trigger** | Overlap tests show duplication with existing business skills, or observed Work Object use shows quality/CAPA, organizational change, data governance, or continuity blocks the next implementation more often. |
| **Rationale** | This slice fills upstream operating-control gaps: portfolio allocation, offer pricing, cash survival, and demand/supply feasibility. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | .work-studio/deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md | The comprehensive business-skill portfolio report identifies the remaining Wave 1 candidates after the completed first tranche. The selected next slice uses four high-leverage remaining candidates: govern-initiative-portfolio, design-pricing-and-packaging, manage-liquidity-and-cash-runway, and balance-demand-supply-capacity. |
| [system] | .work-studio/deliverables/2026-08-22-015-next-business-skill-slice-boundary-cards.md | Created boundary cards for the four-skill next slice. Each card defines trigger, governing question, minimum evidence, output, non-goals, authority gates, routes, and overlap tests against existing Work Studio business ownership. |
| [system] | boundary and authority review, 2026-08-22 | The design keeps implementation, global installation, deployment, external contact, money movement, staffing changes, purchase orders, pricing publication, and live-system mutation out of scope until a separate accepted implementation boundary and authority route exist. |
| [system] | bounded implementation, 2026-08-22 | Implemented the accepted four-skill next business slice locally: added core skill contracts for business-govern-initiative-portfolio, business-design-pricing-and-packaging, business-manage-liquidity-and-cash-runway, and business-balance-demand-supply-capacity; updated BUSINESS-OPERATING-PIPELINE.md, Skill-Aware Grilling profiles, business fixture coverage, component-governance mapping, component ledger entries COMP-037 through COMP-040, kernel manifest, generated skill map, and generated Codex, Claude Code, and GitHub Copilot adapters. Focused verification passed: unittest tests.test_business_management_skills tests.test_component_governance; tools/generate-adapters.py --check; tools/verify-kernel.py; ws validate ledger. |
| [decision] | Director request, 2026-08-22 | After verification of runtime business integration, director said "globally install it", separately authorizing global installation of the regenerated adapter bundles. |
| [system] | tools/install.ps1 global install, 2026-08-22 | Installed verified adapter bundles globally for codex, claude-code, and github-copilot. Source SHA256SUMS verification passed for each platform before copy. Post-install visibility check found 15 alawas-business-* skills in each global destination: C:\Users\Andre\.agents\skills, C:\Users\Andre\.claude\skills, and C:\Users\Andre\.copilot\skills. |
## Open questions

- Does the director accept this four-skill slice for implementation?

## Next move

If accepted, route to `alawas-engineering-implement-bounded-change` to
implement only the four accepted skill contracts and generated adapters.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T12:51:16Z — Next business skill slice boundary cards produced

- **State:** design
- **Status:** waiting
- **Actor:** codex
- **Rationale:** The requested next slice from the portfolio report has been selected and designed as boundary cards; implementation remains gated behind director acceptance of this four-skill boundary.
### 2026-08-22T12:51:34Z — Added waiting revisit trigger

- **State:** design
- **Status:** waiting
- **Actor:** codex
- **Rationale:** The Work Object is waiting for the director's acceptance, rejection, or modification of the four-skill next-slice boundary; the revisit trigger is now explicit in frontmatter.
### 2026-08-22T12:52:27Z — Director accepted four-skill next slice

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director said 'accept next slice', accepting the immediately preceding four-skill boundary for implementation: business-govern-initiative-portfolio, business-design-pricing-and-packaging, business-manage-liquidity-and-cash-runway, and business-balance-demand-supply-capacity. Scope excludes runtime orchestration, global install, deployment, external contact, live business-system mutation, money movement, personnel action, supplier/customer record mutation, and remaining Wave 1 skills.
### 2026-08-22T12:52:33Z — Accepted next business slice routed to implementation

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Director accepted the four-skill boundary; implementation is now authorized only within that recorded slice and its stated exclusions.
### 2026-08-22T12:57:01Z — Implemented accepted four-skill business slice

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The accepted bounded implementation is complete locally and focused verification passed; remaining work is release-evidence review, not global install, deployment, or live business action.
### 2026-08-22T13:00:19Z — Globally installed regenerated business adapters

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Director separately authorized global installation after runtime integration verification. The regenerated adapter bundles were installed globally for codex, claude-code, and github-copilot, and each global skill location now exposes all 15 business skills.
## artifacts

- `.work-studio/deliverables/2026-08-22-015-next-business-skill-slice-boundary-cards.md` (fingerprint: `27d055e27168`, commit: uncommitted at record time) — Boundary cards for the next four-skill business operating-control slice
