# Design Asset Pipeline

## Purpose

The design asset pipeline is the routing spine for governed design assets in
Work Studio. It does not replace the Work Object lifecycle, the component
ledger, or creative authority. A Work Object still owns durable state,
evidence, decisions, implementation, verification, and resumption; this
pipeline decides which design skill owns the current asset question.

## Pipeline distinction

| Pipeline | Owns | Does not own |
|----------|------|--------------|
| Work Object lifecycle | Work state: notice, explore, design, build, verify, release, observe, close. | Design-asset judgment by itself. |
| Component ledger | Durable shipped capability pointers, ownership, dependency edges, and grilling status. | Asset-family truth, theme recipes, UX-pattern knowledge, or workbench presentation. |
| Design asset pipeline | Routing across asset intake, design-system composition, UX-pattern stewardship, implementation, verification, registration, and read-only projection. | Lifecycle state transitions, production architecture, external tool sync, deployment, or unconfirmed creative choices. |

## Canonical route

Use this order as a default route map, not a mandatory sequence. Enter at the
first skill that owns the current decision frontier, then route forward only
when evidence exposes the next design-asset question.

```text
design-manage-assets
-> design-audit-product-interface when current UI structure is unknown
-> design-build-design-foundation when current tokens/themes are unknown
-> design-compose-design-system
-> design-steward-experience-patterns
-> design-apply-design-direction
-> alawas-engineering-implement-bounded-change
-> design-verify-design-implementation
-> design-audit-accessibility when accessibility conformance needs checking
-> design-critique-usability when heuristic quality needs independent evaluation
-> design-track-components
-> design-project-asset-workbench
-> alawas-governance-review-outcome-and-adapt
```

## Ownership map

| Design asset frontier | Owning skill |
|-----------------------|--------------|
| Asset identity, lifecycle status, provenance, current frontier, and next route | `design-manage-assets` |
| Existing route, layout, component, and interface discovery | `design-audit-product-interface` |
| Existing token, typography, color, spacing, and theme discovery | `design-build-design-foundation` |
| Foundation, semantic tokens, theme recipes, variants, component-family relationships, inherited/overridden/prohibited properties | `design-compose-design-system` |
| Reusable user goals, flows, states, accessibility expectations, content behavior, failure/recovery behavior, and evidence links | `design-steward-experience-patterns` |
| Confirmed creative interpretation and execution boundary | `design-apply-design-direction` |
| Reversible implementation of an accepted tracer or bounded change | `alawas-engineering-implement-bounded-change` |
| Browser-visible design parity against the confirmed direction | `design-verify-design-implementation` |
| Accessibility conformance (contrast, semantic structure) against a stewarded expectation or the WCAG generic baseline | `design-audit-accessibility` |
| Usability-heuristic evaluation independent of a confirmed direction | `design-critique-usability` |
| Durable shipped component registration, dependency edges, and component governance | `design-track-components` |
| Read-only graph, catalog, and comparison projection over canonical records | `design-project-asset-workbench` |

## Handoff rules

1. Keep asset changes inside the same Work Object when the next step tests the
   same accepted tracer, has the same consequence and sensitivity, and does not
   need a new creative decision.
2. Create a linked Work Object when the next design asset has a different
   owner, consequence, sensitivity, implementation path, or acceptance
   criteria.
3. Route to the conductor for lifecycle transitions, History entries, Evidence
   ledger entries, successor Work Objects, authority records, and any external
   effect boundary.
4. Treat external design tools, publishing, deployment, production data,
   destructive changes, schema migration, and writes outside the accepted
   bounded path as gated actions requiring scoped authority.
5. Do not let a projection change the asset truth. The workbench reads asset
   records, Work Objects, evidence, and the component ledger; it never writes
   back to them.

## Minimum handoff record

Every design-asset handoff should name:

- current Work Object ID and lifecycle state;
- current asset frontier and owning skill;
- asset identifier, asset kind, lifecycle status, and source of truth;
- evidence that made the current frontier sufficiently answered;
- open assumption or gap that belongs to the next skill;
- whether the next question stays in the same Work Object or needs a linked
  successor;
- exact creative, repository, external-tool, deployment, or destructive-action
  authority boundary.

## ReviewBadge tracer result

The first tracer for this pipeline is `ReviewBadge` in Work Object
`2026-08-22-017`. The tracer tests whether one small design asset can be
routed from intake through system composition, experience-pattern stewardship,
bounded implementation, verification, component registration, and read-only
projection without assigning one frontier to multiple owning skills.

## Revisit triggers

Revisit this pipeline when:

- real Work Object use shows recurring route ambiguity;
- a design asset step needs more than one owning skill;
- the component ledger becomes overloaded with asset-family or theme truth;
- a workbench projection starts acting like a source of truth;
- the studio needs deterministic runtime routing rather than reference
  guidance.
