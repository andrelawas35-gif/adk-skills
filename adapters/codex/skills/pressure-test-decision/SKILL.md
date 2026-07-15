---
name: pressure-test-decision
description: >
   Resume an active Work Object, identify its highest-leverage unresolved
  decision, recommend an answer before asking exactly one question, and safely
  persist the confirmed decision. Use when the user says "help me decide,"
  "pressure-test this," "grill this," "what should I do about X," or when
  conduct-work-object routes a Work Object in the Decide state. Composes
  grilling and domain modeling. Never performs implementation.
platform: codex
---
# Pressure-Test Decision

## Governing principle

A decision is only as good as the evidence beneath it and the alternatives
it survived. This skill stress-tests one decision at a time against
discoverable facts, edge cases, and genuine trade-offs, then records the
confirmed choice with enough context that a future reader — human or agent —
can understand why it was made without replaying the conversation.

## Personal working lens

Most decisions don't need a ceremony. Most "analysis paralysis" is really a
missing fact, not a missing framework. Before running the full loop, check:
is the answer obvious once we look up the right thing? If yes, look it up
and move on.

Real decisions — the ones worth this skill — are the ones where reasonable
people could disagree after seeing the same evidence. Those deserve the full
treatment: one branch at a time, a clear recommendation, and a recorded
rationale with revisit triggers.

## Boundaries and non-goals

**This skill does:**
- Distinguish evidence, inference, decision, and unresolved material
- Retrieve discoverable facts before asking the user
- Walk one decision branch at a time with a single recommendation
- Sharpen vague language into precise alternatives
- Test recommendations against edge cases and failure modes
- Record confirmed decisions with rationale, alternatives, and revisit triggers
- Create architecture decision records (ADRs) only for hard-to-reverse,
  surprising, genuine trade-offs
- Append attributable History entries on every confirmed decision
- Detect and report concurrency conflicts on write

**This skill does NOT:**
- Implement anything — it stops at the decision boundary
- Write code, edit source files outside `.work-studio/`, or deploy
- Export, share, or migrate data
- Make the decision for the user — it recommends, the user decides
- Run multiple decision branches simultaneously
- Create ADRs for routine, obvious, or reversible choices
- Overwrite Work Object history or mutate past entries

## Inputs and preconditions

**Required inputs:**
- An active Work Object in or entering the `decide` state (or a state where
  an unresolved decision blocks progress)
- The Work Object's current evidence ledger, hypothesis, and open questions

**Preconditions:**
- The Work Object is readable and schema-valid
- `conduct-work-object` has already established the workspace and Work Object
- The decision is genuinely unresolved — the answer is not obvious from
  existing evidence

## Required capabilities

This skill requires the following abstract capabilities. The platform adapter
classifies each as native, manual-fallback, or unsupported and degrades
explicitly when one is unavailable (see `references/CAPABILITY-DEGRADATION.md`).

- `file_read` — Read Work Object files, evidence, prior decisions
- `file_write` — Update Work Object with decisions, History entries
- `content_search` — Look up discoverable facts in the workspace
- `terminal_run` — Retrieve facts from git history, run checks
- `git_operations` — Inspect repository state for evidence
- `structured_output` — Produce decision records and YAML frontmatter
- `web_fetch` — Retrieve external documentation or sources when relevant
- `subagent_spawn` — Parallel Standards and Spec review (optional)

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`:

- The skill recommends; the user decides. Authority never transfers.
- `do recommended` accepts only the immediately preceding recommendation
  within its stated scope. It never grants blanket future authority.
- High-consequence decisions require explicit confirmation before recording.
- The skill stops before any implementation, external write, destructive
  action, migration, or export — even on `just execute`.
- Personal memory is read-only during decision work.

## Personal Institution handoff

When a decision needs personal context, apply Shared Protocol v0.1
(`references/SHARED-PROTOCOL.md`). Work Studio must not scan, read, or mutate
the Personal Institution archive. It may use an Evidence Bridge only after the
user approves a minimum-necessary handoff for the receiving Work Object.

Keep a bridge's provenance and sensitivity explicit; never relabel inference
as source or system evidence. Do not persist personalization from chat, infer
identity, or apply inactive or irrelevant contract entries. If the protocol is
unavailable or incompatible, report the limitation and offer only a manual,
user-approved summary.

## Agreement Loop behavior

This skill IS the Agreement Loop for decisions. It activates the full loop
because every invocation is a decision boundary:

1. **Orient** — Read the Work Object. Sort everything into provenance lanes:
   evidence (lived/source/system), inference, prior decisions, and unresolved
   material. Surface what's known vs. what's assumed.

2. **Map** — Identify the decision tree. What branches exist? What depends on
   what? Which decision has the highest leverage — the one that, once made,
   collapses the most uncertainty? Walk dependencies before dependents.

3. **Recommend** — Give ONE recommended answer. State:
   - What evidence supports it
   - What trade-offs it accepts
   - What alternatives were considered and why they rank lower
   - Confidence level (high/medium/low)
   - What would change the recommendation

4. **Ask** — Ask exactly ONE decision-bearing question. Make it specific,
   answerable, and scoped to the current branch. Do not present a menu of
   equal options.

5. **Integrate** — Record the user's answer. If they accept the recommendation,
   proceed to record. If they choose differently, record their choice with
   their rationale. If they push back, re-orient with the new constraint.

6. **Generate novelty** — Only when the current branches are exhausted or the
   user says "try a novel angle." Apply the Adjacent Possibility Pass:
   identify the dominant assumption, find a contradiction or neglected
   dimension, generate at most three materially distinct alternatives, state
   changed assumptions and costs, recommend one or retain the original.

7. **Test** — Before recording, test the confirmed choice against:
   - An edge case the choice doesn't handle well
   - A failure mode that could invalidate the assumption
   - A future scenario where the choice looks wrong
   Surface these, don't hide them.

8. **Converge or route** — If the decision is sufficient to proceed, record it
   and route back to `conduct-work-object`. If new decisions emerged, loop
   back. If the decision space is exhausted, route with documented uncertainty.

## Stage workflow

### 1. Receive the Work Object

This skill is invoked with a Work Object ID and the specific decision
context. Either `conduct-work-object` routes here, or the user invokes
directly.

Read the full Work Object. Extract:
- Current state, status, consequence, sensitivity
- Evidence ledger (all entries with provenance)
- Current hypothesis (if any)
- Prior decisions and revisit triggers
- Open questions
- The specific decision needing pressure-testing

### 2. Sort into provenance lanes

Before any recommendation, classify every claim in the Work Object:

```
[evidence/lived]   — direct observation or experience
[evidence/source]  — attributable external material
[evidence/system]  — code, tests, logs, metrics
[inference]        — interpretation connecting evidence
[decision]         — previously confirmed human choice
[unresolved]       — not yet classified or decided
```

Surface contradictions: "The evidence ledger says X [evidence/source], but
the current hypothesis assumes Y [inference]. Which should govern?"

If a fact is discoverable (filesystem, docs, config, git log), look it up
rather than asking. Never ask the user for information you can find.

### 3. Identify the highest-leverage decision

From the unresolved material, identify the decision tree. Order by leverage:
which decision, once made, makes others easier or irrelevant?

Report: "The highest-leverage unresolved decision is [X]. Here's why it
comes first: [dependency reasoning]."

If multiple independent decisions exist, pick one. Don't interleave them.
The user can always say "not that one, the other one."

### 4. Walk one branch

For the chosen decision:

1. List the viable branches (typically 2-4, rarely more).
2. For each branch, state: evidence for, evidence against, cost, reversibility.
3. Apply grilling: challenge each branch with "what would make this wrong?"
4. Sharpen language: replace vague terms ("scalable," "clean," "better") with
   concrete criteria ("handles 10k concurrent requests," "one file per concern,"
   "passes the existing test suite without modification").

Then recommend one branch. State why it wins.

### 5. Ask one question

Format: "I recommend [X] because [evidence-backed reason]. The main trade-off
is [Y]. Confidence: [high/medium/low]. What would change this: [condition].

Do you accept this recommendation?"

Wait for the answer. Acceptable responses:
- "yes" / "do recommended" → accept and record
- "no, do [alternative]" → record the alternative
- "what about [scenario]?" → test against that scenario and re-recommend
- "grill this" / "show branches" / "try a novel angle" → apply the indicated
  control and re-recommend

### 6. Test the confirmed choice

Before writing, surface:

- One edge case the choice handles poorly or not at all
- One assumption that, if wrong, invalidates the choice
- One future scenario where this choice creates friction

The user may acknowledge and proceed, or adjust. Either way, these go into
the decision record as context.

### 7. Sharpen the language

Before recording, ensure the decision uses precise language:

- "We will use PostgreSQL" → "We will use PostgreSQL 16 for the write model,
  with the existing read replicas unchanged"
- "Keep it simple" → "Single process, no message queue, accepting that restart
  loses in-flight work"
- "Add caching" → "Add a 60-second Redis cache in front of the /search endpoint,
  invalidated on write"

Vague decisions are not decisions — they're postponements dressed as decisions.

### 8. Record the decision

#### Update the Work Object body

In the **Decisions and revisit triggers** section, append:

```markdown
### YYYY-MM-DDTHH:MM:SSZ — <decision summary>

- **Branch chosen**: <what was decided>
- **Alternatives considered**: <branches not taken and why>
- **Rationale**: <evidence-backed reason>
- **Trade-offs accepted**: <what we're giving up>
- **Confidence**: high | medium | low
- **Revisit trigger**: <concrete condition that would reopen this>
- **Edge cases noted**: <surfaced in testing>
- **Actor**: human | agent
```

#### Optionally create an ADR

Create a file at `docs/adr/NNNN-<slug>.md` ONLY when ALL three are true:
1. **Hard to reverse** — the cost of changing is meaningful
2. **Surprising** — a future reader would wonder "why?"
3. **A real trade-off** — genuine alternatives existed

Use the ADR format from `domain-modeling`. Skip ADRs for routine,
obvious, or easily reversible choices.

#### Update frontmatter

If this decision completes the Decide state:
- Set `state` to `design` (or the next appropriate state)
- Update `updated_at`
- Update `next_action` to reflect the next concrete move

#### Append History

```markdown
### YYYY-MM-DDTHH:MM:SSZ — Decision recorded: <summary>

- **State**: <resulting state>
- **Status**: <unchanged unless the decision changes it>
- **Actor**: human (the decider) | agent (if the user said "do recommended")
- **Platform**: codex
- **Rationale**: <one-line evidence-based reason for the state transition>
```

### 9. Concurrency check (mandatory)

Before every write:
1. Re-read the Work Object file.
2. Compare `updated_at` with the value from the initial read.
3. If changed → report the conflict with both timestamps. Do NOT overwrite.
   Offer to re-read, merge, and retry.
4. If unchanged → write, then update `updated_at`.

## Evidence rules

- Every claim in the recommendation must carry a provenance marker.
- Inference must be distinguished from direct evidence: "The API docs say X
  [evidence/source]; I infer that Y is safe [inference]."
- Uncertainty is stated explicitly, not buried: "Confidence is medium because
  we haven't tested this with production traffic volumes."
- Retrieve discoverable facts from the filesystem, git history, or
  documentation before asking the user.

## Adjacent Possibility behavior

When the user says "try a novel angle" or the current branches are exhausted:

1. Identify the dominant assumption everyone is making.
2. Find a contradiction, neglected actor, missing scale, or boundary condition.
3. Transform one dimension: actor, incentive, medium, timing, ownership,
   scale, interface, or constraint.
4. Generate at most three materially distinct possibilities.
5. State: changed assumption, fit with evidence, new possibility, cost, and
   smallest reality test.
6. Recommend one option or retain the original design.

Novel ideas do not enter implementation without framing and a bounded reality
test. Record them as alternatives considered, not as the chosen branch unless
the user explicitly selects one.

## Dependency invocation rules

This skill composes with:
- **grilling** — for the core challenge-every-branch behavior. Applied at
  step 4 of the workflow: challenge each branch with "what would make this
  wrong?"
- **domain-modeling** — for sharpening language, maintaining the glossary in
  `CONTEXT.md`, and creating ADRs when warranted. Applied at step 7
  (sharpen language) and step 8 (ADR creation).

When either dependency is unavailable, report it as reduced capability:
- Missing grilling: "I'll walk the branches but won't apply systematic
  challenge patterns. Consider installing the grilling skill for full
  pressure-testing."
- Missing domain-modeling: "I'll record decisions but won't maintain a
  domain glossary or create formal ADRs."

Never silently imitate a missing dependency.

## Work Object updates

After every confirmed decision:
- The Decisions and revisit triggers section has a new dated entry
- If the state changes, frontmatter reflects it
- `updated_at` is current
- A History entry is appended
- `next_action` is concrete and reflects the post-decision state
- The Work Object is sufficient to resume without chat context

## Routing and termination

**Route back to `conduct-work-object` when:**
- The decision is confirmed and recorded
- The Work Object state has advanced (e.g., decide → design)
- No further decisions are needed at the current stage

**Route to `design-tracer-bullet` when:**
- The decision opens a design question
- The state advances to design

**Terminate when:**
- The user explicitly ends the session
- A blocking condition is recorded that requires external input
- The Work Object is paused or waiting with a revisit trigger

## Output template

After each decision interaction, report:

```markdown
**Work Object**: `{id}` — {title}
**Decision**: {summary of what was decided}
**Branch chosen**: {the confirmed choice}
**Confidence**: {high | medium | low}
**Trade-offs**: {what was accepted}
**Revisit trigger**: {when to reconsider}
**State**: {state} → {new_state} (if changed)
**History appended**: Decision recorded at {timestamp}
**Route**: conduct-work-object — {reason}
```

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| Work Object not found | Report the ID. Ask if it should be created first via conduct-work-object. |
| No unresolved decisions | Report: "This Work Object has no unresolved decisions at the current stage. Current state: {state}. Next action: {next_action}. Route to conduct-work-object?" |
| Missing evidence for recommendation | State what's missing, mark confidence as low, recommend the best option with explicit uncertainty. Do not fabricate evidence. |
| `updated_at` conflict on write | Report both timestamps. Do not overwrite. Offer to re-read, merge, and retry. |
| Decision branches exceed 5 | Pause. Ask the user to narrow the scope or eliminate clearly inferior branches first. |
| User asks to implement | Stop. "Implementation is out of scope for pressure-test-decision. I'll route you to design-tracer-bullet and implement-bounded-change after this decision is recorded." |
| User asks to export or share | Stop. "Export requires explicit confirmation showing destination, content, affected files, and sensitivity. I cannot proceed without this." |
| High-consequence decision without explicit confirmation | Pause. "This is a high-consequence decision. Before I record it, confirm you want to proceed with [specific choice]." |

## Anti-patterns

1. **Menu dumping**: Presenting equal options without a recommendation.
   Always recommend one.

2. **Multi-question barrage**: Asking several decision questions at once.
   One branch, one question, one answer. Repeat.

3. **Premature ADRs**: Creating formal architecture records for routine
   choices. ADRs are for hard-to-reverse, surprising, trade-off decisions.

4. **Vague recording**: Writing decisions like "Use event sourcing" without
   scope, rationale, or trade-offs. Sharpen before recording.

5. **Silent authority drift**: Recording a recommendation as a decision
   without explicit user confirmation. The user always confirms.

6. **Evidence laundering**: Presenting inference as source evidence.
   Distinguish them explicitly.

7. **Endless looping**: Revisiting decided branches without new evidence.
   A decision stands until its revisit trigger fires or new evidence
   arrives.

8. **Implementation creep**: Following a decision into design or code.
   Stop at the decision boundary. Route to the next specialist.

9. **Conflict ignorance**: Writing without re-reading. Always check
   `updated_at` before writing.

10. **False certainty**: Stating medium or low confidence recommendations
    as certain. Confidence level must be explicit.

## Final self-check

Before reporting completion:

- [ ] All claims in the recommendation carry provenance markers
- [ ] Evidence, inference, decision, and unresolved material are distinguished
- [ ] Exactly one recommendation was given, with confidence level
- [ ] Exactly one decision-bearing question was asked
- [ ] The confirmed decision is recorded with rationale, alternatives, trade-offs, and revisit trigger
- [ ] Language is sharpened — no vague terms in the recorded decision
- [ ] An ADR was created only if warranted (hard-to-reverse + surprising + real trade-off)
- [ ] `updated_at` was checked before writing (concurrency guard)
- [ ] A History entry was appended with timestamp, actor, platform, and rationale
- [ ] No implementation, export, or external write was performed
- [ ] The Work Object is sufficient to resume without chat context
- [ ] Route to next specialist is clear
---

## Platform Adapter

This skill is adapted for **Codex (VS Code)** from the canonical core.
Core decision logic, authority boundaries, and schema semantics are
preserved unchanged. This section documents only platform-specific
wiring and declared limitations.

### Installation and precedence

Install with the maintainer tool (no Python required at runtime — it
verifies checksums with the platform's `shasum`/`sha256sum`):

```sh
# Global bootstrap (conductor everywhere):
tools/install.sh --platform codex --global
# Project pin (takes precedence inside this project):
tools/install.sh --platform codex --project .
```

- Global install dir: `~/.codex/skills/`
- Project pin dir: `.codex/skills/`

A **project-pinned** adapter always takes precedence over the global
bootstrap install. The global install supplies conductor and bootstrap
behavior everywhere, then defers to the version a project has pinned.
Precedence is recorded in `.work-studio/adapter.lock` and honored by
Codex (VS Code)'s project-over-user skill resolution.

### Discovery

- Config path: `.work-studio/config.md`
- Boundary marker: `.git`
- Stop condition: repository root (presence of .git)
- Stop condition: filesystem boundary

### Capability Mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `browser_automation` | `—` | manual-fallback |
| `content_search` | `grep_search` | native |
| `directory_list` | `list_dir` | native |
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `git_operations` | `run_in_terminal (git commands)` | native |
| `glob_search` | `file_search` | native |
| `structured_output` | `—` | native |
| `subagent_spawn` | `runSubagent` | native |
| `terminal_run` | `run_in_terminal` | native |
| `web_fetch` | `open_browser_page / mcp tools` | native |
| `web_search` | `—` | manual-fallback |

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

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.

#### `web_search` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Live web search requires manual lookup. The agent can fetch known URLs but cannot perform open-ended web searches.

### Declared Limitations

- **browser_automation**
  (manual-fallback):
  Browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.
- **web_search**
  (manual-fallback):
  Live web search requires manual lookup. The agent can fetch known URLs but cannot perform open-ended web searches.

### Integrity

This file is generated. Do not edit directly — edit the canonical core
at `skills/core/<skill>/SKILL.md` or the overlay at
`adapters/codex/overlay.yaml`. Regenerate with
`python3 tools/generate-adapters.py`.
