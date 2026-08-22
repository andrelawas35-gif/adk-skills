---
name: alawas-research-produce-report
description: "Use when a broad research question or an already-decided Work Object trail needs to become one standalone deliverable document; composes investigate-live-question per sub-question or synthesizes accepted Decisions/History; never authors prospective architecture, exports, or replaces human authority."
default_tier: medium
platform: codex
---
# Produce Report

## Governing principle

A deliverable earns its place by resolving supersession across a whole trail
and giving evidence a standalone identity someone can read without opening a
Work Object — not by being a longer version of one answered question. This
skill's exit condition is a *produced deliverable*, not a *resolved
uncertainty*: it composes `alawas-research-investigate-live-question`'s question-answering
discipline for research-type output, or synthesizes an already-decided trail
for plan-type output, and stops there. It never invents an answer to save a
sub-question, and it never authors architecture, roadmap items, or future
decisions no one has accepted yet.

## Boundaries and non-goals

**This skill does:**

- Decompose a broad research request into falsifiable sub-questions and
  invoke `alawas-research-investigate-live-question` once per sub-question (directly, or via
  `subagent_spawn` when sub-questions are independent).
- For a plan-type deliverable, read one Work Object's (or a linked successor
  chain's) existing `Decisions and revisit triggers` and `History` sections
  directly — no sub-questions, no new investigation, synthesis only.
- Detect and resolve supersession across a time-ordered trail: a stale
  `next_action`, `## Next move`, or an earlier Decision an evidence trail
  later overturned is dropped from the deliverable, not concatenated in.
- Author one standalone document at
  `.work-studio/deliverables/<work-object-id>-<slug>.md`.
- Link the deliverable from its originating Work Object's body with one line
  — never duplicate the full document inline.
- Attribute every claim in the deliverable to the sub-question outcome or
  Decision it came from.
- Route completion, gaps, and unresolved sub-questions back to
  `alawas-governance-conduct-work-object`.

**This skill does NOT:**

- Author new speculative architecture, roadmap items, or unaccepted future
  decisions in a plan-type deliverable — a plan is a synthesis of what was
  already decided, never a forecast (bounded by the source Work Object's own
  Decision, e.g. `2026-08-21-008` Decision 1).
- Answer a sub-question itself — that discipline belongs entirely to
  `alawas-research-investigate-live-question`; this skill composes it, never duplicates or
  bypasses its evidence rules.
- Export, publish, or write the deliverable anywhere outside
  `.work-studio/` without the explicit, per-instance confirmation
  `alawas-governance-conduct-work-object`'s authority rules already require for any write
  outside that boundary.
- Contact people, production, or sensitive sources — any sub-question
  needing that stays inside `alawas-research-investigate-live-question`'s own authority
  gate, not loosened by being called from here.
- Implement, deploy, or operate anything a plan-type deliverable describes.
- Treat a deliverable as evidence in its own right — it is a compiled
  presentation of existing evidence, never a new source.

## Inputs and preconditions

**Required inputs:**
- An activated Work Object naming a broad research or plan request.
- For a report-type deliverable: enough of the request to decompose into
  distinct falsifiable sub-questions.
- For a plan-type deliverable: the source Work Object ID(s) whose
  Decisions/History will be synthesized — those objects must be readable
  and contain at least one Decision with `Result: pass`.

**Preconditions:**
- `alawas-governance-conduct-work-object` has established the Work Object.
- For report-type work, `alawas-research-investigate-live-question` is available to invoke
  per sub-question; this skill does not imitate it when unavailable.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read the Work Object(s), source Decisions/History, and prior
  sub-question outcomes.
- `file_write` — write the deliverable file and link it from the originating
  Work Object.
- `directory_list` — check `.work-studio/deliverables/` for naming collisions.
- `content_search` — locate a source Work Object's relevant Decisions.
- `subagent_spawn` — parallelize independent sub-question investigations
  (optional; sequential invocation of `alawas-research-investigate-live-question` is always
  valid).
- `structured_output` — produce the deliverable and its linking record.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Writing the deliverable inside `.work-studio/deliverables/` is ordinary
  write authority under the Work Object's existing consequence level — no
  broader gate than any other conductor-mediated write.
- Writing the deliverable, or a copy of it, anywhere outside
  `.work-studio/` requires the same explicit, per-instance confirmation
  `alawas-governance-conduct-work-object` requires for any write outside that boundary. This
  skill does not carry standing export authority.
- A plan-type deliverable that would need to author a new decision (not
  merely synthesize an accepted one) is a material boundary crossing — stop
  and route to `alawas-thinking-pressure-test-decision` rather than writing it in.
- For a high-consequence Work Object, confirmation must name the exact
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

This is the synthesis lens: pursue supersession and contradiction across the
whole trail being compiled, not depth on any one sub-question (that depth
belongs to `alawas-research-investigate-live-question`). Nominate a Candidate Card only when
a genuine authority boundary appears — most often, a plan-type request that
turns out to need a new decision, not a synthesis of an old one.

## Skill Grilling Profile

Apply the `alawas-research-produce-report` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Challenge every synthesized claim
against its source Decision or sub-question outcome, and challenge every
dropped (superseded) entry against the possibility that it was dropped
wrongly.

## Stage workflow

### 1. Classify the deliverable type

Report-type (multiple falsifiable sub-questions, no single source Work
Object already holds the answer) or plan-type (one Work Object or linked
chain whose accepted Decisions/History should become a readable document).
If the request mixes both, decompose into separate deliverables rather than
blending an unresolved question into a plan synthesis.

### 2. Gather the source material

- **Report-type:** decompose the request into distinct falsifiable
  sub-questions. Invoke `alawas-research-investigate-live-question` once per sub-question
  (parallel via `subagent_spawn` when independent). Collect each outcome
  (`answered`/`reframed`/`prototype-ready`/`unresolved`) with its evidence
  ledger.
- **Plan-type:** read the source Work Object(s)' `Decisions and revisit
  triggers` and `History` in full. Do not invoke `alawas-research-investigate-live-question`
  — there is no falsifiable question here, only already-decided material.

### 3. Resolve supersession

Walk the gathered material in time order. When a later Decision or History
entry overturns, corrects, or narrows an earlier one (a stale `next_action`,
a corrected framing, a deferred item), keep only what the final record
supports. Note what was dropped and why in the deliverable's own
provenance trail — silently dropping material is not the same as
resolving it.

### 4. Author the deliverable

Write one structured, standalone document at
`.work-studio/deliverables/<work-object-id>-<slug>.md`. Every claim
carries the provenance of its source (sub-question outcome or Decision
number). A plan-type deliverable states explicitly, near its top, that it
synthesizes only already-accepted material and authors nothing new.

### 5. Link, never duplicate

Add one line to the originating Work Object's body pointing at the
deliverable's path. Do not embed the deliverable's full content inline —
that defeats the standalone-document identity this skill exists to
provide (confirmed structural gap, `2026-08-21-008` Decision 3).

### 6. Route completion

Report the deliverable's path, its type, its source sub-questions or
Decisions, and any unresolved sub-question or dropped-material note. Route
to `alawas-governance-conduct-work-object` for durable recording. An unresolved
sub-question is reported honestly inside the deliverable, never silently
omitted or invented.

## Evidence rules

- Apply `capabilities/classify-provenance.md`: every claim in the
  deliverable carries the tag its source material already had — a
  synthesized `[system]` fact stays `[system]`, an `[inference]` stays
  `[inference]`. Synthesis itself (which entries superseded which,
  how sub-question outcomes fit together) is `[inference]` and must be
  labeled as such, never presented as source evidence.
- A dropped, superseded entry is recorded as dropped, with the reason, not
  silently omitted.
- An unresolved sub-question appears in the deliverable as unresolved — the
  deliverable's completeness never implies a resolution that didn't happen.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

This skill does not mutate a Work Object directly. On completion, pass the
conductor:

- the deliverable's path, type (report/plan), and word/section count;
- the source sub-questions or Decision numbers it drew from;
- any dropped/superseded material and why;
- any unresolved sub-question or gap the deliverable surfaces;
- the one-line link to add to the originating Work Object's body.

The conductor owns schema validation, optimistic concurrency, the link edit,
and History. If recording is unavailable, return the exact record and one
concrete manual instruction; do not claim it was written.

## Routing and termination

- **Deliverable produced:** route to `alawas-governance-conduct-work-object` with the path
  and source material; do not imply the deliverable was exported or shared.
- **A sub-question came back unresolved:** report it honestly inside the
  deliverable; route to `alawas-research-investigate-live-question` again only if the director
  wants that specific gap closed before finalizing.
- **A plan-type request needs a new decision, not a synthesis:** stop before
  authoring it in. Route to `alawas-thinking-pressure-test-decision`.
- **Capability gap:** use manual-fallback when it preserves the boundary, or
  stop as unsupported; state exactly what remains unverified.

## Output template

Apply `references/DIRECTOR-LANGUAGE.md` to everything said to the
director. Lead with plain meaning; attach the technical term to the explanation
rather than substituting it. Order anything worth explaining as: what's
happening, why it matters, the technical term, the evidence, the
recommendation, what needs deciding. Short answers stay short, and any part may
be marked absent — "Evidence: none, this is inference" is valid and preferred.
Never fill a part to complete the shape. Never phrase a decision in terms the
director must decode before choosing. Record content is never translated:
field names, state names, record IDs, and file paths stay exact.

```markdown
## Deliverable produced

- **Work Object:** <id and current state>
- **Deliverable type:** <report | plan>
- **Path:** `.work-studio/deliverables/<id>-<slug>.md`
- **Source material:** <sub-question outcomes, or Decision numbers synthesized>
- **Supersession resolved:** <what was dropped and why, if anything>
- **Gaps carried into the deliverable:** <unresolved sub-questions, if any>
- **Route:** conductor — link and record
```

## Anti-patterns

- Authoring new architecture, roadmap items, or forecasts inside a
  plan-type deliverable — synthesis only.
- Embedding the full deliverable inline in the Work Object body instead of
  linking it — defeats the standalone-document identity this skill exists
  to provide.
- Dropping stale or superseded material without noting that it was dropped.
- Answering a sub-question directly instead of invoking
  `alawas-research-investigate-live-question` — bypasses its evidence discipline.
- Presenting synthesis/editorial judgment as source evidence rather than
  `[inference]`.
- Writing the deliverable outside `.work-studio/` without the explicit
  per-instance confirmation that requires.

## Final self-check

- Is the deliverable type (report/plan) explicit, and does the gathering
  method match it?
- Does a plan-type deliverable synthesize only already-accepted material,
  with zero new architecture or forecasts?
- Is every claim attributed to its source sub-question or Decision?
- Is dropped/superseded material noted, not silently omitted?
- Does the deliverable live at `.work-studio/deliverables/` and is it
  linked, not duplicated, from the Work Object?
- Did I avoid exporting or writing outside `.work-studio/` without explicit
  per-instance confirmation?
- Is any unresolved sub-question reported honestly rather than papered over?
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
| `file_write` | `create_file / replace_string_in_file` | native |
| `directory_list` | `list_dir` | native |
| `content_search` | `grep_search` | native |
| `subagent_spawn` | `runSubagent` | native |
| `structured_output` | `—` | native |
