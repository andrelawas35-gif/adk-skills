# ReviewBadge Asset Record

**Work Object:** `2026-08-22-017`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Status:** tracer  
**Asset ID:** `asset.design.reviewbadge`  
**Asset kind:** component-family  
**Source of truth:** this tracer record, pending future asset registry shape  
**Projection status:** projections are read-only and must not be edited as asset truth.

## Asset Summary

`ReviewBadge` is a small reusable status badge for the recurring
`create-review-approve` experience. It shows whether an item is `draft`,
`in_review`, `approved`, or `blocked`.

This record is a tracer asset, not a production asset. Its job is to test
whether the design asset pipeline can represent identity, system composition,
experience behavior, verification, component registration, and projection
without owner ambiguity.

## Lifecycle

| Step | Owning skill | Tracer evidence |
|------|--------------|-----------------|
| Intake and identity | `design-manage-assets` | Asset ID, kind, source of truth, lifecycle status, provenance, and current frontier are recorded here. |
| Existing UI discovery | `design-audit-product-interface` | Not run for this tracer; no current product interface is required to prove pipeline ownership. |
| Existing token discovery | `design-build-design-foundation` | Not run for this tracer; token examples are intentionally local to this asset. |
| Design-system composition | `design-compose-design-system` | One semantic token set and two theme recipes are declared below. |
| Experience-pattern stewardship | `design-steward-experience-patterns` | One `create-review-approve` behavior pattern is declared below. |
| Creative application | `design-apply-design-direction` | No visual implementation is applied in this tracer artifact. |
| Bounded implementation | `alawas-engineering-implement-bounded-change` | This file and related tracer artifacts are the reversible local implementation. |
| Design verification | `design-verify-design-implementation` | Verification is limited to artifact consistency checks; no browser UI exists yet. |
| Component governance | `design-track-components` | A ledger registration proposal exists in `.work-studio/deliverables/2026-08-22-017-reviewbadge-component-ledger-proposal.md`. |
| Workbench projection | `design-project-asset-workbench` | A read-only projection exists in `.work-studio/deliverables/2026-08-22-017-reviewbadge-workbench-projection.md`. |

## Semantic Tokens

| Token | Meaning | Allowed values |
|-------|---------|----------------|
| `review.badge.background` | Badge surface color for the current status. | Theme recipe decides. |
| `review.badge.text` | Badge text color for the current status. | Theme recipe decides. |
| `review.badge.border` | Badge border color for the current status. | Theme recipe decides. |
| `review.badge.radius` | Badge corner radius. | `4px` or `6px`; larger values require creative confirmation. |
| `review.badge.label` | Human-readable status label. | `Draft`, `In review`, `Approved`, `Blocked`. |

## Theme Recipes

| Theme | Intent | Inherited | Overridden | Prohibited |
|-------|--------|-----------|------------|------------|
| `studio-neutral` | Quiet operational status for dense studio tools. | Status names, label rules, radius range. | Muted gray, blue, green, and red surfaces. | Decorative gradients, oversized pills, icon-only status. |
| `editorial-contrast` | Stronger visual contrast for review-heavy editorial systems. | Status names, label rules, radius range. | Higher contrast text and borders. | Changing status meanings, hiding blocked state, using color as the only signal. |

## UX Pattern: create-review-approve

| State | User meaning | Required badge behavior |
|-------|--------------|-------------------------|
| `draft` | Work exists but is not ready for review. | Label says `Draft`; tone is low emphasis. |
| `in_review` | Work is waiting for a reviewer decision. | Label says `In review`; tone is active but not final. |
| `approved` | Work passed review. | Label says `Approved`; tone is positive but not celebratory. |
| `blocked` | Work cannot proceed without recovery. | Label says `Blocked`; tone is urgent and must include non-color contrast. |

## Verification Notes

- The asset has exactly one owning skill for each lifecycle frontier.
- The workbench projection is read-only and points back to this record.
- The component ledger proposal points to this asset without copying all token
  or theme truth into the ledger.

## Rollback

Delete this file and the three related tracer deliverables, then record a Work
Object History entry that the tracer was withdrawn. No external state, generated
adapter, deployment, or production artifact is required to roll back this
tracer.
