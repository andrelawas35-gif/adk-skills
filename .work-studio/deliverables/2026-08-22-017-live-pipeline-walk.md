# Live Pipeline Walk — Design Asset Pipeline on Real Draft Assets

**Work Object:** `2026-08-22-017`  
**Slice:** 9 (outcome review → `deepen`)  
**Deliverable type:** live-use observation record  
**Command basis:** `python -m unittest tests.test_live_pipeline_walk -v` (3 tests OK), `python -m tools.ws asset-workbench`, `python -m tools.ws validate design-assets`.

## Purpose

Exercise the accepted four-contract design asset pipeline on the real draft
asset records and record where the ownership map holds or strains. This is an
observation slice: no creative changes, no canonical asset mutation, no
external tool, no deployment.

## What was walked

All real asset records under `.work-studio/design-assets/` (template excluded):

| Asset ID | Kind | Status | Source |
|----------|------|--------|--------|
| `asset.design.reviewbadge` | component-family | tracer | ReviewBadge tracer record |
| `asset.design.studio-status-tokens` | token-set | draft | controlled ingest slice |
| `asset.design.reviewbadge-themes` | theme | draft | real-use ingest testing |
| `asset.design.create-review-approve-pattern` | ux-pattern | draft | real-use ingest testing |

## Frontier resolution (single owner each)

| Asset | Identity frontier | Kind frontier | Owning skill |
|-------|-------------------|---------------|--------------|
| `reviewbadge` | `design-manage-assets` | `component-family` | `design-compose-design-system` |
| `studio-status-tokens` | `design-manage-assets` | `tokens` | `design-compose-design-system` |
| `reviewbadge-themes` | `design-manage-assets` | `theme` | `design-compose-design-system` |
| `create-review-approve-pattern` | `design-manage-assets` | `ux-pattern` | `design-steward-experience-patterns` |

Every asset resolves to exactly one owner at its kind-appropriate frontier and
to `design-manage-assets` at the identity frontier. No asset routes to multiple
owners. Registry validation reports zero gaps for all four.

## Where the ownership map holds

- Each of the four drafted skills owns a distinct frontier set, and no real
  asset falls into an unowned or multi-owned gap.
- The workbench projection is regenerable from source records and remains
  read-only; refreshing it changes no asset truth.
- Draft records do not silently canonize: `design-manage-assets` must still
  classify and route before any asset becomes accepted.

## Observed strains and observations

1. **Naming strain (prose vs routing key):** the `create-review-approve-pattern`
   lifecycle table says its "current frontier is `experience-patterns`", but the
   routing vocabulary and CLI use `ux-pattern`. The record is descriptive prose,
   not a routing key, so routing is unambiguous; still, a human reading the
   record may expect `experience-patterns` to be a valid frontier. Minor;
   worth aligning the prose in a future repair slice.

> **Resolution (Slice 10 repair):** this strain was repaired on 2026-08-22.
> The `create-review-approve-pattern.asset.md` lifecycle prose now reads
> `ux-pattern`, matching the canonical routing vocabulary and the record's own
> asset kind. The ingest CLI `--frontier` remains a free string; constraining
> it to the routing vocabulary is an optional future hardening, not part of
> this repair.
2. **Value still unobserved at the decision surface:** this walk confirms
   technical ownership but not that the pipeline improves a real design
   decision. The workbench is the lookup surface and has not yet been used to
   make or compare a real creative choice; that remains the next observable
   step.
3. **Creative-authority boundary untested in production terms:** all four assets
   are drafts or tracer records; `design-compose-design-system` and
   `design-steward-experience-patterns` have not yet been exercised on an
   accepted canonical asset under a confirmed creative direction.
4. **Existing contract-shell status remains open:** the pipeline still depends
   on adjacent design skills whose implemented-vs-shell status is an open
   question (see Work Object Open questions).

## Verdict for the deepen direction

The pipeline ownership map holds on real draft assets; no routing ambiguity was
found. Observed value remains partial: lookup/compare surfaces exist but have
not yet driven a real creative decision. The next smallest observation step is
to use the workbench and the compose/steward contracts on one accepted asset
under a confirmed creative direction, or to close the naming strain first.

## Revisit trigger

Re-walk when: a new real asset kind is ingested, a contract frontier changes,
or the first accepted asset passes through compose/steward under confirmed
creative authority.
