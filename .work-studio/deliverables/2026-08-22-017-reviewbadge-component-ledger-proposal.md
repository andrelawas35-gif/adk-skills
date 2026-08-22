# ReviewBadge Component Ledger Proposal

**Work Object:** `2026-08-22-017`  
**Asset record:** `.work-studio/design-assets/reviewbadge.asset.md`  
**Status:** proposal only; not appended to `.work-studio/component-ledger.md`

This proposal tests whether the component ledger can point to a design asset
without becoming the asset registry. The ledger should register the durable
capability pointer and dependency edges; token, theme, UX-pattern, and
workbench truth should stay in the asset pipeline records.

## Proposed Entry

```markdown
## COMP-XXX — ReviewBadge design asset tracer

- **status:** active
- **component kind:** artifact-schema
- **governance domain:** design
- **location(s):** `.work-studio/design-assets/reviewbadge.asset.md`; `references/DESIGN-ASSET-PIPELINE.md`
- **built-by Work Object(s):** `2026-08-22-017`
- **depends-on:** COMP-001, COMP-002, COMP-014, COMP-015, COMP-016, COMP-022, COMP-023
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-manage-assets` with routing through `references/DESIGN-ASSET-PIPELINE.md`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** tracer passes when one asset can be traced across intake, design-system composition, experience-pattern stewardship, bounded implementation, verification, ledger proposal, and read-only projection with one owning skill per frontier.
- **status rationale / findings:** Proposed by WO `2026-08-22-017` as a reversible design asset-management tracer. Do not copy token, theme, or UX-pattern truth into the ledger; preserve those in the asset record and pipeline artifacts.
```

## Ledger Boundary Test

| Question | Expected answer |
|----------|-----------------|
| Does the ledger know this asset exists? | Yes, as a durable pointer after proposal acceptance. |
| Does the ledger own token values or theme recipes? | No. Those belong to the design asset record and design-system composition skill. |
| Does the ledger own UX state behavior? | No. That belongs to experience-pattern stewardship. |
| Does the ledger own workbench display data? | No. The workbench is a read-only projection. |
| Can this be rolled back? | Yes. Do not append the proposal, or remove a future accepted ledger entry through the normal retired-status path. |

## Revisit Trigger

Revisit the design asset pipeline if a real ledger entry needs to store asset
family, version, theme, UX-pattern, and projection fields directly in the
component ledger to remain useful.
