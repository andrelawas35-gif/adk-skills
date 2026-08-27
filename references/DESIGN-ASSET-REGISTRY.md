# Design Asset Registry

## Purpose

The design asset registry is the local source-of-truth shape for reusable
design assets in Work Studio. It keeps canonical asset records in
`.work-studio/design-assets/` and lets workbench files, catalogs, dashboards,
and future database indexes remain read-only projections.

This registry does not replace Work Objects, the component ledger, or the
design asset pipeline. Work Objects govern decisions and lifecycle state. The
component ledger governs shipped capability pointers. The design asset pipeline
routes the next asset question. The registry stores the asset record itself.

## File Location

Asset records live at:

```text
.work-studio/design-assets/<slug>.asset.md
```

The filename is a stable pointer, not the identity. The asset's identity is the
`Asset ID` field inside the record.

## Required Fields

Each asset record must include these exact bold labels near the top:

| Field | Required shape |
|-------|----------------|
| `Work Object` | Backtick-wrapped Work Object ID such as `2026-08-22-017`. |
| `Pipeline` | Backtick-wrapped path to a pipeline reference. |
| `Status` | One of `tracer`, `draft`, `active`, `deprecated`, `retired`. |
| `Asset ID` | Dot-separated lowercase identifier beginning with `asset.design.`. |
| `Asset kind` | One of `foundation`, `token-set`, `theme`, `component-family`, `ux-pattern`, `flow`, `projection`, `motion`. |
| `Source of truth` | Plain statement naming the canonical record or accepted successor. |
| `Projection status` | Plain statement that projections are read-only and must not be edited as truth. |

## Required Sections

Each asset record must include:

- `## Asset Summary`
- `## Lifecycle`
- `## Verification Notes`
- `## Rollback`

The lifecycle section must assign each frontier to exactly one owning skill.
When a step is intentionally not run, the record should say so directly instead
of pretending it was verified.

## Projection Rule

A projection may read asset records and display relationships. It must not be
the way to edit asset truth. Missing edges mean "not recorded", not "false".

## Database Rule

The registry stays file-backed until real use shows a query, sharing, or
relationship-history limit that files cannot handle cleanly. If that happens,
prefer a read-only generated index first, then local SQLite, then hosted
Postgres/Neon only when cross-machine or shared hosted access is truly needed.

## Validation

Run:

```text
python -m tools.ws validate design-assets
```

The check validates all `*.asset.md` files under `.work-studio/design-assets/`.
It is explicit rather than part of the default Work Object checks because asset
records are their own artifact class.
