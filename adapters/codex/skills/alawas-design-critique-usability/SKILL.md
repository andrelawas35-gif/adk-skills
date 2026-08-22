---
name: alawas-design-critique-usability
description: "Use when a rendered interface's usability needs independent evaluation; checks it against named heuristics (visibility of status, consistency, recognition over recall) with evidence-linked findings; never fixes findings or overrides confirmed creative direction."
default_tier: medium
platform: codex
---
# Critique Usability

## Governing principle

`alawas-design-verify-design-implementation` answers one question: does the code match
what was confirmed? It never asks whether what was confirmed is actually
good. No skill in the pipeline does — a design can pass parity checks
perfectly and still have real usability problems no one was asked to look
for. This skill is that missing question: it evaluates a real rendered
interface against named usability heuristics, independent of whether a
specific direction was confirmed, and reports findings a person can check
and challenge. It never fixes anything and never overrides a confirmed
creative decision — a finding is a candidate for `alawas-design-apply-design-direction`
to weigh, not a verdict that changes code on its own.

## Boundaries and non-goals

This skill does:

- Evaluate a real rendered interface against a named, fixed set of
  usability heuristics (e.g., visibility of system status, consistency and
  standards, recognition rather than recall, error prevention, aesthetic
  and minimalist design).
- Produce findings that each cite the specific element and the exact
  heuristic violated — never a bare taste judgment with nothing concrete
  behind it.
- Explicitly name which heuristics were *not* checked in a given pass and
  why (most commonly: heuristics needing live interaction — error recovery,
  undo, help/documentation — that static or single-frame inspection cannot
  test), matching `alawas-design-verify-design-implementation`'s own honesty about
  deferred dimensions.
- Produce a `[system:usability-critique]` Evidence Ledger entry with
  per-heuristic findings.
- Run independent of whether a specific direction has been confirmed —
  usability quality is a different question from direction parity, and
  this skill does not wait on `alawas-design-apply-design-direction`'s cycle.

This skill does not:

- Fix, patch, or otherwise mutate any code, style, or markup — findings
  route to `alawas-design-apply-design-direction` as candidate direction changes.
- Override or invalidate a confirmed creative decision — a finding is
  evidence for the director to weigh, not an automatic correction.
- Check parity against a confirmed proposal — that remains
  `alawas-design-verify-design-implementation`'s job; this skill evaluates the design's
  quality on its own terms, confirmed or not.
- Perform heuristics that require live interaction (error recovery, undo,
  help/documentation, multi-step task completion) in this version — these
  are named as out of scope, not attempted with a weaker static proxy.
- Conduct real user testing, A/B testing, or gather behavioral analytics —
  this is heuristic evaluation by inspection, not empirical user research.
- Modify the frontier-ownership map or pipeline documentation on its own —
  registering a new frontier is a routing change the conductor and pipeline
  reference own.

## Inputs and preconditions

**Required input:** a readable Work Object with access to a real, rendered
interface to evaluate — a target project's running application, or a
Work-Studio-owned static projection (e.g. `.work-studio/*.html`). No
particular Work Object state is required, the same independence
`alawas-design-audit-accessibility` and `alawas-design-build-design-foundation` already claim:
usability quality is orthogonal to whether a specific direction has been
confirmed.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. The surface to evaluate is identifiable and
reachable (a URL, a dev server, or a real file path).

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback,
or unsupported and follows `references/CAPABILITY-DEGRADATION.md` when
needed.

- `file_read` — read the target file or inspect the rendered markup.
- `browser_automation` — inspect a live running application when the
  surface is not a static file (manual-fallback: a described check the user
  confirms, same posture as `alawas-design-verify-design-implementation` and
  `alawas-design-audit-accessibility`).
- `structured_output` — produce the usability-critique report.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill performs only reads and observations — **low consequence**.
- No code, styles, markup, or design artifacts are modified.
- The critique report is written to the Evidence Ledger through the
  conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and
wait for explicit entry; do not silently start a continuous session.

The usability lens asks:

1. Does every finding cite a specific element and heuristic, or does any
   finding rest on taste alone?
2. Are heuristics requiring live interaction named as out of scope, rather
   than silently skipped or weakly proxied?
3. Could a finding instead be an intentional design choice the critique
   mistook for a violation?

## Skill Grilling Profile

Apply the `alawas-design-critique-usability` profile and continuous
Grilling Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Identify the surface and heuristic set

Identify the real rendered interface to evaluate. Select the named
heuristic set for this pass — start from the statically-checkable subset
(visibility of system status, consistency and standards, recognition
rather than recall, aesthetic and minimalist design) unless the surface
supports live interaction and the director wants the interactive
heuristics (error prevention and recovery, help and documentation)
included.

### 2. Check visibility of system status and consistency

Inspect whether the interface communicates what state it's in (when was
this generated, what does this count represent) and whether repeated
concepts (labels, status indicators, metadata fields) follow one
consistent presentation pattern across the surface, not different
conventions for equivalent things.

### 3. Check recognition rather than recall

Inspect whether information can be understood from what's on screen, or
whether it requires the viewer to already know an external schema,
abbreviation, or vocabulary with no on-screen explanation.

### 4. Check remaining named heuristics

For each additional heuristic in the selected set (e.g., aesthetic and
minimalist design, error prevention where staticly checkable), produce
findings with the same evidence-linking discipline: cite the element, name
the heuristic, describe exactly what violates it.

### 5. Report deferred heuristics

State explicitly which heuristics in the full standard set were not
checked in this pass and why — most commonly, heuristics requiring live
interaction that this pass's mechanism cannot test.

### 6. Produce the critique report

Assemble the `[system:usability-critique]` Evidence Ledger entry: the
surface evaluated, the heuristic set checked, per-heuristic findings with
concrete evidence (element cited, exact violation described), and the
deferred-heuristics table with reasons.

## Routing and termination

**Route when:**
- The critique report is complete — return to `alawas-governance-conduct-work-object`.
- A finding should be fixed — route to `alawas-design-apply-design-direction` with the
  specific finding as a candidate direction change; this skill does not fix
  it directly.

**Terminate when:**
- The usability-critique report is recorded in the Evidence Ledger.
- All selected heuristics are checked or explicitly deferred with reasons.

## Output contract

The `[system:usability-critique]` entry contains:

- `surface`: the file, URL, or dev-server path evaluated
- `heuristics_checked`: the named set evaluated in this pass
- `findings`: per-heuristic list, each with the cited element, a quoted or
  described concrete violation, and a pass/fail status
- `deferred_heuristics`: table of heuristic, deferred, and reason
- `overall`: a count summary (e.g., "N/M heuristic checks pass"), never a
  single pass/fail collapsing distinct findings

## Final self-check

- [ ] Every finding cites a specific element and names the heuristic it
      violates
- [ ] No finding rests on a bare taste judgment with nothing concrete
      behind it
- [ ] Heuristics requiring live interaction are named as deferred, not
      silently skipped or weakly proxied
- [ ] Findings that could instead be intentional design choices are flagged
      as ambiguous, not asserted as settled violations
- [ ] No code, style, markup, or design artifact was modified
- [ ] No finding was presented as an automatic override of a confirmed
      creative decision
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.


### Runtime pin resolution

Codex can discover both user and repository skills with the same name.
Before applying this skill, search upward from the current directory for
`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem
boundary. Read its `dest` value and
resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from
the currently loaded copy, **load and follow the pinned copy** before
continuing. A matching legacy `adapter.lock` remains valid during migration.
If the pinned file is unavailable, report the broken pin and
stop instead of silently falling back to the global copy.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `browser_automation` | `—` | manual-fallback |
| `structured_output` | `—` | native |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.
