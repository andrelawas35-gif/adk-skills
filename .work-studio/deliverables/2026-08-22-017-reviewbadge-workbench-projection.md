# ReviewBadge Workbench Projection

**Projection type:** read-only tracer  
**Generated from:** `.work-studio/design-assets/reviewbadge.asset.md` and
`references/DESIGN-ASSET-PIPELINE.md`  
**Work Object:** `2026-08-22-017`  
**Projection rule:** Missing edges mean "not recorded", not "false".

## Catalog Row

| Field | Value |
|-------|-------|
| Asset ID | `asset.design.reviewbadge` |
| Name | `ReviewBadge` |
| Kind | component-family |
| Status | tracer |
| Source of truth | `.work-studio/design-assets/reviewbadge.asset.md` |
| Introduced by | `2026-08-22-017` |
| Current frontier | bounded implementation evidence |
| Next route | conductor -> verification/review after local checks |

## Relationship Graph

```text
2026-08-22-017
  -> references/DESIGN-ASSET-PIPELINE.md
  -> asset.design.reviewbadge
       -> semantic tokens
       -> theme: studio-neutral
       -> theme: editorial-contrast
       -> UX pattern: create-review-approve
       -> component-ledger proposal
       -> workbench projection
```

## Theme Comparison

| Theme | Shared behavior | Distinct expression |
|-------|-----------------|---------------------|
| `studio-neutral` | Same statuses, labels, radius limits, and blocked-state obligations. | Quiet operational status for dense studio tools. |
| `editorial-contrast` | Same statuses, labels, radius limits, and blocked-state obligations. | Higher contrast review status for editorial systems. |

## Frontier Ownership View

| Frontier | Owner | Projection confidence |
|----------|-------|-----------------------|
| Asset identity | `design-manage-assets` | Recorded in asset record. |
| Theme composition | `design-compose-design-system` | Recorded as tracer recipe, not verified in UI. |
| UX behavior | `design-steward-experience-patterns` | Recorded as tracer pattern, not tested with users. |
| Implementation | `alawas-engineering-implement-bounded-change` | This artifact set is the implementation slice. |
| Design verification | `design-verify-design-implementation` | Not yet run; no browser UI exists. |
| Component registration | `design-track-components` | Proposal only. |
| Projection | `design-project-asset-workbench` | This file is read-only. |

## Read-Only Guard

This projection must not be edited as the way to change asset truth. To change
the asset, update the owning source record through the appropriate Work Object
and skill route, then regenerate or revise the projection.

## Useful Relationship Exposed

The tracer exposes the main relationship the current component ledger cannot
express alone: one design asset has governance identity, design-system themes,
UX behavior, a possible component-ledger pointer, and a workbench projection,
but each layer has a different owner and source-of-truth boundary.
