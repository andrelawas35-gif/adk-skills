---
name: business-manage-commercial-pipeline
default_tier: high
description: "Use when a business must qualify, advance, forecast, or close sales opportunities; produces an evidence-based pipeline decision; never contacts prospects, edits a CRM, promises terms, or treats stage labels as proof."
---
# Manage Commercial Pipeline

## Governing principle

A pipeline is a set of evidenced buying decisions in motion, not a list of
optimistic names. Keep customer need, authority, timing, value, risk, and the
next observable commitment separate so forecasts expose uncertainty.

## Boundaries and non-goals

This skill does:

- Define qualification and exit evidence for opportunity stages.
- Inspect opportunity evidence, stalled movement, concentration, conversion,
  timing, and forecast assumptions.
- Recommend one action per opportunity: advance, hold, requalify, or close.
- Separate gross pipeline, evidence-weighted forecast, and manager judgment.

This skill does not:

- Find prospects, send outreach, join calls, edit a CRM, quote prices, promise
  delivery, negotiate terms, or accept an order.
- Invent customer need, budget, authority, timing, probability, or activity.
- Turn a stage name, email count, or model score into proof of purchase intent.
- Own pricing strategy, financial approval, delivery planning, or legal review.

## Inputs and preconditions

Use an activated Work Object that names the commercial decision and its time
window. Minimum evidence is an opportunity identifier, stated customer problem,
current stage, stage-entry evidence, value basis, target date, decision actors,
known blockers, and last/next customer commitment. Missing fields remain gaps.

## Required capabilities

- `file_read` and `content_search` — inspect permitted opportunity records and
  prior decisions.
- `file_write` — return a compact pipeline record through the conductor.
- `web_fetch` — retrieve permitted market or account evidence at known sources.
- `user_confirmation` — authorize any external contact, CRM write, pricing or
  contractual commitment.
- `structured_output` — report qualification, forecast, gaps, and next route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only analysis within the approved evidence boundary is allowed.
- Contacting a person, changing a CRM, issuing a quote, promising scope or
  timing, discounting, negotiating, or accepting an order requires explicit
  scoped authority immediately before the action.
- Financial, personal, or proprietary opportunity data is private; store only
  the minimum necessary summary in the Work Object.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Outside explicit grilling,
nominate a Candidate only when missing buying evidence, forecast concentration,
or a proposed external action could materially change the recommendation.

## Skill Grilling Profile

Apply the `business-manage-commercial-pipeline` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge stage inflation, stale next
steps, single-threaded access, unsupported probabilities, and hidden loss risk.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to keep the commercial pipeline
as the sales-opportunity frontier inside the broader business operating
pipeline. Do not let opportunity-stage labels replace Work Object lifecycle
state, market evidence, financial approval, delivery planning, or customer
success outcomes.

## Stage workflow

1. Define the forecast period and exact decision: prioritization, stage change,
   forecast, or close/no-close.
2. Reconstruct each opportunity from evidence, not its label. Test customer
   problem, fit, decision process, authority, commercial feasibility, timing,
   blockers, competition or alternative, and a dated mutual next commitment.
3. Apply stage exit criteria. If evidence is missing, keep or move the
   opportunity backward; never promote it to preserve optics.
4. Separate totals into gross pipeline, qualified pipeline, evidence-weighted
   range, and explicit manager judgment. Show concentration and stale-deal risk.
5. Recommend advance, hold, requalify, or close with owner, next evidence,
   deadline, and revisit trigger. Route external execution through authority.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; preserve customer statements as
  testimony and system records as system evidence.
- A forecast probability is an inference unless calibrated against relevant
  historical outcomes. Use ranges when precision is unsupported.
- Silence, activity volume, or a changed stage is not buying evidence.

## Work Object updates

Return the decision boundary, opportunity evidence, stage assessment, forecast
range and basis, concentration/staleness risks, contradictions, gaps, recommended
action, authority needs, and revisit trigger to `conduct-work-object`.

## Routing and termination

- Financial viability question → `business-assess-financial-decision`.
- Delivery/process feasibility question → `business-improve-operating-process`.
- External action → conductor for scoped authority.
- Evidence insufficient → retain the gap and route the smallest investigation.

## Output template

```markdown
## Commercial pipeline decision
- **Scope:** <period and opportunity set>
- **Qualification:** <stage evidence and gaps>
- **Forecast:** <gross, qualified, range, and basis>
- **Risks:** <staleness, concentration, blockers, contrary evidence>
- **Actions:** <advance | hold | requalify | close, owner, date>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Did stage movement follow exit evidence rather than optimism?
- Are forecast inference, manager judgment, and system facts separate?
- Is every external or commercial commitment gated?
