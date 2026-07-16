Developer: Reload Window
# Andrelawas Work Studio — Accepted Planning Record

Date: 2026-07-15  
Status: Planning accepted; implementation not started  
Origin: Grilling session grounded in the Personal Knowledge Manager project,
Matt Pocock's engineering skills, and the Andrelawas Personal Institution
skills.

## Purpose

Andrelawas Work Studio is a portable personal operating system for moving from
a live signal or idea to reality-tested work, deployment, observation, and
post-deployment repair. It must preserve user authority, distinguish evidence
from inference, produce durable artifacts, and adapt through reviewed outcomes
rather than inferred identity.

The Personal Knowledge Manager supplies reviewed memory and evidence. It does
not define the user's identity or working method.

## Governing architecture

Use a thin conductor with focused skills. The conductor interprets state,
enforces gates, and routes work. Specialists own domain behavior. Routing is
state-based rather than a mandatory linear pipeline.

The canonical unit is a **Work Object**. Chats are interaction surfaces; Work
Objects are continuity surfaces.

### Work Object types

- **Inquiry** — resolves an uncertain question through research or reality
  contact.
- **Project** — turns a live question into a bounded artifact or capability.
- **Change** — modifies an existing system through design, implementation, and
  verification.
- **Incident** — restores expected behavior after an operational failure.

An idea is provisional input. It becomes durable only when activated as one of
these types.

### Lifecycle states

1. Notice
2. Frame
3. Explore
4. Decide
5. Design
6. Build
7. Verify
8. Release
9. Observe
10. Close

These are available states, not compulsory stops. Evidence may require moving
backward.

### Work status

- **Active** — receiving current effort with a concrete next move.
- **Waiting** — depends on a known external event, person, elapsed period, or
  environment change.
- **Paused** — deliberately deprioritized with a revisit trigger.
- **Blocked** — repeated attempts establish that progress requires new
  authority, information, or external state.
- **Closed** — completed, stopped, superseded, or abandoned with the reason
  recorded.

## Shared reasoning protocol

Every skill is compatible with the **Agreement Loop**, but the loop activates
only at unresolved decision boundaries:

1. Orient to the Work Object, memory, evidence, consequence, and state.
2. Map unresolved branches, dependencies, and contradictions.
3. Give one recommended answer with evidence and trade-offs.
4. Ask one decision-bearing question.
5. Integrate the user's answer.
6. Generate novelty only when it changes the option space.
7. Test the emerging agreement with an edge case or failure scenario.
8. Converge or route to a more useful workflow.

The loop stops when agreement is sufficient, action or external evidence is
needed, further questions will not change the recommendation, the user proceeds
with documented uncertainty, or another skill is more appropriate.

### Adjacent Possibility Pass

During Explore, Decide, or Design, a skill may:

1. Identify the dominant assumption.
2. Find a contradiction, neglected actor, missing scale, or boundary condition.
3. Transform one dimension such as actor, incentive, medium, timing, ownership,
   scale, interface, or constraint.
4. Generate at most three materially distinct possibilities.
5. State the changed assumption, fit with evidence, new possibility, cost, and
   smallest reality test.
6. Recommend one option or retaining the original design.

Novel ideas cannot enter Build without framing and a bounded reality test.

## Evidence and authority

### Provenance lanes

- **Lived Evidence** — dated observations, conversations, field encounters, and
  direct experience.
- **Source Evidence** — papers, documentation, laws, records, and attributable
  external material.
- **System Evidence** — code, tests, logs, metrics, browser checks, and
  deployment results.
- **Inference** — interpretation connecting available evidence.
- **Decision** — a human-owned choice with alternatives, rationale, and revisit
  trigger.

Memory retrieves records into these lanes; memory is not itself evidence.

### Consequence levels

- **Low** — private, cheap, and reversible. Stages may be compressed.
- **Meaningful** — affects durable data, substantial effort, public artifacts,
  or other people. Framing, decision, and verification evidence are required.
- **High** — affects safety, privacy, money, production, irreversible data,
  identity claims, or external commitments. Explicit human authority,
  verification, recovery, and observation are required.

Consequence follows effects, not emotional intensity or urgency.

### Sensitivity classes

- **Ordinary** — normal project information.
- **Private** — personal, proprietary, financial, relationship, or internal
  operational information.
- **Restricted** — credentials, intimate regulation history, security-sensitive
  infrastructure, identity documents, or similarly harmful material.

Sensitivity and consequence are independent. Store the minimum required,
exclude secrets, and link to protected sources rather than copying them.

## Personalization governance

Observed behavior does not silently become identity or a permanent rule.

1. Record an observation with provenance.
2. Propose a **Workflow Candidate** with supporting and contrary evidence.
3. Test it in bounded Work Objects.
4. Ask for confirmation before promotion.
5. Store confirmed rules with scope, exceptions, confidence, and revisit trigger.
6. Retire or revise rules when outcomes contradict them.

Initial provisional WIP candidate: one Primary Work Object receiving build or
deployment effort, plus at most two Supporting Work Objects limited to inquiry,
waiting, or maintenance. Review after five completed Work Objects.

## Skill family

### `conduct-work-object`

Detect existing or new work, retrieve minimal context, infer type/state/
consequence, identify the highest-leverage unresolved condition, route to the
right specialist, enforce authority gates, detect stalled or recursive loops,
and close only through outcome review. It contains little domain logic.

### `turn-signal-into-work`

Capture the signal in the user's language, retrieve related records, classify
it as discard/remember/incubate/activate, and create a Work Object only after
activation. Optimize for preserving attention rather than maximizing projects.

### `investigate-live-question`

Compose personal memory, Project Studio, and primary-source research. Define a
revisable hypothesis, identify missing evidence, require reality contact where
the question concerns actual people or use, and finish answered, reframed,
prototype-ready, or unresolved.

### `pressure-test-decision`

Compose grilling and domain modeling. Retrieve discoverable facts, walk one
decision branch at a time, recommend before asking, sharpen language, test edge
cases, preserve disagreement, and create ADRs only for hard-to-reverse,
surprising, genuine trade-offs.

### `design-tracer-bullet`

Compose domain modeling, codebase design, and prototyping. Identify the riskiest
assumption, define the smallest end-to-end slice, prefer deep modules, specify
state/authorization/failure/observability, and include non-goals and rollback.

### `implement-bounded-change`

Compose TDD and relevant domain skills. Inspect repository state, preserve
unrelated work, implement only the accepted slice, use the Agreement Loop only
for new decisions, record deviations, and verify continuously.

### `verify-release-evidence`

Verify the full user and operational story: acceptance, failure, recovery,
tests, types, lint, builds, migrations, security, privacy, performance, rendered
UI, degraded dependencies, retries, restarts, duplicates, and untested
assumptions in proportion to consequence.

### `deploy-with-recovery`

Load the relevant platform skill and project runbooks. Confirm readiness,
secrets, migrations, access, budgets, and rollback; deploy incrementally; verify
production reality; record sanitized evidence; then move to Observe rather than
Close.

### `diagnose-production-incident`

Separate containment, restoration, diagnosis, and prevention. Protect users and
data, preserve sanitized evidence, build a timeline, test ranked hypotheses,
avoid stacked speculative fixes, verify recovery on the affected path, and
create follow-up Change Work Objects.

### `review-outcome-and-adapt`

Compare hypothesis with lived and system outcomes, distinguish shipped output
from observed value, choose stop/repeat/deepen/repair/share/new work, and extract
Workflow Candidates rather than instant doctrine.

### `maintain-working-method`

Govern workflow candidates and confirmed rules, surface contrary evidence and
conflicts, review friction and routing quality, propose versioned skill changes,
test material adaptations, and prevent identity or value inference.

## Common Skill Contract

Each specialist receives the Work Object, lifecycle state, consequence level,
relevant evidence, confirmed workflow rules, and explicit request. It must:

- distinguish known, inferred, decided, and unresolved material;
- retrieve discoverable facts rather than ask for them;
- activate the Agreement Loop only at real decisions;
- recommend before asking one question;
- preserve human authority;
- generate novelty only when it changes the option space;
- maintain traceable artifacts and decisions;
- route when action is more useful than deliberation.

Each output identifies the updated state, artifact or evidence, decision status,
risks, next skill, exit criteria, and revisit trigger.

## Direct controls

- `do recommended`
- `grill this`
- `show branches`
- `show evidence`
- `try a novel angle`
- `just execute`
- `pause this`
- `close this`
- `route this`
- `private`
- `remember this rule`

Equivalent ordinary language has the same effect. `do recommended` accepts only
the immediately preceding recommendation, never blanket future authority.

## Storage and project integration

Markdown files are the canonical Work Object store. By default they live in a
local, Git-ignored `.work-studio/` directory. Agents discover that directory by
searching upward from the current workspace for `.work-studio/config.md` and
stop at the repository or filesystem boundary. They never scan the home
directory automatically. External or global stores require explicit
configuration.

Work Objects use immutable, time-sortable IDs and human-readable filenames:
`.work-studio/objects/YYYY/MM/<id>-<slug>.md`. Titles and filenames may change;
references use the immutable ID. The type is also immutable after activation.
When an Inquiry produces a Project, or an Incident produces a Change, create a
linked successor using typed relationships such as `resulted_in`, `responds_to`,
or `supersedes`.

Current Primary and Supporting attention roles live in
`.work-studio/active.md`, not in Work Object identity. The provisional limit of
one Primary and two Supporting objects is advisory for five completed Work
Objects; overrides remain available with a recorded reason. Unactivated signals
live as dated, user-language entries in `.work-studio/inbox.md`. Only explicit
activation creates a Work Object.

Private operational records and shareable project history are separate. A
reviewed, sanitized ledger may be tracked under `docs/work-studio/`, but every
export requires explicit human confirmation showing the destination, proposed
content, affected files, and sensitivity classification. Skill completion and
release never export automatically.

Personal memory is read-only during ordinary work. Work Objects retain stable
references and short attributed summaries rather than copied notes. New memory
or corrections require explicit confirmation before write-back.

Chat history is provisional. Extract decisions and evidence into the Work
Object, keep sensitive transcripts out by default, and make the Work Object
sufficient when chat history is unavailable.

## Work Object schema

```yaml
---
schema_version: 1
id: <immutable-time-sortable-id>
title: Human-readable title
type: inquiry | project | change | incident
status: active | waiting | paused | blocked | closed
state: notice | frame | explore | decide | design | build | verify | release | observe | close
consequence: low | meaningful | high
sensitivity: ordinary | private | restricted
created_at: RFC-3339 timestamp
updated_at: RFC-3339 timestamp
next_action: Concrete next move
---
```

`revisit_trigger` is additionally required for Waiting and Paused objects.
Evidence, decisions, risks, typed relationships, and history remain in
structured Markdown sections rather than expanding the minimum frontmatter.

Lifecycle movement is flexible. Consequence gates still apply when states are
skipped, and a rationale is required for backward moves, skipped states,
reopening Closed work, and entering Release.

Every meaningful transition appends an immutable History entry containing the
timestamp, action, resulting state, actor type (`human` or `agent`), platform
adapter, and concise evidence-based rationale. Hidden reasoning, full prompts,
and complete chat transcripts are excluded by default. Writers use optimistic
concurrency: re-read immediately before writing and stop if `updated_at` changed
since the initial read.

Body sections: Intent; Success evidence; Constraints and non-goals; Evidence
ledger; Current hypothesis; Decisions and revisit triggers; Agreement Loop
state; Relationships; Artifacts; Verification and release evidence; Observed
outcome; Open questions; Next move; Workflow Candidates; History.

## Composition map

| Work Studio skill | Existing capabilities composed |
| --- | --- |
| `turn-signal-into-work` | capture-lived-evidence, maintain-personal-memory, project-studio |
| `investigate-live-question` | maintain-personal-memory, project-studio, Matt Pocock research |
| `pressure-test-decision` | grill-with-docs, grilling, domain-modeling |
| `design-tracer-bullet` | domain-modeling, codebase-design, prototype |
| `implement-bounded-change` | TDD and relevant implementation skills |
| `verify-release-evidence` | code review and applicable browser/full-story verification |
| `deploy-with-recovery` | platform deployment skills and project runbooks |
| `diagnose-production-incident` | diagnosing-bugs and project recovery guidance |
| `review-outcome-and-adapt` | capture-lived-evidence, maintain-personal-memory |
| `maintain-working-method` | maintain-personal-memory, anti-homogenization-editor |

Compose rather than copy. Missing dependencies must be reported as reduced
capability rather than silently imitated.

## Skill document format

Each `SKILL.md` contains:

1. Trigger-oriented YAML frontmatter
2. Governing principle
3. Personal working lens
4. Boundaries and non-goals
5. Inputs and preconditions
6. Consequence and authority rules
7. Agreement Loop behavior
8. Stage workflow
9. Evidence rules
10. Adjacent Possibility behavior where relevant
11. Dependency invocation rules
12. Work Object updates
13. Routing and termination
14. Output template
15. Failure and degradation behavior
16. Anti-patterns
17. Final self-check

Personalization must appear as evidence-backed rules rather than decorative
biography.

## Qualification and red-team checks

Qualification covers contract behavior, one-question loops, convergence,
anti-loop behavior, memory confirmation, provenance, consequence, novelty,
dirty worktrees, degradation, golden Work Objects, and end-to-end journeys.

The system explicitly guards against ceremony inflation, interrogation fatigue,
recursive routing, stage theater, novelty churn, memory overreach, evidence
laundering, artifact sprawl, stale state, authority drift, false readiness,
context obesity, dependency imitation, and personalization lock-in.

The qualitative scorecard reviews completion, decision quality, reality contact,
loop burden, routing quality, escaped defects, recovery quality, personal fit,
artifact value, and novelty yield. It does not default to message counts, hours,
streaks, or artifact volume.

## Packaging and versioning

The bounded context and package name is **Andrelawas Work Studio**. This source
repository is the release authority for Codex, Claude Code, and GitHub Copilot;
do not edit installed plugin caches.

Each skill has one agent-neutral Markdown source with simple YAML frontmatter.
The core expresses capability requirements rather than platform tool names.
Thin adapters map those requirements to native tools and may vary only in
metadata, discovery and installation wiring, and capability mappings. Core
decision logic, authority boundaries, and the Work Object schema cannot diverge
unless a documented platform constraint makes equivalence impossible. Core
semantics govern; stricter platform safety rules always take precedence.

Keep the portable core and all adapters versioned together under `skills/core/`,
`adapters/codex/`, `adapters/claude-code/`, and
`adapters/github-copilot/`. Generate committed adapter artifacts using a small,
dependency-free Python maintainer tool plus explicit overlays. CI fails on
generated-file drift. Installation uses deterministic copies, checksums, and a
manifest; symlinks are only an optional development convenience.

Project-local, version-pinned adapters take precedence over global skills.
Global installation supplies conductor and bootstrap behavior, then defers to a
project's pinned version. Each adapter classifies capabilities as native,
manual fallback, or unsupported. It pauses with a concrete manual step when a
safe fallback exists and otherwise stops and records the limitation. It never
claims verification it could not perform.

Shared contracts:

- `references/WORK-OBJECT.md`
- `references/AGREEMENT-LOOP.md`
- `references/EVIDENCE-MODEL.md`
- `references/CONSEQUENCE-AUTHORITY.md`

Version core skills and the Work Object schema separately. Readers support
older schemas where practical. Every migration requires a preview, backup,
explicit confirmation, and an appended migration History entry. Installation
never rewrites private records automatically. Do not rewrite closed Work
Objects merely to match newer versions.

Read-only inspection and routine private Work Object updates that faithfully
reflect the conversation require no additional confirmation. Unrequested
source changes, external writes, deployments, exports, destructive actions,
schema migrations, and high-consequence actions require explicit authority.
`just execute` accepts the current recommendation within the stated scope and
records its assumptions and revisit trigger; it never bypasses safety, privacy,
destructive-action, or external-commitment gates.

## Implementation sequence

### Slice 1 — Core protocol

- Four shared contracts
- Work Object schema, template, storage, history, and concurrency rules
- `conduct-work-object`
- `pressure-test-decision`
- Codex, Claude Code, and GitHub Copilot adapters
- Deterministic generator, manifest installer, and CI drift check
- One shared cross-platform behavioral fixture

The Slice 1 fixture must prove that every adapter can discover the same
workspace, open or resume the same Work Object, identify one unresolved
decision, recommend before asking exactly one question, record the confirmed
decision without overwriting history, and stop before unauthorized
implementation or export. A platform either passes or explicitly marks a
capability unsupported.

### Slice 2 — Build path

- `turn-signal-into-work`
- `design-tracer-bullet`
- `implement-bounded-change`
- `verify-release-evidence`
- One real PKM Change Work Object exercised end to end

### Slice 3 — Reality and operations

- `investigate-live-question`
- `deploy-with-recovery`
- `diagnose-production-incident`
- PKM Project Adapter and operational scenarios

### Slice 4 — Learning and governance

- `review-outcome-and-adapt`
- `maintain-working-method`
- Workflow Candidate store
- Scorecard review and versioning rules

The first real qualification Work Object is the PKM Memory Candidate gate
correctness change. Selection of the pilot does not authorize implementation.

## Current boundary

This document preserves the accepted planning session. No generated Work Studio
skills have been implemented yet. The next action, once authorized, is Slice 1.
