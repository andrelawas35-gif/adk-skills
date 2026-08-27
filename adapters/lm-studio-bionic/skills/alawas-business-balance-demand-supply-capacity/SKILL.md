---
name: alawas-business-balance-demand-supply-capacity
description: "Use when demand, supply, capacity, inventory, constraints, and exception actions must become a feasible operating plan; never issues schedules, purchase orders, customer promises, staffing changes, or live-system writes without scoped authority."
default_tier: high
platform: lm-studio-bionic
---
# Balance Demand, Supply, and Capacity

## Governing principle

A feasible plan is a negotiated constraint model, not a demand wish. Keep
demand confidence, supply availability, capacity, inventory, bottlenecks,
service commitments, exceptions, and authority boundaries visible before work
is scheduled or promised.

## Boundaries and non-goals

This skill does:

- Reconcile demand signals, supply availability, capacity, inventory, backlog,
  constraints, and exception rules into a feasible operating-plan recommendation.
- Expose bottlenecks, scenario options, guardrails, escalation paths, and
  revisit cadence.
- Route commercial, supplier, workforce, process, delivery, cash, or risk gaps.

This skill does not:

- Issue production schedules, purchase orders, customer promises, ERP/MRP/CRM
  changes, staffing changes, or inventory moves.
- Redesign the recurring process, select suppliers, qualify opportunities, or
  approve money movement.
- Treat forecast demand as committed demand or nominal capacity as usable capacity.

## Inputs and preconditions

Use an activated Work Object with planning horizon, demand signal, supply
availability, capacity basis, inventory/service policy, backlog, constraints,
owner, exception rules, and the operating decision that must be made now.

## Required capabilities

- `file_read` and `content_search` — inspect permitted demand, supply,
  inventory, capacity, backlog, process, supplier, and customer evidence.
- `terminal_run` — run reproducible local capacity or scenario checks when useful.
- `file_write` — return a compact operating-plan recommendation through the
  conductor.
- `user_confirmation` — authorize schedules, purchase orders, staffing changes,
  customer promises, inventory actions, or live-system writes.
- `structured_output` — report feasibility, constraints, scenarios, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only feasibility analysis within the approved evidence boundary is allowed.
- Production schedules, purchase orders, inventory moves, customer delivery
  promises, supplier commitments, staffing changes, and live ERP/MRP/CRM writes
  require explicit scoped authority.
- Customer, supplier, workforce, inventory, and operational data may be private;
  store only minimum necessary summaries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before receiving that scoped confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when demand
confidence, nominal capacity, supplier lead time, inventory policy, or an
exception action could reverse the feasible plan.

## Skill Grilling Profile

Apply the `alawas-business-balance-demand-supply-capacity` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge demand-as-commitment, nominal
capacity, hidden bottlenecks, supplier optimism, inventory blindness, and
unapproved customer promises.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
demand/supply/capacity feasibility frontier from the Work Object lifecycle and
the commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define horizon, owner, service objective, planning boundary, demand signal,
   supply/capacity boundary, and excluded execution actions.
2. Inspect demand confidence, backlog, available capacity, supplier/material
   constraints, inventory policy, lead times, bottlenecks, quality limits, and
   cash or risk constraints.
3. Build feasible base/downside/upside options and identify the binding
   constraint. Separate committed demand from forecast, and nominal capacity
   from usable capacity.
4. Compare fulfill, level-load, prioritize, defer, source, add capacity, reduce
   scope, or escalate options with guardrails and exception rules.
5. Recommend an operating-plan choice with evidence gaps, owner, authority
   needs, revisit cadence, and downstream routes.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A forecast is not committed demand; a capacity number is not usable capacity
  without constraint, availability, and quality evidence.
- A feasible-plan recommendation is not a production schedule or customer promise.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the planning boundary, demand and supply evidence, capacity model,
constraint, scenarios, recommended plan, exceptions, authority needs, routes,
and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Demand/source uncertainty -> `alawas-business-manage-market-intelligence`,
  `alawas-business-manage-commercial-pipeline`, or `alawas-business-manage-customer-success`.
- Supplier constraint -> `alawas-business-source-and-govern-suppliers`.
- Workforce constraint -> `alawas-business-plan-workforce-accountability`.
- Process bottleneck -> `alawas-business-improve-operating-process`.
- Delivery commitment -> `alawas-business-direct-project-delivery`.
- Cash/inventory consequence -> `alawas-business-manage-liquidity-and-cash-runway`.
- Schedule, purchase, inventory, staffing, customer promise, or live-system
  action -> conductor for scoped authority.

## Output template

Apply `references/DIRECTOR-LANGUAGE.md` to everything said to the
director. Lead with plain meaning; attach the technical term to the explanation
rather than substituting it. Order anything worth explaining as: what's
happening, why it matters, the technical term, the evidence, the
recommendation, what needs deciding. Short answers stay short, and any part may
be marked absent — "Evidence: none, this is inference" is valid and preferred.
Never fill a part to complete the shape. Never phrase a decision in terms the
director must decode before choosing. Record content is never translated:
field names, state names, record IDs, and file paths stay exact.

```markdown
## Demand, supply, and capacity decision
- **Scope:** <horizon, owner, service objective, boundary>
- **Evidence:** <demand, supply, capacity, backlog, inventory, constraints>
- **Scenarios and constraint:** <base, downside, upside and bottleneck>
- **Plan:** <fulfill | level-load | prioritize | defer | source | add capacity | reduce scope | escalate>
- **Exceptions and gaps:** <authority boundary, weak evidence, guardrails>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are forecast demand, committed demand, nominal capacity, and usable capacity separate?
- Is the binding constraint and exception rule explicit?
- Is every schedule, purchase, promise, staffing change, inventory move, or system write gated?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **full 6‑tag system** (`references/epistemic/epistemic-rules-full.md`).

The epistemic tier is resolved from the skill's `default_tier` (high).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: high`.
The platform overlay resolves this to `Qwen3.5-9B Q4`.
The prompt budget for this tier is approximately 32000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `native project file access (Read file)` | native |
| `content_search` | `Search (native project index)` | native |
| `terminal_run` | `Shell tool (native, coding projects)` | native |
| `file_write` | `Edit / write file (native coding tools)` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `Structured output (native, per-session schema)` | native |
