# design-manage-assets Component Ledger Proposal

**Work Object:** `2026-08-22-017`  
**Status:** proposal only; not appended to `.work-studio/component-ledger.md`

## Proposed Entry

```markdown
## COMP-XXX — Design asset intake and routing

- **status:** active
- **component kind:** skill
- **governance domain:** design
- **location(s):** `skills/core/design-manage-assets/SKILL.md`; `tools/ws/design_asset_routing.py`
- **built-by Work Object(s):** `2026-08-22-017`
- **depends-on:** COMP-001, COMP-002, COMP-014, COMP-015, COMP-016, COMP-022, COMP-023
- **depended-on-by:** future design asset registry, design-system composition, experience-pattern stewardship, and workbench projection skills
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-manage-assets`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** one local design asset can be classified and routed to exactly one next owning skill; missing fields, source-of-truth conflicts, projection drift, and unknown frontiers remain explicit gaps.
- **status rationale / findings:** Proposed by WO `2026-08-22-017` Slice 2. The skill is a thin intake/router and does not create, mutate, approve, implement, verify, register, export, or deploy assets.
```

## Boundary Test

| Question | Expected answer |
|----------|-----------------|
| Does this skill own asset identity and next-route classification? | Yes. |
| Does this skill create or mutate assets? | No. |
| Does this skill approve creative choices? | No. |
| Does this skill write the component ledger? | No. It can propose a route to `design-track-components`. |
| Does this skill own workbench projections? | No. It routes projection questions to `design-project-asset-workbench`. |
