---
name: review-outcome-and-adapt
description: >
  Compare a Work Object hypothesis with proportionate lived and system outcomes,
  distinguish shipped output from observed value, and route a user-chosen next
  direction without overstating evidence or mutating the original work.
---

# Review Outcome and Adapt

## Governing principle

Review is a learning boundary, not a victory lap. Compare the hypothesis with
what was actually shipped and what was actually observed, keep evidence,
inference, decision, and uncertainty distinct, then let the user choose the
smallest justified next direction.

## Boundaries and non-goals

This skill does:

- Review an `observe` or `close` Work Object against its recorded hypothesis
  and proportionate lived or system outcomes.
- Separate shipped output from observed value, and distinguish evidence,
  inference, decision, and unresolved uncertainty.
- Recommend one bounded next direction before asking the user to choose:
  `stop`, `repeat`, `deepen`, `repair`, `share`, or `create successor`.
- Route a user-authorized successor through `conduct-work-object` as a separate
  correctly typed Work Object with its own authority boundary.

This skill does not:

- Invent an outcome, use a shipped artifact as proof of value, or treat lack of
  observation as confirmation or failure.
- Automatically create a successor, change the original Work Object's type, or
  turn a review into implementation, deployment, export, or external contact.
- Establish analytics, telemetry, a new schema, a generalized outcome taxonomy,
  or a production reporting system.

## Inputs and preconditions

**Required input:** a readable Work Object in `observe` or `close` with a
recorded hypothesis or explicit hypothesis gap, consequence and sensitivity,
available lived or system evidence, and its current authority boundary.

**Preconditions:** `conduct-work-object` has discovered the Work Object. If
the hypothesis, outcome evidence, or review authority is missing, record the
gap and route the smallest safe observation or decision move; do not infer a
review result.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` and `content_search` — read the Work Object, its hypothesis,
  prior evidence, and permitted local outcome records.
- `file_write` — pass a concise review record to `conduct-work-object` for
  durable persistence.
- `user_confirmation` — obtain the user's selected direction and any scoped
  authority needed for successor creation.
- `structured_output` — return an attributable outcome comparison, uncertainty
  boundary, decision, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Reading and recommending do not authorize a successor, implementation,
  external contact, sharing, or closure.
- A low- or meaningful-consequence review may be recorded after the user
  accepts the selected direction. A high-consequence review or successor
  mutation requires confirmation naming that exact mutation.
- For a high-consequence Work Object, confirmation must name the exact review
  or successor mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before that confirmation.
- `share` identifies a candidate audience and boundary but does not export or
  publish. `repair` and `deepen` identify bounded follow-up work but do not
  implement it.
- A successor is created only after the user explicitly chooses `create
  successor`, names its type and bounded outcome, and supplies the authority
  required by its consequence.

## Agreement Loop behavior

Apply the shared conversational inquiry contract in
`references/AGREEMENT-LOOP.md`: give a recommendation before one question,
maintain coverage of material branches, and continue without an arbitrary
question cap until the user and evidence establish the next safe move.

When a review outcome needs a direction, state the recorded hypothesis,
available evidence, inference, unresolved uncertainty, and consequence.
Recommend the smallest direction justified by those facts before asking one
decision-bearing question. Do not ask for blanket authority to create future
work, share a result, or improve adjacent systems.

## Skill Grilling Profile

Apply the `review-outcome-and-adapt` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Compare technical behavior, intended
outcome, and unintended effects independently; challenge attribution, aggregate
success, subgroup harm, and the earliest invalid upstream assumption. On
direct entry, route through `conduct-work-object` first. Return the compact
continuity record; do not reset context, store a transcript, or mutate the Work
Object.

## Stage workflow

### 1. Reconstruct the review boundary

Read the hypothesis, intended outcome, shipped output, prior evidence,
consequence, sensitivity, and authority. Label unavailable information as an
explicit gap. A completed deliverable is shipped output; it is not observed
value unless attributable outcome evidence supports that inference.

### 2. Compare hypothesis and outcomes

Record minimum-necessary `[system]` and `[lived]` evidence separately from
`[inference]`. State whether the available evidence confirms, contradicts, or
is insufficient to assess the hypothesis. Preserve disconfirming evidence and
the original hypothesis; never rewrite either to make a result fit.

### 3. Handle insufficient observation safely

If the hypothesis or outcome evidence is missing, select `insufficient
observation`. Record the missing evidence, affected decision, consequence, and
one concrete revisit trigger. Do not claim observed value, confirmation,
contradiction, completion, or closure. Route to the smallest authorized
observation, investigation, or decision move.

### 4. Recommend and select a bounded direction

Recommend one of `stop`, `repeat`, `deepen`, `repair`, `share`, or `create
successor`, including its trade-off. Ask the user to accept, reject, or change
that one direction. `stop` closes only through the conductor's applicable
authority; `repeat`, `deepen`, and `repair` remain bounded follow-up proposals;
and `share` remains a proposal until separate sharing authority exists.

### 5. Create a successor only through the conductor

When the user selects `create successor`, collect the successor's immutable
type, one bounded outcome, consequence, sensitivity, owner, acceptance
evidence, and relationship to the reviewed Work Object. Route this record to
`conduct-work-object`, which creates the separate Work Object and preserves the
original type and history. Do not create a successor when any required field or
authority is absent.

## Evidence rules

- Label observations `[system]` or `[lived]`, review choices `[decision]`,
  interpretations `[inference]`, and unavailable information `[unresolved]`
  according to `references/EVIDENCE-MODEL.md`.
- Retain the distinction between shipped output and observed value in the
  durable review record.
- Capture only minimum-necessary local evidence. Do not scan personal archives
  or contact people or external systems without separate scoped authority.
- An unrun observation plan is an uncertainty, never outcome evidence.

## Work Object updates

Return a concise record to `conduct-work-object` containing the hypothesis,
shipped output, attributable lived and system evidence, inference, unresolved
uncertainty, selected direction, rationale, next action, and revisit trigger.
For a successor, include its type, bounded outcome, consequence, sensitivity,
owner, acceptance evidence, and typed relationship. The conductor owns schema
validation, state/status transitions, History, and successor creation.

## Routing and termination

- **Confirmed outcome:** record the evidence and user-selected direction; do
  not treat confirmation as automatic closure.
- **Contradicted hypothesis:** preserve the contradiction and route the chosen
  bounded repair, deeper inquiry, or stop decision.
- **Insufficient observation:** retain `observe` or `close` as appropriate,
  make the gap explicit, and route the smallest authorized evidence move.
- **Successor selected:** route to `conduct-work-object` for a separate linked
  Work Object; never mutate the original type.
- **Manual-fallback capability:** pause with one concrete user-run observation
  instruction and mark the associated outcome unverified.
- **Unsupported capability:** stop the affected route, record the limitation,
  and route to a supported platform or the user.

## Output template

```markdown
## Outcome review

- **Work Object and boundary:** <id, state, consequence, authority>
- **Hypothesis and shipped output:** <recorded hypothesis and delivered artifact>
- **Observed outcomes:** <attributable [system] and [lived] evidence>
- **Assessment:** <confirmed | contradicted | insufficient observation, with inference>
- **Uncertainty:** <gaps, consequence, and revisit trigger>
- **Recommended direction:** <one bounded direction and trade-off>
- **Decision status:** <proposed | accepted and recorded | awaiting authority>
- **Successor:** <none | separately typed linked Work Object>
- **Next route:** <conductor | investigate | decision | manual fallback>
```

## Anti-patterns

- Calling delivery proof of value without observed evidence.
- Rewriting a hypothesis after contradictory outcomes appear.
- Turning insufficient observation into a positive or negative result.
- Automatically creating a successor or changing the reviewed Work Object's
  type in place.
- Treating `share` as authority to export or `repair` as authority to implement.

## Final self-check

- Did I separate shipped output, observed evidence, inference, decision, and
  uncertainty?
- Is the assessment confirmed, contradicted, or insufficient observation based
  only on attributable evidence?
- Did I recommend one bounded direction before asking for a decision?
- Is any successor separate, correctly typed, linked, and independently
  authorized?
- Did I avoid implementation, sharing, export, deployment, and external
  contact without separate authority?
