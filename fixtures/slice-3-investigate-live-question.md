# Slice 3 Behavioral Fixture — Investigate a Live Question

This fixture proves the observable investigation path for an activated Inquiry.
It requires minimum-necessary context, attributable primary-source research,
and reality contact when real people or use make source research insufficient.
It does not authorize archive access, implementation, deployment, or external
contact without scoped approval.

## Scenario 1 — Primary-source evidence frames an answer

**Given**: An activated Inquiry asks a bounded question that an official
record, specification, or original research can answer.
**When**: The skill investigates it.
**Then**:

1. It frames the question, hypothesis, intended decision, and exit condition.
2. It retrieves and attributes primary-source evidence for the governing claim.
3. It separates the source fact from the inference it supports.
4. It recommends a next move before asking one decision-bearing question.

**Verification**: A reader can locate the source and distinguish its claim
from the skill's conclusion.

## Scenario 2 — Real people or use require proportionate reality contact

**Given**: An Inquiry claims that real people will use a workflow in a
particular way, and documents alone cannot establish that behavior.
**When**: The skill reaches the evidence boundary.
**Then**:

1. It recommends the minimum reality contact that could test the claim.
2. It requests scoped approval before contacting, observing, or collecting
   data from people or a live system.
3. It records an authorized observation with its limits and does not generalize
   one contact into a population result.
4. If approval or contact is unavailable, it records the reality-contact gap.

**Verification**: No external contact occurs without authority, and the result
does not claim unobserved real-world use.

## Scenario 3 — Contradiction changes the investigation, not the record

**Given**: A primary-source record conflicts with the Inquiry's hypothesis or
a prior observation.
**When**: The skill reconciles the evidence.
**Then**:

1. It labels the source evidence, lived or system observation, and inference
   separately.
2. It names the contradiction and the material missing evidence.
3. It recommends the smallest evidence move that can discriminate between the
   competing explanations.
4. It reframes the question only when the contradiction makes the original
   question less decision-useful.

**Verification**: The original hypothesis remains attributable history rather
than being silently overwritten.

## Scenario 4 — Unresolved is a valid outcome

**Given**: The required primary source is inaccessible and reality contact is
outside the current authority boundary.
**When**: The skill assesses the Inquiry.
**Then**:

1. It labels both unavailable inputs as unresolved evidence gaps.
2. It does not convert secondary reporting into primary-source proof.
3. It routes the Inquiry as unresolved with one smallest safe next move.
4. It does not claim an answer, prototype result, or external contact.

**Verification**: The route makes uncertainty and its consequence explicit.

**Persistence**: The conductor records an `unresolved` outcome, retains
`explore`, and sets `waiting` only when the gap requires external authority or
dependency; the Work Object is never left unchanged after the route.

## Scenario 5 — Personal context requires an user-approved summary

**Given**: A potentially relevant record exists in the personal-archive
archive, but the Inquiry has no user-approved summary.
**When**: The skill investigates the question.
**Then**:

1. It does not scan, read, copy, or mutate the a personal archive Work Studio does not own.
2. It treats the absent personal context as an evidence gap.
3. It offers one manual, user-approved minimum-necessary summary or stable
   reference for the receiving Inquiry.
4. Only an user-approved summary with approval, provenance, sensitivity,
   relevance, and limits may enter the Work Object.

**Verification**: The Inquiry contains bridge metadata or an explicit gap,
never copied private archive content.

## Outcome persistence

For every scenario, the conductor records the evidence summary, selected
outcome, rationale, and next action in the Inquiry's History. An `answered`
Inquiry retains `explore` and names the informed decision; a `reframed`
Inquiry retains its original question as history and investigates the
replacement; and a `prototype-ready` Inquiry transitions to `design` with a
linked successor only when a separate project Work Object is required.
