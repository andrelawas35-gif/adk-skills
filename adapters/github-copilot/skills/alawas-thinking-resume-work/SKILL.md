---
name: alawas-thinking-resume-work
description: "Use when returning after a break to see where the studio stands and resume one thread; reads Work Objects read-only, ranks forward-motion work by recency, hands back one candidate with its state and next_action, and never writes anything."
default_tier: medium
platform: github-copilot
---
# Resume Work

## Governing principle

Resuming is not deciding. This skill reads the Work Objects directly, reports
where the workspace stands, and hands back exactly one candidate to pick up —
a named object with its state and recorded next action — then routes to the
conductor. It is read-only and never acquires mutation authority.

## Personal working lens

The capability already exists inside the conductor's status path; the problem
is that it sits in a skill entered for another purpose and reads a register
that is materially wrong. This skill is a separate, read-only orientation
skill so the director can answer "where were we?" without governance overhead.

A resume tool that refuses to point is `active.md` with extra steps. Naming a
candidate with visible grounds is not deciding for the director — the director
picks; the skill recommends.

## Boundaries and non-goals

**This skill does:**
- Read Work Object frontmatter across `.work-studio/objects/`
- Report three standing lines: unclosed count, oldest untouched, and
  `active.md` drift
- Rank forward-motion objects (notice/explore/design/build) by `updated_at`,
  most recently touched first
- Disqualify an active object with an empty `next_action`, reporting it by
  name rather than skipping silently
- Return exactly one candidate: its ID, state, and recorded `next_action`
- Name the state-to-skill routing table as belonging to the conductor; this
  skill does not copy it
- Route the candidate to `alawas-governance-conduct-work-object` with the ID
  and destination already named

**This skill does NOT:**
- Write, edit, or delete any file, including anything under `.work-studio/`
- Create, resume, transition, or annotate a Work Object
- Use `active.md` as a ranking input (drift is reported, not relied on)
- Surface a candidate from `verify` or `observe`
- Score, grade, or rank anything numerically; assign any aggregate health
  figure; or produce time-series metrics
- Decide that work is finished, or repair `active.md` (repair belongs to the
  conductor)
- Read bodies, apply model judgment about relative importance, or parse
  dependency/blocking prose

## Inputs and preconditions

**Required input:** none. Called with no arguments after a break.

**Preconditions:** the workspace root is identifiable (`.work-studio/objects/`
exists). If the objects directory is missing or unreadable, report that and
stop; do not substitute another store.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read Work Object files and `active.md`.
- `directory_list` — walk `.work-studio/objects/` without assuming what is there.
- `content_search` — locate the frontmatter fields across many files.
- `structured_output` — return the standing lines, the candidate, and the route.
- `user_confirmation` — required before any handoff that would mutate; the
  handoff here is to the conductor, which is the only skill permitted to write.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

This skill has no mutation authority of any kind and never acquires it. There
is no confirmation that promotes it into writing. Handing a candidate to the
conductor does not authorize the conductor to close, repair, or act on it —
the director decides what the candidate means. Do not stage, annotate, change
status, append History, or make any other mutation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

This is the resume lens: read Work Objects read-only, rank forward-motion work
by recency, and hand back exactly one candidate with its state and next_action,
never writing anything itself.

## Skill Grilling Profile

Apply the `alawas-thinking-resume-work` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Rank live work by recency and
forward-motion evidence, and hand back exactly one candidate with its state and
next_action before routing.

## Ranking procedure

1. **Read frontmatter.** Parse only the structured frontmatter of every file
   under `.work-studio/objects/`, treating quoted and bare scalar values
   identically (e.g. `status: "active"` and `status: active` are the same).
   Fields needed: `id`, `status`, `state`, `next_action`, `updated_at`,
   `created_at`. A file with no frontmatter is reported by name as a parse gap
   and skipped.
2. **Standing lines.** Compute and print:
   - **Unclosed count** — the number of `status: active` objects.
   - **Oldest untouched** — the active object with the earliest `updated_at`.
   - **`active.md` drift** — how many active objects are absent from the
     register (reported, never repaired here).
3. **Forward-motion pile.** From active objects, keep only states
   `notice`, `explore`, `design`, `build`. Exclude `verify` and `observe`.
4. **Disqualify.** Any forward-motion object with an empty `next_action` is
   disqualified and reported by name with its state. The schema promises
   `next_action` is resumable by a different agent; enforce that promise.
5. **Rank.** Order the remaining (eligible) candidates by `updated_at`,
   most recently touched first.
6. **Candidate.** Return exactly one: the top-ranked eligible object's ID,
   its state, and its recorded `next_action`. If none are eligible, return
   no candidate and say so — list the disqualifications by name and the three
   standing lines, and route to the conductor as "no candidate — director
   selects."

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
## Where the studio stands

- **Unclosed count:** <n active objects>
- **Oldest untouched:** <id> (updated <timestamp>)
- **active.md drift:** <n active objects absent from the register>

## Forward motion

- <id> — <state> — <eligible | disqualified: empty next_action> (updated <timestamp>)
- ... (ranked, most recently touched first)

## Candidate

- **ID:** <id>
- **State:** <state>
- **next_action:** <recorded text>

## Next move

Route to `alawas-governance-conduct-work-object` with the candidate ID and
destination named. Or: no candidate — director selects.
```

Sections appear only when they carry something.

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| `.work-studio/objects/` missing or unreadable | Report it, return no candidate, stop. Do not substitute another store. |
| A file has no parseable frontmatter | Report it by name as a parse gap; skip it; continue. Never silently drop it. |
| Quoted vs bare frontmatter values | Read them identically; a reader that handles only one form miscounts roughly a fifth of the workspace. |
| `active.md` missing or stale | Report drift as unverifiable or with the computed gap; do not use the register as a ranking input. |
| Every forward-motion object disqualified | Return no candidate, list disqualifications by name, route to the conductor; never fall back to `verify`/`observe`, never fabricate. |
| A capability is unavailable | Use its declared manual-fallback path; state exactly what remains unverified. |
| Git unavailable | Report the `active.md` drift line as unverifiable rather than asserting a value. |

## Anti-patterns

- Returning a candidate from `verify` or `observe` because that is where most
  live objects sit.
- Silently skipping an object with an empty `next_action` instead of reporting
  it by name.
- Reading `active.md` as ground truth for what is live.
- Adding a score, rank number, or health figure to the output.
- Copying the conductor's state-to-skill routing table into this skill.
- Repairing `active.md`, transitioning an object, or writing anything.
- Treating the candidate as an instruction to act rather than a proposal the
  director picks up.
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

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `directory_list` | `list_dir` | native |
| `content_search` | `grep_search` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
