---
name: alawas-design-steward-experience-patterns
description: "Use when reusable UX goals, flows, states, accessibility, content, or recovery patterns need stewardship; governs evidence links and never styles or implements them."
default_tier: high
platform: opencode
---
# Steward Experience Patterns

## Governing principle

A reusable experience pattern preserves user outcome and behavior across visual
themes and implementations. Keep it behavioral and evidence-linked: this skill
stewards goals, flows, states, accessibility expectations, content behavior,
and recovery behavior as reusable knowledge, and it does not style, implement,
or register those patterns itself.

## Boundaries and non-goals

This skill does:

- Steward reusable user goals, flows, state models, accessibility
  expectations, content behavior, and failure/recovery behavior.
- Record happy, empty, loading, error, and recovery behavior for a recurring
  experience, plus the UI components or component families that realize it.
- Link research, testimony, or implementation evidence to the pattern record.
- Inspect local asset records under `.work-studio/design-assets/`, the routing
  rules in `references/DESIGN-ASSET-PIPELINE.md`, and the record shape in
  `references/DESIGN-ASSET-REGISTRY.md`.
- Route visual expression, implementation, verification, and component
  registration to the skills that own them.
- Return a compact stewardship record through the conductor for confirmation,
  implementation, and verification.

This skill does not:

- Style the pattern or choose visual themes for it.
- Implement code or verify browser parity against a rendered direction.
- Replace user research or claim accessibility compliance from a written
  pattern alone.
- Register durable components in the component ledger by itself.
- Mutate canonical asset records, the component ledger, code, or external
  design tools by itself.

## Inputs and preconditions

Use an activated Work Object that names the experience pattern. Minimum
evidence is the user goal and context; the flow states including happy, empty,
loading, error, and recovery behavior; content requirements and accessibility
expectations; linked UI components or component families; and any research,
testimony, or implementation evidence when available. Missing fields remain
gaps.

## Required capabilities

- `file_read` and `content_search` - inspect permitted asset records, pipeline
  references, Work Objects, and component-ledger pointers.
- `directory_list` - discover local design asset records.
- `terminal_run` - run focused validation such as
  `python -m tools.ws validate design-assets`.
- `file_write` - return a compact stewardship record through the conductor.
- `user_confirmation` - obtain scoped authority before accessibility claims,
  external research, personal-data use, production analytics, code changes, or
  component-ledger writes.
- `structured_output` - report states, behavior, accessibility and content
  expectations, evidence links, gaps, authority boundary, and revisit trigger.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only stewardship inside the current workspace is allowed.
- Accessibility claims, external research, personal data, production analytics,
  and code changes require scoped authority.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full, with one explicit override
for this skill (WO `2026-08-22-038` Decision 1): every user goal, flow
state, accessibility expectation, or content behavior proposed for a
pattern record is always nominated as a Grilling Candidate — the standing
three-part threshold does not gate nomination here. All properties
proposed for one pattern are grilled as a single continuous
`breadth-sweep`-mode session (`AGREEMENT-LOOP.md`'s existing mode), one
branch per property, one multiple-choice question per turn. Every grill
question must offer explicit options — never an open-ended prompt.

## Skill Grilling Profile

Apply the `alawas-design-steward-experience-patterns` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge whether each state and recovery
behavior is grounded in evidence, whether accessibility expectations are
claims rather than compliance proof, and whether the pattern stays in one
owning frontier.

## Design asset pipeline

Use `references/DESIGN-ASSET-PIPELINE.md` to keep intake distinct from system
composition, UX-pattern stewardship, creative application, implementation,
verification, component governance, and workbench projection. Use
`references/DESIGN-ASSET-REGISTRY.md` for the local file-backed asset record
shape.

## Stage workflow

1. Identify the pattern record by explicit asset ID or file path.
2. Validate the local registry shape when possible with
   `python -m tools.ws validate design-assets`.
3. Reconstruct the user goal, flow states, happy/empty/loading/error/recovery
   behavior, content requirements, and accessibility expectations.
4. Record evidence links and mark missing evidence as gaps; do not inflate a
   written pattern into a compliance or research claim.
5. Steward the pattern as a record for the director's confirmation; do not
   mutate canonical assets, ledgers, code, or external tools.
6. Route the confirmed pattern to the next owning skill.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; local asset records, validation output,
  Work Objects, and component-ledger entries are `[system]`.
- User creative choices and accepted routes are `[decision]`.
- Behavioral and state-model judgments are `[inference]` unless already
  recorded as decisions.
- Missing fields, ungrounded accessibility claims, and source-of-truth
  conflicts are `[gap]`.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the asset identifier, source record, user goal, flow states, behavior
summary, accessibility and content expectations, evidence links, gaps,
authority needs, and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Visual token or theme expression for the pattern ->
  `alawas-design-compose-design-system`.
- Confirmed creative interpretation and execution boundary ->
  `alawas-design-apply-design-direction`.
- Reversible implementation of an accepted tracer or bounded change ->
  `alawas-engineering-implement-bounded-change`.
- Browser-visible design parity -> `alawas-design-verify-design-implementation`.
- Durable shipped component registration -> `alawas-design-track-components`.
- Read-only catalog, graph, comparison, or trace view ->
  `alawas-design-project-asset-workbench`.
- Ambiguous owner, ungrounded accessibility claim, or scope expansion ->
  conductor for decision or outcome review.

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
## Experience-pattern stewardship

- **Asset:** <asset ID, kind, status, and source record>
- **Work Object:** <provenance and current lifecycle state>
- **User goal:** <goal and context>
- **States and behavior:** <happy, empty, loading, error, recovery behavior>
- **Accessibility and content:** <expectations or explicit gaps>
- **Evidence links:** <research, testimony, or implementation evidence>
- **Validation:** <executed registry check, result, and gaps>
- **Authority boundary:** <what this stewardship does not authorize>
- **Revisit trigger:** <when to re-steward or reopen>
```

## Anti-patterns

- Styling a pattern or choosing its visual themes from the stewardship step.
- Claiming accessibility compliance from a written pattern alone.
- Treating a pattern record as a substitute for user research.
- Copying token, theme, UX-pattern, or projection truth into the component
  ledger.
- Mutating canonical asset records, code, or external design tools from the
  stewardship step.
- Routing to multiple owners instead of naming the ambiguity.

## Final self-check

- Did I identify the pattern and its source of truth?
- Did I validate or explicitly mark validation as unavailable?
- Did I keep behavior, evidence, and accessibility claims distinct?
- Did I avoid styling, implementing, or registering the pattern by myself?
- Did I route to exactly one owner or preserve ambiguity as a gap?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **full 6‑tag system** (`references/epistemic/epistemic-rules-full.md`).

The epistemic tier is resolved from the skill's `default_tier` (high).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: high`.
The platform overlay resolves this to `anthropic/claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 80000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read` | native |
| `content_search` | `grep` | native |
| `directory_list` | `list` | native |
| `terminal_run` | `bash` | native |
| `file_write` | `edit / write / apply_patch` | native |
| `user_confirmation` | `question / permission ask` | native |
| `structured_output` | `—` | native |
