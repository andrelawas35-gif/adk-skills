---
name: develop-idea
description: "Use when a Work Object in explore state needs divergent exploration; generates strongly differentiated directions grounded in project context; never decides which direction is better, never declares exploration complete without user selection."
---

# Develop Idea

## Governing principle

A rough thought inside a Work Object's `explore` state deserves structured
divergence — not premature convergence. This skill takes an ambiguous or
half-formed idea and develops it into strongly differentiated directions,
each grounded in project context and stated precisely enough that the user
can make a genuine choice. It is the system's first and only divergent
exploration capability.

The skill generates directions — it does not select, prioritize, or combine
them. Direction selection is the user's judgment call.

## Personal working lens

Most "vague ideas" are not actually vague — they are specific thoughts whose
contours haven't been tested against alternatives. Before reaching for
research, generate at least three distinct directions from what is already
known. The structure of the differences often reveals what the user actually
cares about more than any individual direction does.

When the user says "explore this" or "develop this idea," resist the urge to
ask clarifying questions first. Generate directions first, surface
information gaps after those directions make the gaps visible.

## Boundaries and non-goals

**This skill does:**
- Generate strongly differentiated directions from a rough idea in an
  `explore`-state Work Object
- Ground each direction in discovered project context (codebase, config,
  existing skills, prior decisions)
- Structure each direction with exactly five fields: title, core idea,
  distinctness claim, key assumption, smallest test
- Surface information gaps that direction differences make visible
- Offer enhancement operations (combine, expand, reframe) on user request
  only — never as a mandatory step
- Trigger web search only after initial directions are produced and
  information gaps are identified
- Record accepted directions in the Work Object's Decisions section

**This skill does NOT:**
- Decide which direction is "better" — that is the user's judgment
- Declare exploration complete without the user confirming selection
- Reframe the user's intent without explicitly checking the reframe
- Converge on a single answer — that is `investigate-live-question`'s job
- Challenge decisions adversarially — that is `pressure-test-decision`'s job
- Run a full grilling architecture session — that is `grilling-session`'s job
- Produce standalone idea-brief artifacts — output is captured in the Work
  Object body
- Generate visual designs, mockups, or diagrams in v1
- Implement any selected direction — it stops at the selection boundary

## Inputs and preconditions

**Required inputs:**
- An active Work Object in the `explore` state with `type: inquiry`
- The Work Object's current description of the idea or signal to develop
- Existing evidence ledger, decisions, and open questions (if any)

**Preconditions:**
- The Work Object is readable and schema-valid
- `conduct-work-object` has already established the workspace and Work Object
- The idea is genuinely ambiguous or half-formed — not already concrete
  enough for direct implementation

## Required capabilities

This skill requires the following abstract capabilities. The platform adapter
classifies each as native, manual-fallback, or unsupported and degrades
explicitly when one is unavailable (see `references/CAPABILITY-DEGRADATION.md`).

- `file_read` — Read Work Object files, evidence, project context
- `file_write` — Update Work Object with generated directions
- `content_search` — Search workspace for relevant context
- `directory_list` — List skills, references, and project structure
- `terminal_run` — Run checks, inspect git state
- `web_fetch` — Fetch external context after initial directions produced
- `structured_output` — Produce structured direction records

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`:

- The skill generates; the user selects. Authority never transfers.
- The agent never decides which direction is "better" beyond citing evidence.
- The agent never declares exploration complete without user selection.
- The agent never reframes the user's intent without explicitly checking.
- For a high-consequence Work Object, direction generation still proceeds
  (it is exploration, not commitment), but recording a selection requires
  explicit human confirmation.
- `just execute` accepts the current recommendation but never bypasses
  creative authority boundaries, safety gates, or the user's right to
  select among directions.

## Personal Institution handoff

When exploring an idea that may draw on personal context, apply Shared
Protocol v0.1 (`references/SHARED-PROTOCOL.md`). Work Studio must not scan,
read, or mutate the Personal Institution archive. It may receive an Evidence
Bridge only after the user approves a minimum-necessary handoff for the
receiving Work Object.

Record the bridge's provenance and sensitivity in the Evidence ledger.
Do not copy a personal-memory record, treat chat history as persistent
personalization, or let an inactive or irrelevant contract entry guide
exploration. If the protocol is unavailable or incompatible, report the
limitation and offer only a manual, user-approved summary.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and
wait for explicit entry; do not silently start a continuous session.

This is the divergence lens: pursue breadth over depth, surface the
dimensions along which directions meaningfully differ, and route to
enhancement or combination only when the user requests it. The engine, not
this skill, controls turn order, continuity, and convergence.

## Skill Grilling Profile

Apply the `develop-idea` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Generate at least three strongly
differentiated directions, surface what makes each distinct, and let
information gaps visible in the differences drive any follow-up research
before asking the user to select.

## Stage workflow

### 1. Receive the Work Object

This skill is invoked with a Work Object ID in `explore` state and
`type: inquiry`. Either `conduct-work-object` routes here, or the user
invokes directly.

Read the full Work Object. Extract:
- Current idea description or signal text
- Existing evidence ledger and provenance
- Prior decisions and revisit triggers
- Open questions
- Project context: active skills in `config.md`, component ledger entries,
  relevant reference documents

### 2. Discover project context

Before generating directions, gather context that grounds them:

- Read the skills directory to understand existing capabilities
- Read the component ledger for declared edges and dependencies
- Check `active.md` for potentially overlapping Work Objects
- Search the codebase for relevant patterns, config, or prior art

Do NOT ask the user for context that is discoverable from the workspace.

### 3. Generate differentiated directions

Produce at least three strongly differentiated directions. Each direction
must be genuinely distinct from the others — not the same idea with minor
variations. Directions should diverge along meaningful dimensions such as:

- **Scope**: broad integration vs narrow targeted addition
- **Approach**: new component vs extension of existing
- **Risk profile**: safe incremental vs ambitious rewrite
- **Time horizon**: quick win vs foundation for future
- **User impact**: visible feature vs internal infrastructure

If the idea naturally yields fewer than three distinct directions, report
why. If it yields more, present the strongest 3-5.

Each direction uses exactly five fields (DEC-12):

```markdown
### Direction N: <short title>

- **Core idea**: <one-paragraph description of what this direction entails>
- **Distinctness claim**: <how this differs materially from the other directions>
- **Key assumption**: <the single assumption this direction bets on>
- **Smallest test**: <the minimal experiment that would validate or invalidate the key assumption>
```

### 4. Surface information gaps

After presenting directions, identify what information would help the user
choose:

- Which gaps, if resolved, would eliminate one or more directions?
- Which gaps are discoverable (filesystem, docs, git log) vs need external
  research or user input?

Trigger web search only after directions are produced and gaps are identified
(DEC-9). Never search before initial directions exist.

### 5. Offer enhancement operations

When the user requests it (never proactively), offer to:

- **Combine two directions** — merge their strengths into a new option
- **Expand a direction** — add more detail to a specific direction
- **Reframe the intent** — check whether a different framing of the original
  idea opens new directions
- **Generate more directions** — if the user feels the space is not well
  covered

Enhancement operations are explicit and user-invoked, never a mandatory step
in the workflow (DEC-8).

### 6. Record the selection

When the user selects one or more directions:

1. Record the selection in the Work Object's **Decisions and revisit
   triggers** section with:
   - Direction(s) selected
   - Rationale (the user's stated reason)
   - Assumptions accepted
   - Next concrete action for the selected direction

2. Update the Work Object state:
   - If a single direction is selected → transition from `explore` to
     `design` (or the next appropriate state)
   - If multiple directions are selected → transition to `explore` with a
     note that multiple are under consideration

3. Append History with the selection and rationale.

4. Route to `conduct-work-object` for next-stage routing.

Do NOT implement the selected direction. Implementation is routed through
`design-tracer-bullet` and `implement-bounded-change`.

### 7. Concurrency check (mandatory)

Before every write:
1. Re-read the Work Object file.
2. Compare `updated_at` with the value from the initial read.
3. If changed → report the conflict with both timestamps. Do NOT overwrite.
   Offer to re-read, merge, and retry.
4. If unchanged → write, then update `updated_at`.

## Evidence rules

- Distinguish known, inferred, decided, and unresolved material in every
  direction's basis.
- Every factual claim grounding a direction carries a provenance marker.
- Information gaps are recorded in the Evidence ledger, not in History
  entries.
- Retrieve discoverable facts from the filesystem before asking the user.
- Directions may be based on inference (they are speculative by nature), but
  inference must be labeled as such and never presented as fact.

## Adjacent Possibility behavior

When the user says "try a novel angle" or the generated directions feel
unsurprising:

1. Identify the dominant assumption underlying all directions.
2. Find a contradiction, neglected actor, missing scale, or boundary
   condition that every direction shares.
3. Transform one dimension: actor, incentive, medium, timing, ownership,
   scale, interface, or constraint.
4. Generate at most three materially distinct additional possibilities.
5. State: changed assumption, fit with evidence, new direction, key
   assumption, and smallest test.
6. Present as alternatives alongside the original set.

Novel angles are additional directions, not replacements for the original
set — unless the user explicitly discards the original set.

## Dependency invocation rules

This skill composes with:
- **conduct-work-object** — for lifecycle management, state transitions,
  and routing after selection
- **investigate-live-question** — for resolving information gaps that would
  discriminate between directions (when the gap is narrower than generating
  more directions)
- **design-tracer-bullet** — for reality-testing the selected direction's
  key assumption after user selection

When any dependency is unavailable, report it as reduced capability:
- Missing conduct-work-object: "I can generate directions but cannot manage
  the Work Object lifecycle. Resume with conduct-work-object when ready."
- Missing investigate-live-question: "I can identify information gaps but
  cannot resolve them through targeted investigation."
- Missing design-tracer-bullet: "I can record the selected direction but
  cannot design a reality test for its key assumption."

Never silently imitate a missing dependency. Never route to a specialist
that does not exist.

## Work Object updates

After every interaction with a Work Object:
- Generated directions are recorded in the Work Object body
- If a selection is made, the Decisions section has a new dated entry
- If the state changes, frontmatter reflects it
- `updated_at` is current
- A History entry is appended for any state or status change
- `next_action` is concrete and reflects the post-exploration state
- The Work Object is sufficient to resume without chat context

## Routing and termination

**Route to `conduct-work-object` when:**
- Directions are generated and presented (awaiting user selection)
- A direction is selected and recorded
- The user declines to select and wants to pause or close

**Route to `investigate-live-question` when:**
- An information gap would discriminate between directions and can be
  resolved through targeted research rather than generating more directions

**Route to `design-tracer-bullet` when:**
- A direction is selected and its key assumption needs a reality test

**Terminate when:**
- The user explicitly ends the session
- The Work Object transitions out of explore state after selection
- A blocking condition is recorded and the object is set to Waiting

## Output template

After each interaction, report:

```markdown
**Work Object**: `{id}` — {title}
**Directions generated**: {N}
**Selection**: {selected direction or "awaiting user selection"}
**State**: {state} → {new_state} (if changed)
**Status**: {status}
**Next action**: {next_action}
**History appended**: {action} at {timestamp}
**Route**: {next_skill or "none — awaiting user input"}
```

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| Work Object not in explore state | Report current state. Cannot generate directions outside explore state. Route to conduct-work-object for state adjustment. |
| Work Object not found | Report the ID. Ask if it should be created first via conduct-work-object. |
| Fewer than 3 distinct directions possible | Report why. Present what exists. Do not fabricate false distinctions. |
| Missing project context for grounding | State what's missing. Generate directions with explicit uncertainty about context. |
| Web fetch fails | Report the failure. Proceed with directions grounded in available workspace context alone. |
| `updated_at` conflict on write | Report both timestamps. Do not overwrite. Offer to re-read, merge, and retry. |
| User asks to implement | Stop. "Implementation is out of scope for develop-idea. Route to design-tracer-bullet and implement-bounded-change after selecting a direction." |
| User asks to converge before generating | Respect the request. Route to investigate-live-question or pressure-test-decision if convergence is genuinely what they need. |

## Anti-patterns

1. **False divergence**: Presenting three variations of the same idea with
   cosmetic differences. Directions must be materially distinct.

2. **Premature convergence**: Steering toward one direction through framing
   or emphasis. Present all directions neutrally.

3. **Silent reframing**: Interpreting or redirecting the user's idea without
   checking. Always confirm reframes explicitly.

4. **Ceremonial generation**: Generating directions when the idea is already
   concrete enough to proceed. Route to design or implementation instead.

5. **Information hoarding**: Asking the user for context that is
   discoverable from the workspace. Search first, ask second.

6. **Selection by exhaustion**: Wearing the user down until they pick one.
   If no direction stands out, offer enhancement operations or pause.

7. **Scope creep**: Generating implementation plans, architectures, or
   timelines. Directions describe what and why, not how.

8. **Visualization pressure**: Creating diagrams, mockups, or wireframes
   without explicit user request. v1 has no visualization capability.

## Final self-check

Before reporting completion:

- [ ] At least three materially distinct directions generated
- [ ] Each direction has all five required fields
- [ ] Directions are grounded in discoverable project context
- [ ] Inference is labeled as inference, not presented as fact
- [ ] No direction is recommended over others
- [ ] Information gaps are surfaced for user to act on
- [ ] No implementation or design work performed
- [ ] Web search was triggered only after initial directions, if at all
- [ ] Enhancement operations were offered only on user request, if at all
- [ ] No standalone artifact created — output is in the Work Object
- [ ] No visualization, diagrams, or mockups produced
- [ ] The Work Object is sufficient to resume without chat context

---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live
outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `content_search` | `grep_search` | native |
| `directory_list` | `list_dir` | native |
| `terminal_run` | `run_in_terminal` | native |
| `web_fetch` | `fetch_webpage` | native |
| `structured_output` | `—` | native |
