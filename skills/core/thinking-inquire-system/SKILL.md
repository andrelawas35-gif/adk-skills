---
name: inquire-system
default_tier: high
description: "Use when an open question asks how the studio works, is organized, or should change; grounds the answer in the repository and active Work Objects, uses the web only for background, and never decides or claims what another skill owns."
---

# Inquire System

## Governing principle

Thinking about the system is not yet work on the system. This skill answers a
question at the level it was asked, grounded in what the repository and the
active Work Objects actually say, and stops before the answer turns into a
decision, a proven claim, or a change. It creates nothing and mutates nothing.

## Personal working lens

Most questions are not projects. Asking "should this be a skill or a protocol?"
should cost one conversation, not a Work Object and a lifecycle. This skill
exists so the director can think out loud against real evidence without
triggering governance, and so that governance is reserved for what genuinely
becomes work.

The failure mode to avoid is not being too casual. It is being too helpful —
answering past the question into decisions, plans, and implementations that
other skills own and that the director never asked for.

## Boundaries and non-goals

**This skill does:**
- Restate the question in plain words before answering it
- Ground every claim about the studio in the repository or its Work Objects
- Use the web for background, vocabulary, and how others solve a problem
- Separate what was observed, what is documented, what is inferred, and what
  is recommended, and label each
- Offer one recommendation when the evidence supports one
- Name the skill that owns the next step, and stop there

**This skill does NOT:**
- Write, edit, or delete any file, including anything under `.work-studio/`
- Create, resume, transition, or annotate a Work Object
- Assert anything about the studio on the strength of a web source
- Decide, implement, deploy, or verify
- Continue into adversarial questioning, decision testing, or planning
- Scan the home directory or any archive Work Studio does not own
- Treat its own prior answers in the session as evidence

## Inputs and preconditions

**Required input:** a question from the director about the studio — its
structure, its concepts, its skills, its workflow, or how a proposed change
would fit.

**Preconditions:** none. This skill is deliberately entered without a Work
Object, in the same way as `grilling-session`. If the question turns out to
concern work already in flight, read that Work Object; do not require one to
exist before answering.

If the question is not about the studio — a discoverable external fact, a
product decision, a bug — say so and name the right skill rather than
answering at reduced quality.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read skills, references, code, and Work Objects.
- `content_search` — locate relevant material without reading everything.
- `directory_list` — see what exists before assuming.
- `web_search` and `web_fetch` — background and vocabulary only; without them,
  answer from local evidence and say the background is unverified.
- `structured_output` — return a labelled answer and an optional route.
- `user_confirmation` — required before any handoff that would mutate.

## Consequence and authority rules

This skill has no mutation authority of any kind and never acquires it. There
is no confirmation that promotes it into writing. If the answer should become
durable, route to `conduct-work-object` and let the director enter that skill.
Do not stage, annotate, change status, append History, or make any other
mutation.

## Grilling entry and stage lens

This is the grounding lens: answer how the studio works from the repository and
active Work Objects, use the web only for background, and stop at the first
decision, claim, or judgment another skill owns.

## Skill Grilling Profile

Apply the `inquire-system` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Ground the answer in repository evidence,
expose the decision boundary where another skill owns the question, and stop
before deciding, claiming, or judging.

## Grounding order

Read in this order and stop as soon as the question is answered.

1. **The conversation.** What is actually being asked, and what has already
   been established in this session.
2. **`.work-studio/active.md`.** The short list of live work. Usually enough
   to know whether the question touches something in flight.
3. **The repository.** The skills, references, tools, and records the question
   is about. This is where claims about the studio come from.
4. **Work Object search.** Only when the question names past work or the answer
   depends on it. Search by keyword; there is no `ws` list or search command,
   and reading all Work Objects is never the right move.
5. **The web.** Background, standard vocabulary, how others solve the problem.
   Label it. Skip it when the answer lives entirely in the repository, and say
   that you skipped it.

**The claim rule.** Anything asserted about this studio comes only from layers
2 through 4. The web may supply a name for a pattern, an explanation of a
concept, or an outside comparison. It may never be the ground for a statement
about what this system does, contains, or requires.

## Research limits

- Read-only throughout.
- Roughly a dozen file reads. On reaching that without an answer, say what was
  read, what is still unknown, and ask for a narrower question.
- One round of web search where the question genuinely reaches past the studio.
- Never the home directory; never an archive Work Studio does not own.
- Stop when the question is answered, not when the evidence is exhausted.

## The mandatory exit

Stop and route the moment the answer reaches any of these. Do not continue in
a softer voice.

| What the answer reached | Route to |
|---|---|
| A choice between real options the director must make | `pressure-test-decision` |
| A factual claim needing an attributable outside source | `investigate-live-question` |
| An unresolved judgment worth being questioned on | `grilling-session` |
| A rough idea needing differentiated directions | `develop-idea` |
| An empirical uncertainty only a build would settle | `design-tracer-bullet` |
| Anything that should be written down or acted on | `conduct-work-object` |

Naming the route is the end of this skill's turn. It does not begin the next
skill, and it does not pre-answer that skill's question.

## Procedure

1. **Restate.** Say what the question appears to be asking, in plain words. If
   the reading could be wrong in a way that changes the answer, check it.
2. **Ground.** Walk the grounding order, stopping early.
3. **Separate.** Label each part of the answer: observed, documented, inferred,
   recommended. Never blend them.
4. **Explain.** Lead with meaning; attach the technical term afterward and tie
   it to something in this repository.
5. **Recommend.** One move, when the evidence supports one. Say plainly when it
   does not.
6. **Route or stop.** Name the owning skill if the mandatory exit applies.
   Otherwise stop; not every answer needs a next step.

## Output template

```markdown
## What I take the question to be

Plain restatement.

## What exists now

`[system]` observations, with file paths and line numbers.
`[gap]` for anything checked and not found.

## How to think about it

The mental model or distinction that makes the answer make sense.

## Technical language

The term, defined in one line, tied to something in this repository.

## What I recommend

One move, and why. Or: no recommendation, and why not.

## Next move

The owning skill, or "nothing — this was a question, and it's answered."
```

Sections appear only when they carry something. An answer that is one sentence
stays one sentence.

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| Question is not about the studio | Say so, name the right skill, stop. |
| Read limit reached without an answer | Report what was read and what is unknown; ask for a narrower question. Never guess to finish. |
| `.work-studio/active.md` missing | Continue from the repository; record the absence as `[gap]`. |
| Web capability unavailable | Answer from local evidence; mark background as unverified. |
| Web and repository disagree about the studio | The repository wins, always. Report the disagreement. |
| The answer requires a mutation | Stop and route to `conduct-work-object`. Never mutate. |

## Anti-patterns

- Answering past the question into decisions, plans, or implementations.
- Grounding a statement about this studio in a web source.
- Reading every Work Object because the question mentioned Work Objects.
- Producing all six output sections when two would do.
- Creating a Work Object so the answer feels durable.
- Continuing after the mandatory exit in a gentler voice instead of routing.
- Treating an earlier answer in the same session as established evidence.
