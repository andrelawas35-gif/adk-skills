# Epistemic Loop Mapping

Non-binding cross-reference. Per Work Object `2026-08-22-001` Decision 1: a
proposal to add a formal `Evidence -> Hypothesis -> Prediction -> Test -> New
Evidence -> Judgment -> Decision -> Action -> Outcome -> Revision` loop as a
new tracked Work Object mechanism was tested and rejected — every stage
already exists, distributed across existing skills and fields under
different names. This document exists only so that mapping is discoverable
without re-deriving it. It changes no schema, template, or validator, and it
is not a required reading for any skill.

| Loop stage | Already implemented as |
|---|---|
| Evidence | The Work Object's Evidence ledger (`references/EVIDENCE-MODEL.md`, `references/AGREEMENT-LOOP.md`) |
| Hypothesis | `alawas-thinking-pressure-test-decision`'s "Branch chosen" + alternatives considered; `alawas-design-design-tracer-bullet`'s "riskiest falsifiable assumption" |
| Prediction | `alawas-thinking-pressure-test-decision` Stage 6, "Test the confirmed choice" — the edge case and invalidating assumption surfaced before recording |
| Test | `alawas-design-design-tracer-bullet`'s "observable exit evidence" for that falsifiable assumption |
| New Evidence | New Evidence ledger entries appended after the test runs |
| Judgment | The Decision record's `Rationale` and `Confidence` fields |
| Decision | The Decision record itself (`## Decisions and revisit triggers`) |
| Action | `alawas-engineering-implement-bounded-change` / `alawas-operations-deploy-with-recovery` |
| Outcome | `alawas-governance-review-outcome-and-adapt` — "Compare the hypothesis with what was actually shipped and what was actually observed" |
| Revision | The Decision record's `Revisit trigger` firing, producing a new dated Decision entry |

**Revisit trigger** (carried from Decision 1): if a concrete need arises to
query, group, filter, or automate over Work Objects by loop-stage — not
merely a preference for the loop's naming to feel more explicit — revisit
toward a formal, schema-tracked mechanism instead of this mapping.
