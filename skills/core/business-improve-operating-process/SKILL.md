---
name: business-improve-operating-process
default_tier: high
description: "Use when recurring business work must be mapped, stabilized, measured, or improved; designs an evidence-backed process experiment; never changes a live operation, staffing, supplier, or control without scoped authority."
---
# Improve Operating Process

## Governing principle

Improve the flow that creates customer value, not an isolated task metric.
Observe the current process, distinguish demand from failure demand, find the
constraint, and test the smallest safer future state before standardizing it.

## Boundaries and non-goals

This skill does:

- Define process purpose, customer, trigger, outcome, boundary, owner, demand,
  inputs, outputs, steps, queues, controls, handoffs, and measures.
- Map current material and information flow using direct evidence.
- Identify bottlenecks, rework, delay, variation, failure demand, and control gaps.
- Design a bounded future-state experiment with safeguards and rollback.

This skill does not:

- Change a live process, schedule, staffing level, supplier, control, inventory,
  customer promise, or production system without explicit scoped authority.
- Assume every wait is waste, optimize one step at the expense of the whole,
  or treat documentation as proof of actual work.
- Replace incident response when harm is active or compliance review when required.

## Inputs and preconditions

Use an activated Work Object naming one recurring value stream or process,
customer/outcome, current problem, boundary, owner, consequence, and available
observations. If actual work has not been observed, label the map provisional.

## Required capabilities

- `file_read`, `directory_list`, and `content_search` — inspect permitted process evidence.
- `file_write` — return the current/future-state record through the conductor.
- `terminal_run` — calculate cycle, queue, error, or capacity measures locally.
- `user_confirmation` — authorize observation of people/live systems or any operational change.
- `structured_output` — report map, constraint, experiment, safeguards, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only artifact inspection is allowed. Observing people or live systems,
  collecting operational data, or running a process experiment requires scoped
  authority when not already covered by the Work Object.
- Changes to staffing, suppliers, customer commitments, financial controls,
  safety controls, production, or regulated work require separate explicit authority.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
current-state map lacks direct observation, local optimization could harm the
whole, or the proposed experiment crosses a control or people boundary.

## Skill Grilling Profile

Apply the `business-improve-operating-process` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge map/reality gaps, bottleneck
misidentification, demand assumptions, rework concealment, and unsafe standardization.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
recurring operating-process frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define purpose, customer, trigger, terminal outcome, boundaries, owner, and
   outcome/guardrail measures.
2. Capture the actual current state: demand arrival, steps, decisions, handoffs,
   queues, work time, elapsed time, defects/rework, controls, and information flow.
3. Separate value creation, necessary control, delay, and failure demand. Locate
   the system constraint and test contrary explanations.
4. Design the smallest future-state experiment that changes flow at the
   constraint, with owner, sample/window, success/failure signals, stop condition,
   affected groups, and rollback.
5. Recommend test, investigate, stabilize, or stop. Standardize only after
   observed evidence supports the change and the owner accepts it.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; a documented procedure is not evidence
  that work follows it.
- Report work time and elapsed time separately; keep averages from hiding tails or subgroup harm.
- A local improvement is not system improvement unless end-to-end outcomes and guardrails hold.

## Work Object updates

Return process boundary, current-state evidence, measures, constraint hypothesis,
contradictions, future-state experiment, affected groups, controls, stop/rollback,
authority needs, and revisit trigger to `conduct-work-object`.

## Routing and termination

- Active harm → `operations-diagnose-production-incident`.
- Implementation after accepted experiment → `engineering-implement-bounded-change`.
- Financial trade-off → `business-assess-financial-decision`.
- Staffing/accountability trade-off → `business-plan-workforce-accountability`.

## Output template

```markdown
## Operating-process improvement
- **Purpose and boundary:** <customer, trigger, outcome, owner>
- **Current state:** <flow, measures, queues, rework, controls>
- **Constraint:** <hypothesis, evidence, alternatives>
- **Future-state experiment:** <change, window, safeguards, rollback>
- **Decision:** <test | investigate | stabilize | stop>
- **Authority and route:** <exact operational boundary and next skill>
```

## Final self-check

- Is the current state grounded in actual evidence and marked provisional when not?
- Does the experiment improve end-to-end outcomes with guardrails?
- Is every live operational change separately authorized?
