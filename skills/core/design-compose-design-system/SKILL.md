---
name: design-compose-design-system
default_tier: high
description: "Use when a governed foundation, semantic token set, theme recipe, variant, or component-family relationship must be created or revised; composes design-system properties and preserves director authority over creative choices without mutating canonical assets."
---
# Compose Design Systems

## Governing principle

A governed design system is composed from a shared foundation with explicit
inheritance, overrides, and prohibitions, not invented whole per project.
Keep creative authority with the director: this skill proposes and records
system composition, and it never silently chooses direction or mutates
canonical assets itself.

## Boundaries and non-goals

This skill does:

- Compose and revise governed foundations, semantic token sets, theme recipes,
  variants, and component-family relationships.
- Record which properties are inherited, overridden, prohibited, or awaiting
  creative confirmation for an asset or project.
- Inspect local asset records under `.work-studio/design-assets/`, the routing
  rules in `references/DESIGN-ASSET-PIPELINE.md`, and the record shape in
  `references/DESIGN-ASSET-REGISTRY.md`.
- Route discovery of existing interface structure or token inventories to the
  skills that own them.
- Return a compact composition record through the conductor for confirmation,
  implementation, and verification.

This skill does not:

- Discover existing UI structure; route to `design-audit-product-interface`.
- Audit existing tokens or themes as a separate discovery pass; route to
  `design-build-design-foundation`.
- Silently choose a creative direction or approve themes, tokens, or variants
  on the director's behalf.
- Mutate canonical asset records, the component ledger, code, or external
  design tools by itself.
- Implement code or verify browser parity against a rendered direction.

## Inputs and preconditions

Use an activated Work Object that names the design-system outcome. Minimum
evidence is asset or project identity, the requested foundation, token set,
theme recipe, or component-family outcome, any current foundation or token
inventory when discoverable, confirmed creative direction or an explicit gap,
and constraints on inheritance, overrides, prohibited properties, and export.
Missing fields remain gaps.

## Required capabilities

- `file_read` and `content_search` - inspect permitted asset records, pipeline
  references, Work Objects, and component-ledger pointers.
- `directory_list` - discover local design asset records.
- `terminal_run` - run focused validation such as
  `python -m tools.ws validate design-assets`.
- `file_write` - return a compact composition record through the conductor.
- `user_confirmation` - obtain scoped authority before creative selection,
  source-token mutation, code writes, external design-tool sync, export, or
  schema migration.
- `structured_output` - report composition, inheritance, overrides,
  prohibitions, gaps, authority boundary, and revisit trigger.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only classification inside the current workspace is allowed.
- Creative selection, source-token mutation, code writes, external design-tool
  sync, export, and schema migration require scoped authority.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Outside explicit grilling,
nominate a Candidate only when a creative-direction conflict, inheritance
ambiguity, or proposed external effect would materially change the composition.

## Skill Grilling Profile

Apply the `design-compose-design-system` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge whether each property is truly
inherited, overridden, or prohibited, whether creative authority was confirmed
for every non-trivial choice, and whether composition stays in one owning
frontier.

## Design asset pipeline

Use `references/DESIGN-ASSET-PIPELINE.md` to keep intake distinct from system
composition, UX-pattern stewardship, creative application, implementation,
verification, component governance, and workbench projection. Use
`references/DESIGN-ASSET-REGISTRY.md` for the local file-backed asset record
shape.

## Stage workflow

1. Identify the asset or project record by explicit asset ID or file path.
2. Validate the local registry shape when possible with
   `python -m tools.ws validate design-assets`.
3. Confirm the requested outcome and any already-confirmed creative direction.
4. Classify which properties are inherited, overridden, prohibited, or awaiting
   creative confirmation.
5. Compose the system as a record for the director's confirmation; do not
   mutate canonical assets, ledgers, code, or external tools.
6. Route the confirmed composition to the next owning skill.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; local asset records, validation output,
  Work Objects, and component-ledger entries are `[system]`.
- User creative choices and accepted routes are `[decision]`.
- Composition and inheritance judgments are `[inference]` unless already
  recorded as decisions.
- Missing fields, unconfirmed creative choices, and source-of-truth conflicts
  are `[gap]`.

## Work Object updates

Return the asset identifier, source record, requested outcome, composition
record, confirmed creative direction, inheritance/override/prohibition
summary, gaps, authority needs, and revisit trigger to `conduct-work-object`.

## Routing and termination

- Existing route, layout, component, or interface discovery ->
  `design-audit-product-interface`.
- Existing token, typography, color, spacing, and theme discovery ->
  `design-build-design-foundation`.
- Reusable user goals, flows, states, accessibility, or content behavior ->
  `design-steward-experience-patterns`.
- Confirmed creative interpretation and execution boundary ->
  `design-apply-design-direction`.
- Reversible implementation of an accepted tracer or bounded change ->
  `alawas-engineering-implement-bounded-change`.
- Browser-visible design parity -> `design-verify-design-implementation`.
- Durable shipped component registration -> `design-track-components`.
- Read-only catalog, graph, comparison, or trace view ->
  `design-project-asset-workbench`.
- Ambiguous owner, unconfirmed creative direction, or scope expansion ->
  conductor for decision or outcome review.

## Output template

```markdown
## Design-system composition

- **Asset/Project:** <asset ID or project identity and source record>
- **Work Object:** <provenance and current lifecycle state>
- **Requested outcome:** <foundation/token/theme/component-family goal>
- **Creative direction:** <confirmed choice or explicit gap>
- **Composition:** <inherited, overridden, prohibited, and awaiting-confirmation properties>
- **Validation:** <executed registry check, result, and gaps>
- **Authority boundary:** <what this composition does not authorize>
- **Revisit trigger:** <when to recompose or reopen>
```

## Anti-patterns

- Treating composition as permission to choose creative direction silently.
- Copying token, theme, UX-pattern, or projection truth into the component
  ledger.
- Mutating canonical asset records, code, or external design tools from the
  composition step.
- Letting a workbench projection become the source of truth.
- Routing to multiple owners instead of naming the ambiguity.

## Final self-check

- Did I identify the asset/project and its source of truth?
- Did I validate or explicitly mark validation as unavailable?
- Did I preserve director authority over every creative choice?
- Did I avoid mutating assets, ledgers, projections, code, or external tools?
- Did I route to exactly one owner or preserve ambiguity as a gap?
