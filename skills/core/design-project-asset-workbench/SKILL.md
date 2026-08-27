---
name: design-project-asset-workbench
default_tier: high
description: "Use when assets, Work Objects, evidence, themes, components, or patterns need read-only inspection; projects catalog views and never edits assets or source truth."
---
# Project Asset Workbench

## Governing principle

A workbench is a read-only projection over canonical records, never a second
source of truth. It helps the director browse, compare, trace, and inspect
relationships among assets, Work Objects, evidence, themes, components,
patterns, and implementations, while every change stays in the owning asset
skill, Work Object, or component ledger.

## Boundaries and non-goals

This skill does:

- Produce read-only catalog, graph, comparison, and trace projections from
  canonical asset records, Work Objects, evidence, and component-ledger
  pointers.
- Label missing data and unrecorded edges explicitly rather than filling them.
- Point every projected row back to its source record.
- Inspect local asset records under `.work-studio/design-assets/`, the routing
  rules in `references/DESIGN-ASSET-PIPELINE.md`, and the record shape in
  `references/DESIGN-ASSET-REGISTRY.md`.
- Regenerate the projection from source records, such as the local
  `python -m tools.ws asset-workbench` output.
- Return a compact projection record through the conductor when a new view is
  needed.

This skill does not:

- Create or edit assets, Work Objects, or component-ledger records.
- Become the source of truth for asset, theme, UX-pattern, or component
  knowledge.
- Infer unrecorded relationships or invent data to fill gaps.
- Approve design choices, implement code, or register durable components.
- Export, publish, or share a projection without scoped authority.

## Inputs and preconditions

Use an activated Work Object that names the projection need. Minimum evidence
is the canonical records to project, the fields and relationships to display,
missing-edge behavior, source-of-truth pointers for each projected item, and a
projection timestamp or version. Missing fields remain gaps.

## Required capabilities

- `file_read` and `content_search` - inspect permitted asset records, pipeline
  references, Work Objects, and component-ledger pointers.
- `directory_list` - discover local design asset records.
- `terminal_run` - run focused validation such as
  `python -m tools.ws validate design-assets` and regenerate projections such
  as `python -m tools.ws asset-workbench`.
- `file_write` - return a compact projection record through the conductor.
- `user_confirmation` - obtain scoped authority before export, sharing,
  external indexing, production dashboard publication, source-record mutation,
  or schema migration.
- `structured_output` - report projected items, source pointers, missing-data
  labels, gaps, authority boundary, and revisit trigger.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only projection inside the current workspace is allowed.
- Export, sharing, external indexing, production dashboard publication,
  source-record mutation, and schema migration require scoped authority.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Outside explicit grilling,
nominate a Candidate only when a projection would imply an unrecorded
relationship or begin acting as a source of truth.

## Skill Grilling Profile

Apply the `design-project-asset-workbench` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge every projected edge for a
source-record backing, every missing-data label, and whether the projection
stays read-only and regenerable from canonical records.

## Design asset pipeline

Use `references/DESIGN-ASSET-PIPELINE.md` to keep intake distinct from system
composition, UX-pattern stewardship, creative application, implementation,
verification, component governance, and workbench projection. Use
`references/DESIGN-ASSET-REGISTRY.md` for the local file-backed asset record
shape.

## Stage workflow

1. Identify the canonical records to project by explicit source path or asset
   ID.
2. Validate the local registry shape when possible with
   `python -m tools.ws validate design-assets`.
3. Determine the fields, relationships, and missing-edge behavior for the view.
4. Generate the projection from source records; label every missing edge rather
   than inferring it.
5. Keep the projection read-only; never write back to asset records, Work
   Objects, or the component ledger.
6. Return the projection through the conductor with source pointers and any
   authority boundary.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; local asset records, validation output,
  Work Objects, and component-ledger entries are `[system]`.
- User creative choices and accepted routes are `[decision]`.
- Projected-relationship and missing-edge judgments are `[inference]` unless
  already recorded as decisions.
- Missing fields, unbacked edges, and source-of-truth drift are `[gap]`.

## Work Object updates

Return the projection name, source records projected, fields and relationships
displayed, missing-data labels, source pointers, gaps, authority needs, and
revisit trigger to `conduct-work-object`.

## Routing and termination

- A question about what the current record shows -> this skill owns the
  projection.
- A question about what a record should become -> route back to the owning
  asset skill or conductor.
- Missing source record or ambiguous ownership -> conductor for decision or
  outcome review.

## Output template

```markdown
## Asset workbench projection

- **Projection:** <name, kind (catalog/graph/comparison/trace), and version>
- **Source records:** <canonical asset, Work Object, evidence, and ledger pointers>
- **Fields and relationships:** <displayed items and edges>
- **Missing data:** <explicit labels, none invented>
- **Validation:** <executed registry check, result, and gaps>
- **Source of truth:** <unchanged canonical records; projection is read-only>
- **Authority boundary:** <what this projection does not authorize>
- **Revisit trigger:** <when to regenerate or reopen>
```

## Anti-patterns

- Letting a workbench projection become the source of truth.
- Editing assets, Work Objects, or the component ledger from the projection.
- Inferring unrecorded relationships to make the view look complete.
- Publishing, exporting, or sharing a projection without scoped authority.
- Copying token, theme, UX-pattern, or projection truth into the component
  ledger.

## Final self-check

- Did I project only from canonical source records?
- Did I label missing edges instead of inventing them?
- Did I keep the projection read-only and regenerable?
- Did I avoid creating, editing, approving, implementing, or registering?
- Did I preserve the source-of-truth boundary?
