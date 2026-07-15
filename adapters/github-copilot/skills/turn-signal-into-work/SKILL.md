---
name: turn-signal-into-work
description: "turn-signal-into-work — GitHub Copilot adapter"
platform: github-copilot
---
# Turn Signal into Work

## Governing principle

A signal deserves faithful capture before it deserves a project. Preserve the
user's words, distinguish evidence from interpretation, and protect attention
by creating a Work Object only when the user explicitly activates work.

## Personal working lens

The useful question is not "how can this become a project?" but "what is the
smallest durable handling that preserves the signal and the user's authority?"
Incubation is a valid outcome. An unactivated signal is not hidden backlog.

## Boundaries and non-goals

This skill does:

- Capture a signal without rewriting its meaning into premature plans.
- Retrieve only discoverable, relevant Work Studio context.
- Classify the signal as discard, remember, incubate, or activate.
- Create or resume a Work Object only after explicit activation.
- Route activated work to the conductor or the appropriate next specialist.

This skill does not:

- Implement, investigate, design, deploy, export, or write personal memory.
- Treat chat history as durable evidence or personalization.
- Scan, read, or mutate the Personal Institution archive.
- Infer activation from enthusiasm, urgency, or a detailed idea.

## Inputs and preconditions

**Required input:** a live signal in the user's language, such as an idea,
observation, request, concern, or possible change.

**Optional input:** an approved Evidence Bridge or a stable reference supplied
by the user. Never request or retrieve the Personal Institution archive
directly.

Discover the workspace by searching upward for `.work-studio/config.md`,
stopping at the repository or filesystem boundary. Read the inbox and active
Work Objects only when they are relevant to classification; never scan the
home directory.

## Required capabilities

- `file_read` — read workspace configuration and relevant Work Studio records.
- `file_write` — update `.work-studio/inbox.md` or create a Work Object after
  authorization.
- `directory_list` — inspect Work Object locations without broad scanning.
- `content_search` — find relevant active or recent Work Objects.
- `structured_output` — preserve provenance, classification, and next move.
- `user_confirmation` — obtain explicit activation before creating work.

If a required capability is manual-fallback or unsupported, follow
`references/CAPABILITY-DEGRADATION.md`: pause with one concrete manual step or
stop the affected path. Do not claim capture, retrieval, or activation occurred
when it did not.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Capturing an unactivated signal is a routine private Work Studio update.
- Creating or updating low- or meaningful-consequence Work Objects after the
  user explicitly activates the signal may proceed through the conductor.
- High-consequence activation requires explicit confirmation naming the Work
  Object mutation; phrases such as `do recommended` do not authorize it. Do
  not stage, annotate, change status, append History, or make any other
  mutation before receiving that scoped confirmation.
- Never export, share, deploy, or copy private or restricted material.

## Agreement Loop behavior

Classification is not a decision loop when the signal and next handling are
clear. Activate the Agreement Loop only when an unresolved boundary would
materially change the handling:

1. State the evidence, inference, and consequence level.
2. Recommend one classification and explain the smallest trade-off.
3. Ask one decision-bearing question.
4. Integrate the answer and record only the durable result.

Do not offer a menu of equal options, and do not use a classification question
to obtain blanket authority for future work.

## Stage workflow

### 1. Capture faithfully

Record a dated signal using the user's language. Separate direct observations
from inferred intent. Mark the provenance lane in accordance with
`references/EVIDENCE-MODEL.md`; chat context alone is provisional, not durable
evidence.

### 2. Retrieve minimum relevant context

Search for a matching active Work Object, a recent related Work Object, and a
relevant existing inbox entry. Summarize only what changes the classification.
If personal context would help, request an approved, minimum-necessary
Evidence Bridge. Work Studio must not scan, read, or mutate Personal
Institution records.

### 3. Classify

- **Discard** when the user does not want durable retention.
- **Remember** when it should be retained without becoming current work.
- **Incubate** when it may matter later but lacks a concrete next move; record
  a revisit trigger.
- **Activate** only when the user explicitly asks to start or resume work.

Recommend one classification when unclear. State any inference and uncertainty.

### 4. Persist the smallest appropriate artifact

For remember or incubate, add a dated, user-language entry to
`.work-studio/inbox.md`; record the classification, provenance, and revisit
trigger for incubated signals. For discard, do not create a Work Object or
retain material beyond what the user asks to keep. For activate, route to
`conduct-work-object` with the captured signal, relevant evidence, proposed
type, consequence, and sensitivity.

### 5. Activate through the conductor

The conductor checks for a matching Work Object, creates or resumes one under
its schema and concurrency rules, updates the attention register only when
appropriate, and selects the next specialist. This skill never bypasses the
conductor to manufacture a Work Object.

## Evidence rules

- Keep the original signal concise and attributable; do not store full chat
  transcripts or hidden reasoning.
- Label interpretation as `[inference]`, user choice as `[decision]`, and any
  user report as `[lived]` unless a stronger source is supplied.
- An Evidence Bridge must be user-approved, minimum-necessary, and record its
  provenance, sensitivity, source reference, and receiving Work Object.
- Restricted material is never copied into inbox entries or Work Objects.

## Work Object updates

This skill does not create Work Objects itself. When activation is explicit,
pass the conductor a concise capture that includes the candidate intent,
relevant evidence, classification rationale, consequence and sensitivity
assessment, and concrete next move. The conductor owns schema validation,
optimistic concurrency, History, and active-role changes.

## Routing and termination

- **Discard:** confirm no Work Object was created and stop.
- **Remember or incubate:** report the durable entry and revisit trigger, then
  stop.
- **Activate:** route to `conduct-work-object`.
- **Missing personal-memory capability:** request one user-approved manual
  summary or stable reference; do not imitate retrieval.
- **Unclear activation:** recommend a classification and ask one question.

## Output template

```markdown
## Signal handling

- **Signal:** <user-language summary>
- **Known evidence:** <provenance-labelled facts>
- **Inference:** <if any>
- **Recommendation:** discard | remember | incubate | activate
- **Authority status:** <whether explicit activation was received>
- **Artifact:** <none | inbox entry | Work Object ID after conductor route>
- **Next move:** <concrete action or revisit trigger>
```

## Failure and degradation behavior

If the workspace cannot be discovered, stop and ask for the workspace path.
If writing the inbox is unavailable, return the exact user-language capture and
one concrete manual instruction; do not claim it was retained. If a matching
Work Object cannot be read, say the classification is based only on the current
signal. If an Evidence Bridge is unavailable, continue without personal context
or request a user-approved summary; never substitute a personal-memory scan.

## Anti-patterns

- Turning every idea into an active Project.
- Rewriting a user's tentative signal as a confident requirement.
- Creating a Work Object before explicit activation.
- Copying personal-memory records or inferring identity from a signal.
- Treating an inbox entry as evidence without recording provenance.
- Hiding uncertainty, degradation, or a missing user decision.

## Final self-check

- Did I preserve the user's language and separate evidence from inference?
- Did I choose the smallest handling and avoid project inflation?
- Did explicit activation occur before any Work Object creation or resumption?
- Did I protect Personal Institution boundaries and restricted material?
- Did I state the artifact, next move, and any capability gap honestly?
---

## Platform Adapter

This skill is adapted for **GitHub Copilot** from the canonical core.
Core decision logic, authority boundaries, and schema semantics are
preserved unchanged. This section documents only platform-specific
wiring and declared limitations.

### Installation and precedence

Install with the maintainer tool (no Python required at runtime — it
verifies checksums with the platform's `shasum`/`sha256sum`):

```sh
# Global bootstrap (conductor everywhere):
tools/install.sh --platform github-copilot --global
# Project pin (takes precedence inside this project):
tools/install.sh --platform github-copilot --project .
```

- Global install dir: `~/.copilot/skills/`
- Project pin dir: `.copilot/skills/`

A **project-pinned** adapter always takes precedence over the global
bootstrap install. The global install supplies conductor and bootstrap
behavior everywhere, then defers to the version a project has pinned.
Precedence is recorded in `.work-studio/adapter.lock` and enforced by
the generated adapter's runtime pin-resolution contract.

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
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `git_operations` | `run_in_terminal (git commands)` | native |
| `glob_search` | `file_search` | native |
| `parallel_tool_execution` | `—` | manual-fallback |
| `structured_output` | `—` | native |
| `subagent_spawn` | `runSubagent` | native |
| `terminal_run` | `run_in_terminal` | native |
| `user_confirmation` | `conversation turn` | native |
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
- **Note**: GitHub Copilot browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.

#### `parallel_tool_execution` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: GitHub Copilot may serialize some parallel tool calls. For performance-critical multi-step workflows, verify execution order manually.

#### `web_search` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.

### Declared Limitations

- **browser_automation**
  (manual-fallback):
  GitHub Copilot browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.
- **parallel_tool_execution**
  (manual-fallback):
  GitHub Copilot may serialize some parallel tool calls. For performance-critical multi-step workflows, verify execution order manually.

### Integrity

This file is generated. Do not edit directly — edit the canonical core
at `skills/core/<skill>/SKILL.md` or the overlay at
`adapters/github-copilot/overlay.yaml`. Regenerate with
`python3 tools/generate-adapters.py`.
