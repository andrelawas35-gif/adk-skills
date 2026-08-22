# Explicit Gap Plan and Database Decision

**Work Object:** `2026-08-22-017`  
**Deliverable type:** plan synthesis with one bounded recommendation  
**Source material:** `2026-08-22-017` Decisions 1-3, verification evidence, and
`2026-08-22-012` database inquiry Decisions 1-2.

This document synthesizes already-recorded Work Object evidence. It does not
authorize database provisioning, production deployment, external design-tool
integration, or canonical-store replacement.

## Recommendation

Do not integrate a database management system now as the foundation of the
asset management system.

Build the actual asset management system first as a studio-native, local,
file-backed asset registry with generated read-only projections. Revisit a
database only after one of the recorded trigger conditions appears:

- real asset queries become awkward or slow with files;
- multiple Work Studio machines or users need shared live access;
- the workbench needs cross-project aggregation that flat files and generated
  indexes cannot support cleanly;
- asset versioning or relationship history forces duplicated or brittle file
  structures;
- the director explicitly chooses a hosted read-side database despite the
  local-first trade-off.

## Why Not Database Now

`2026-08-22-012` already tested the closest database decision in this studio
and closed with a no-database result for business artifacts. Its accepted
Direction 5 was spreadsheet-first, no database; the hand-test was judged clean;
the recorded revisit trigger was awkward spreadsheet representation at real
volume or a cross-machine/sharing need.

`2026-08-22-017` has not produced evidence that design assets have crossed
that threshold. The `ReviewBadge` tracer verified file-backed records,
artifact fingerprints, one-owner lifecycle boundaries, a read-only workbench
projection, and a component-ledger proposal that did not absorb asset truth.
That is evidence for a governed registry and projection model, not for a
hosted database.

## Gap Plan

| Gap | Why it matters | Next evidence move | Database implication |
|-----|----------------|--------------------|----------------------|
| No browser UI verified | The tracer proved artifact consistency, not a usable asset-management interface. | Build one local read-only asset catalog page over the `ReviewBadge` record and pipeline reference. | No database needed; generated HTML/JSON is enough for first UI proof. |
| No external design tool verified | The system must not assume Figma, but may later need Figma/Canva/etc. adapters. | Keep external design tools out of the next slice; add an adapter only when a real project names one. | A database does not solve external-tool authority or source-of-truth boundaries. |
| No production path verified | The tracer is local evidence only. | Add a local registry shape and deterministic validation before any production/deployment question. | Do not add hosted infrastructure before the canonical local path is proven. |
| No live user outcome verified | We do not yet know whether the workbench materially improves studio use. | Use the next slice personally on 2-3 real design assets and record where lookup/comparison helps or strains. | Database only if real use shows file/query limits. |
| Current design skill shell status remains open | Some design skills are contract shells or pending implementation. | Promote the four draft asset skills only as contracts first; implement `design-manage-assets` before the heavier specialists. | Skill readiness is an ownership problem, not a storage problem. |
| Component ledger schema overload remains possible | The ledger may become crowded if it stores asset truth. | Register one accepted asset pointer only after review; keep token/theme/UX truth in asset records. | If many asset relationships need querying later, add a read-only index before a canonical DB. |
| Workbench source-of-truth drift remains possible | A useful workbench can accidentally become the place people edit truth. | Enforce read-only projection language and generate the workbench from source records. | A database can worsen drift if it becomes a second writable store. |

## Proposed Next Slices

### Slice 1: Promote The Local Asset Registry Shape

Create a canonical local directory and schema for design assets, probably under
`.work-studio/design-assets/`, using the `ReviewBadge` record as the seed.

Deliverables:

- asset record template;
- allowed asset kinds and statuses;
- validation rules for required fields;
- source-of-truth and projection rules;
- one migration note for the existing `ReviewBadge` tracer record if needed.

Exit evidence:

- one validator or focused check confirms required fields;
- `ReviewBadge` passes;
- a deliberately incomplete asset fails with a useful message.

### Slice 2: Implement `design-manage-assets`

Start with the thin intake/router skill, not all four skills at once.

Deliverables:

- canonical skill contract;
- routing rules to existing design skills and draft future asset skills;
- fixture covering `ReviewBadge`;
- component-ledger proposal for the new skill, not yet broad adapter churn.

Exit evidence:

- one asset can be classified and routed to exactly one next owner;
- missing source-of-truth, missing status, and ambiguous owner cases are
  reported as gaps.

### Slice 3: Generate A Read-Only Asset Workbench

Build a local projection over asset records, Work Objects, component-ledger
proposals, and pipeline references.

Deliverables:

- static HTML or Markdown catalog;
- graph/catalog rows for `ReviewBadge`;
- missing-edge labels;
- no write path.

Exit evidence:

- the projection can be regenerated from source records;
- editing the projection is not required to change asset truth;
- the projection exposes at least one relationship that is harder to see in
  the raw component ledger.

### Slice 4: Test Real Asset Use Before Database

Use the registry and workbench on 2-3 real studio assets: one token/theme
asset, one component-family asset, and one UX-pattern asset.

Exit evidence:

- file-backed records remain clean enough, or
- relationship/query pain is documented clearly enough to justify a database
  tracer.

## Database Decision Rule

If the next real-use slice shows file-backed records are clean, stay local and
file-backed.

If the next real-use slice shows query or relationship pain, run a database
tracer in this order:

1. Read-only generated JSON index.
2. Local SQLite read-only/query projection.
3. Hosted Postgres/Neon read-only projection only if cross-machine, sharing, or
   hosted query access is truly needed.

Do not replace Markdown Work Objects, asset records, or the component ledger as
canonical truth without a separate high-consequence pressure-test decision.

## Supersession

The old "database management system now" direction is superseded for this
asset-management work by two later evidence trails:

- `2026-08-22-012` closed with no database needed now.
- `2026-08-22-017` verified the `ReviewBadge` tracer using local file-backed
  records and read-only projections.

The database idea is not rejected forever. It is deferred until the recorded
trigger conditions appear.

## Recommended Route

Route `2026-08-22-017` to `alawas-governance-review-outcome-and-adapt` with
this report as outcome evidence. The likely outcome recommendation is:

- promote `references/DESIGN-ASSET-PIPELINE.md` as the routing spine;
- create the local asset registry shape;
- implement `design-manage-assets` first;
- keep database work deferred until local registry/workbench evidence shows a
  real storage or query limit.
