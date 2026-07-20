---
name: alawas-investigate-live-question
description: "Use when one falsifiable question blocks a recommendation; gathers the smallest discriminating evidence with provenance; does not contact people, production, or sensitive sources without scoped authority."
platform: github-copilot
---
# Investigate Live Question

## Governing principle

An activated Inquiry earns movement by reducing uncertainty with attributable
evidence, not by producing a persuasive answer. Start with the smallest
question that could change the next move, preserve the distinction between
evidence and inference, and leave uncertainty visible when reality does not
support a conclusion.

## Boundaries and non-goals

This skill does:

- Frame an activated Inquiry as a falsifiable question, current hypothesis,
  stakes, and exit condition.
- Retrieve minimum-necessary source evidence, preferring attributable
  primary-source material for claims that guide the result.
- Identify missing evidence and contradictions before recommending a next move.
- Seek proportionate reality contact when the question concerns real people,
  their use, or a live environment.
- Route the Inquiry as answered, reframed, prototype-ready, or unresolved.

This skill does not:

- Treat a plausible inference, secondary summary, or model output as source
  evidence.
- Invent interviews, observations, citations, consent, or a successful
  reality-contact result.
- Contact people, use live systems, collect sensitive data, or make an
  external commitment without explicit authority.
- Implement, deploy, export, or mutate the Personal Institution archive.

## Inputs and preconditions

**Required input:** a readable, activated Inquiry Work Object in `explore`, or
an explicit route from the conductor with the Inquiry's concrete question.

**Preconditions:** The Work Object identifies its consequence and sensitivity,
contains a concrete question or hypothesis, and names the decision or next
route that the investigation can inform. If these are absent, route to
`alawas-conduct-work-object` to frame the Inquiry; do not substitute a broad research
topic.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read`, `directory_list`, and `content_search` — read the Inquiry and
  discover local system evidence.
- `web_fetch` — retrieve attributable source material at a known URL.
- `web_search` — discover candidate primary sources when they are not already
  named; without it, ask for one source or a manual lookup.
- `user_confirmation` — obtain scoped authority before reality contact or a
  new privacy, safety, or external-commitment boundary.
- `structured_output` — return a provenance-labelled inquiry record and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only source research within the approved Inquiry is allowed. A question
  about real people or use requires reality contact only when it can safely and
  proportionately test the claim; plan the contact before carrying it out.
- Before contacting a person, observing a live setting, running a live test,
  collecting personal data, or writing to an external system, state the
  purpose, minimum data, participant or system boundary, and proposed action;
  then request scoped confirmation.
- For high-consequence Inquiries, explicit confirmation must name the proposed
  Work Object mutation. Do not stage, annotate, change status, append History,
  or make any other mutation until it is received.
- A missing source, declined contact, unavailable participant, or inaccessible
  system is an evidence gap. It never becomes confirmation of the hypothesis.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Use as many progressive one-question turns as the evidence frontier requires,
while keeping each evidence move minimal:

1. **Orient:** Label what is known as `[lived]`, `[source]`, `[system]`,
   `[inference]`, `[decision]`, or `[unresolved]`; state the current
   hypothesis and missing evidence.
2. **Map:** Identify the smallest claim whose answer changes the Inquiry's
   route. Prefer primary-source evidence for that claim and name any required
   reality contact.
3. **Recommend:** Recommend one smallest safe evidence move, including why it
   resolves the most uncertainty and what it cannot establish.
4. **Ask:** Recommend before asking one decision-bearing question. Ask only
   when authority, source selection, or a reality-contact boundary is needed.
5. **Integrate:** Record observed evidence and contradictions without erasing
   the prior hypothesis. Reframe only when the new evidence makes the original
   question unhelpful.

## Skill Grilling Profile

Apply the `alawas-investigate-live-question` profile and continuous Grilling Session
in `references/SKILL-AWARE-GRILLING.md`. Frame one falsifiable question, choose
the smallest discriminating evidence move, preserve source conflicts, and test
the strongest plausible alternative before concluding

## Stage workflow

### 1. Frame the inquiry

Read the full activated Inquiry. State its question, hypothesis, intended
decision, consequence, sensitivity, exit condition, existing evidence, and
known constraints. Rewrite a vague question into one observable claim only
when the Work Object supports that wording; otherwise identify framing as the
missing evidence.

### 2. Build the evidence map

For each claim, list its required evidence, best available provenance lane,
primary source or direct observation, confidence, and disconfirming evidence.
Separate source facts from inferences in the report. If source evidence and
the hypothesis conflict, preserve both and make the contradiction the next
investigation target.

### 3. Retrieve primary-source evidence

Retrieve only sources proportionate to the decision. Attribute author,
publisher or system, date, URL or stable identifier, and the exact claim the
source supports or contradicts. A secondary account may locate a primary
source, but cannot replace it without an explicit evidence gap.

### 4. Plan and perform reality contact when relevant

When the question concerns real people or use, determine whether source
research alone can answer it. If not, recommend the minimum reality contact:
one consented conversation, observation, prototype interaction, or bounded
live-system check. Obtain scoped authority before contact. Record what was
observed, its limits, and what was not observed; do not generalize one contact
into a population claim.

### 5. Reconcile evidence and decide the route

Compare the evidence with the original hypothesis. State supporting evidence,
contradictions, missing evidence, and confidence. Route only to:

- **answered** — attributable evidence sufficiently resolves the stated
  question within its declared scope;
- **reframed** — evidence shows a different, more decision-useful question;
- **prototype-ready** — evidence supports a bounded experiment as the next
  way to learn, not as proof of the hypothesis; or
- **unresolved** — material evidence is missing, contradictory, unavailable,
  or outside authority.

## Evidence rules

- Every factual statement uses the provenance lanes in
  `references/EVIDENCE-MODEL.md`; label conclusions as `[inference]`.
- Record source evidence with attributable author or institution, date,
  durable location, relevant claim, confidence, and corroboration or
  contradiction.
- Record reality contact as `[lived]` or `[system]`, including consent or
  authorization boundary, method, observation, and limits. Never imply
  unobserved use.
- Name missing evidence as `[unresolved]`, including the consequence of acting
  without it. Do not launder a gap into confidence.

## Personal Institution handoff

Work Studio must not scan, read, or mutate the Personal Institution archive.
Personal context may enter this Inquiry only through an Approved Evidence Bridge
governed by `references/SHARED-PROTOCOL.md`. Before using one, verify
explicit user approval, this receiving Work Object, relevance, minimum-
necessary summary or stable reference, provenance, sensitivity, and limits.
Without a valid bridge, name the missing context as an evidence gap and offer
one manual, user-approved summary; never request direct archive access.

## Work Object updates

This skill returns a concise record to `alawas-conduct-work-object`, which validates
and persists it. Include the framed question and hypothesis; evidence ledger
entries with provenance and attribution; contradictions; reality-contact
authority and observations; missing evidence; recommended route; confidence;
and one concrete next move. For an unavailable write capability, return the
same record with a single manual instruction.

The conductor persists each route as a durable transition, not merely a report:

- **answered:** retain the Inquiry's `explore` state, add an `answered`
  outcome record with the bounded answer and evidence, and set `next_action`
  to the named decision or work that the answer now informs.
- **reframed:** retain `explore`, replace the active question only with the
  evidence-backed replacement, retain the original question in the outcome
  record, and set `next_action` to investigate the reframed question.
- **prototype-ready:** transition the Inquiry to `design`, add a
  `prototype-ready` outcome record naming the uncertainty to test, and set
  `next_action` to `alawas-design-tracer-bullet`. If a separate project Work Object
  is required for the prototype, the conductor creates and links that
  successor rather than silently changing the Inquiry's type.
- **unresolved:** retain `explore`, add an `unresolved` outcome record with
  the material gap and consequence, and set `status` to `waiting` only when
  an external dependency or authority is required; otherwise leave it active
  with the smallest safe evidence move as `next_action`.

Each update appends attributable History with the selected outcome, evidence
summary, rationale, and next action. For high-consequence Inquiries, the
conductor requests the already-specified scoped confirmation before mutation.

## Routing and termination

- **answered:** route to `alawas-conduct-work-object` with the bounded answer and
  evidence ledger.
- **reframed:** route to the conductor with the replacement question and why
  the original no longer governs.
- **prototype-ready:** route to `alawas-design-tracer-bullet` with the uncertainty a
  prototype should test; do not implement it.
- **unresolved:** route to the conductor with the exact gap and smallest safe
  next move. Do not force a conclusion.
- **Unavailable capability:** follow the declared manual-fallback or stop the
  affected path as unsupported; never claim research or reality contact was
  completed.

## Output template

```markdown
## Live-question investigation

- **Inquiry:** <id, question, hypothesis, intended decision>
- **Evidence:** <attributed [source], [lived], and [system] observations>
- **Inference:** <what the evidence supports, with confidence>
- **Contradictions and gaps:** <conflicting or missing evidence>
- **Reality contact:** <observed result, limit, or not needed/authorized>
- **Recommendation:** <one smallest next move>
- **Route:** <answered | reframed | prototype-ready | unresolved>
- **Durable transition:** <state, status, next_action, outcome record, and
  linked successor if any>
```

## Anti-patterns

- Writing a confident synthesis before framing the decision it must inform.
- Citing a search snippet or secondary summary as if it were a primary source.
- Treating one person's report or one prototype interaction as universal use.
- Hiding contradictory evidence to preserve the original hypothesis.
- Calling a question answered when material evidence is unavailable.
- Reading personal-memory records because they might be relevant.

## Final self-check

- Did I frame one activated Inquiry and identify the decision it informs?
- Did I distinguish evidence from inference and attribute every source claim?
- Did I name missing evidence and contradictions plainly?
- For a question about real people or use, did I seek proportionate reality
  contact or state why it was not needed, authorized, or available?
- Did I recommend one move before asking one decision-bearing question?
- Did I route only as answered, reframed, prototype-ready, or unresolved?
- Did I avoid Personal Institution archive access without an Approved Evidence
  Bridge?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `directory_list` | `list_dir` | native |
| `content_search` | `grep_search` | native |
| `web_fetch` | `open_browser_page / mcp tools` | native |
| `web_search` | `—` | manual-fallback |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |

### Capability Degradation

This adapter classifies every required capability. When a capability
is unavailable, the workflow degrades explicitly — it never pretends
that equivalent verification occurred.

**Degradation rules**:

- **`manual-fallback`**: Pause with ONE concrete manual instruction.
  Record in the Work Object what was done and what remains unverified.
  Never mark verification, export, or deployment as "successful" when
  the required capability was unavailable.
- **`unsupported`**: Stop the affected path immediately. Record the
  platform limitation. Route to a supported platform or ask the user.
- **Stricter safety wins**: When this platform imposes a stricter
  constraint than the core, the platform rule takes precedence.
  Divergences are disclosed below.

#### `web_search` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
