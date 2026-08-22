# Design Asset Skill Boundary Cards

**Work Object:** `2026-08-22-017`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Tracer asset:** `asset.design.reviewbadge`

These are narrow skill contract drafts for the asset-management pipeline. They
are not installed skills yet; they define ownership boundaries tested by the
`ReviewBadge` tracer.

## Boundary Card 1: `design-manage-assets`

**Trigger:** A reusable design asset needs identity, lifecycle status,
provenance, impact, or routing before another design skill can act.

**Governing question:** What is this design asset, where is its truth, what
state is it in, what depends on it, and which skill owns the next frontier?

**Minimum evidence:**

- asset identifier, kind, source of truth, and current lifecycle status;
- Work Object that introduced or changed it;
- provenance and sensitivity;
- known dependencies and dependents;
- current frontier and candidate owning skill.

**Output:** Asset intake and routing record with one current owner, gaps,
authority boundary, and revisit trigger.

**Non-goals:**

- Does not create themes, tokens, patterns, components, previews, or code.
- Does not approve creative choices.
- Does not mutate the component ledger by itself.
- Does not act as a workbench or source of truth for projections.

**Authority gates:** Writes outside the accepted asset record, external sync,
schema migration, destructive changes, and source-of-truth changes require
scoped authority.

**Overlap tests:**

- If the question is asset identity and next route, this skill owns it.
- If the question is token/theme composition, use
  `design-compose-design-system`.
- If the question is behavior, state, content, or accessibility expectations,
  use `design-steward-experience-patterns`.
- If the question is durable shipped component registration, use
  `design-track-components`.

## Boundary Card 2: `design-compose-design-system`

**Trigger:** A governed foundation, semantic token set, theme recipe, variant,
or component-family relationship needs to be created or revised.

**Governing question:** Which design-system properties are inherited,
overridden, prohibited, or awaiting creative confirmation for this asset or
project?

**Minimum evidence:**

- asset or project identity;
- current foundation or token inventory when discoverable;
- requested theme or component-family outcome;
- confirmed creative direction or explicit gap;
- constraints on inheritance, overrides, prohibited properties, and export.

**Output:** Design-system composition record naming foundation, tokens, themes,
variants, inheritance, overrides, prohibited properties, authority boundary,
and verification needs.

**Non-goals:**

- Does not discover existing UI structure; route to
  `design-audit-product-interface`.
- Does not discover existing tokens as a separate audit; route to
  `design-build-design-foundation`.
- Does not silently choose creative direction.
- Does not implement code or verify browser parity.

**Authority gates:** Creative selection, source token mutation, code writes,
external design-tool sync, export, and schema migration require scoped
authority.

**Overlap tests:**

- If the question is how a theme or component family should be composed, this
  skill owns it.
- If the question is user flow, state, accessibility, or content behavior, use
  `design-steward-experience-patterns`.

## Boundary Card 3: `design-steward-experience-patterns`

**Trigger:** A reusable UX pattern, user goal, flow, state model,
accessibility expectation, content behavior, or recovery behavior needs
stewardship.

**Governing question:** What user outcome and behavior does this reusable
experience pattern preserve across visual themes and implementations?

**Minimum evidence:**

- user goal and context;
- flow states, happy path, empty/loading/error/recovery behavior;
- content requirements and accessibility expectations;
- linked UI components or component families;
- research, testimony, or implementation evidence when available.

**Output:** Experience-pattern record with states, behavior, accessibility and
content expectations, evidence links, gaps, and revisit trigger.

**Non-goals:**

- Does not style the pattern or choose visual themes.
- Does not implement code.
- Does not replace user research or claim accessibility compliance from a
  written pattern alone.
- Does not register durable components in the ledger.

**Authority gates:** Accessibility claims, external research, personal data,
production analytics, and code changes require scoped authority.

**Overlap tests:**

- If the question is behavior across themes, this skill owns it.
- If the question is visual token or theme expression, use
  `design-compose-design-system`.
- If the question is rendered parity, use `design-verify-design-implementation`.

## Boundary Card 4: `design-project-asset-workbench`

**Trigger:** A person needs to browse, compare, trace, or inspect relationships
among assets, Work Objects, evidence, themes, components, patterns, and
implementations.

**Governing question:** What can be shown as a read-only projection from
canonical asset, Work Object, evidence, and component records?

**Minimum evidence:**

- canonical records to project;
- fields and relationships to display;
- missing-edge behavior;
- source-of-truth pointers;
- projection timestamp or version.

**Output:** Read-only graph, catalog, comparison, or trace projection with
source pointers, missing-data labels, and no write path.

**Non-goals:**

- Does not create or edit assets.
- Does not become the source of truth.
- Does not infer unrecorded relationships.
- Does not approve design choices, implement code, or register components.

**Authority gates:** Export, sharing, external indexing, production dashboard
publication, source-record mutation, and schema migration require scoped
authority.

**Overlap tests:**

- If the question is "what does the current record show?", this skill owns the
  projection.
- If the question is "what should the record become?", route back to the
  owning asset skill or conductor.
