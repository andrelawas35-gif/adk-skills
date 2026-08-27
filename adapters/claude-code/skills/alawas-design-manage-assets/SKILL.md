---
name: alawas-design-manage-assets
description: "Use when a design asset needs identity, status, provenance, impact, or routing; classifies the frontier and never creates, mutates, or approves assets."
default_tier: high
platform: claude-code
---
# Manage Design Assets

## Governing principle

A design asset is useful only when the studio knows what it is, where its truth
lives, why it exists, what depends on it, and which skill owns the next
question. Keep identity and routing separate from creative production,
implementation, verification, component governance, and workbench projection.

## Boundaries and non-goals

This skill does:

- Classify a design asset's identity, kind, lifecycle status, source of truth,
  provenance, current frontier, dependencies, and next owning skill.
- Inspect local asset records under `.work-studio/design-assets/` and the
  routing rules in `references/DESIGN-ASSET-PIPELINE.md`.
- Report missing identity, missing source-of-truth, ambiguous ownership, and
  projection/source-of-truth drift as gaps.
- Route the next question to the one skill that owns the current asset
  frontier.

This skill does not create, edit, approve, style, implement, verify, register,
export, deploy, or retire assets by itself.

This skill does not:

- Choose creative direction or silently revise a theme, component, token, UX
  pattern, or implementation.
- Mutate the component ledger, generate adapters, write to external design
  tools, or turn a workbench projection into source truth. It does not become
  the source of truth.
- Replace the Work Object lifecycle, the component ledger, or the asset
  registry validator.

## Inputs and preconditions

Use an activated Work Object that names the design asset or asset question.
Minimum evidence is an asset identifier, asset kind, lifecycle status, source
of truth, Work Object provenance, current frontier, and any known dependency or
projection links. Missing fields remain gaps.

## Required capabilities

- `file_read` and `content_search` - inspect permitted asset records, pipeline
  references, Work Objects, and component-ledger pointers.
- `directory_list` - discover local design asset records.
- `terminal_run` - run focused validation such as
  `python -m tools.ws validate design-assets`.
- `file_write` - return a compact routing record through the conductor.
- `user_confirmation` - obtain scoped authority before any asset mutation,
  creative approval, external tool sync, ledger write, export, deployment, or
  destructive action.
- `structured_output` - report identity, status, gaps, route, and revisit
  trigger.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only classification inside the current workspace is allowed.
- Asset creation, source-of-truth changes, creative approval, implementation,
  verification, component-ledger mutation, projection export, external design
  tool sync, schema migration, destructive action, deployment, or sharing
  requires the owning specialist and any scoped authority that specialist
  requires.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Outside explicit grilling,
nominate a Candidate only when an ownership ambiguity, source-of-truth conflict,
or proposed external effect would materially change the route.

## Skill Grilling Profile

Apply the `alawas-design-manage-assets` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge identity, source-of-truth
claims, lifecycle status, projection drift, ledger overlap, and whether the
next frontier truly has one owner.

## Design asset pipeline

Use `references/DESIGN-ASSET-PIPELINE.md` to keep asset intake distinct from
system composition, UX-pattern stewardship, creative application,
implementation, verification, component governance, and workbench projection.
Use `references/DESIGN-ASSET-REGISTRY.md` for the local file-backed asset
record shape.

## Stage workflow

1. Identify the asset record by explicit asset ID or file path. If neither is
   present, report an identity gap instead of searching broadly.
2. Validate the local registry shape when possible with
   `python -m tools.ws validate design-assets`.
3. Classify asset kind, lifecycle status, source of truth, Work Object
   provenance, projections, dependencies, and current frontier.
4. Apply the pipeline ownership map. Route to exactly one next owning skill:
   `alawas-design-compose-design-system`, `alawas-design-steward-experience-patterns`,
   `alawas-design-apply-design-direction`, `alawas-engineering-implement-bounded-change`,
   `alawas-design-verify-design-implementation`, `alawas-design-track-components`, or
   `alawas-design-project-asset-workbench`.
5. If two owners appear plausible, preserve the ambiguity as a gap and route to
   outcome review or decision rather than choosing silently.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; local asset records, validation output,
  Work Objects, and component-ledger entries are `[system]`.
- User creative choices and accepted routes are `[decision]`.
- Ownership and next-route judgments are `[inference]` unless already recorded
  as decisions.
- Missing fields, source-of-truth conflicts, and projection drift are `[gap]`.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the asset identifier, source record, lifecycle status, current frontier,
validation result, dependency/projection links, gaps, recommended owning skill,
authority needs, and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Theme, token, variant, or component-family composition ->
  `alawas-design-compose-design-system`.
- User goal, flow, state, content, accessibility, or recovery behavior ->
  `alawas-design-steward-experience-patterns`.
- Confirmed creative interpretation or code-facing design change ->
  `alawas-design-apply-design-direction`.
- Accepted reversible implementation path ->
  `alawas-engineering-implement-bounded-change`.
- Browser-visible parity check -> `alawas-design-verify-design-implementation`.
- Durable shipped component registration -> `alawas-design-track-components`.
- Read-only catalog, graph, comparison, or trace view ->
  `alawas-design-project-asset-workbench`.
- Ambiguous owner, source-of-truth conflict, or scope expansion -> conductor for
  decision or outcome review.

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
## Design asset routing

- **Asset:** <asset ID, kind, status, and source record>
- **Work Object:** <provenance and current lifecycle state>
- **Validation:** <executed registry check, result, and gaps>
- **Current frontier:** <one frontier or ambiguity>
- **Recommended owner:** <one owning skill and why>
- **Authority boundary:** <what this route does not authorize>
- **Revisit trigger:** <when to reclassify or reopen>
```

## Anti-patterns

- Treating asset intake as permission to create or change the asset.
- Letting a workbench projection become the source of truth.
- Copying token, theme, UX-pattern, or projection truth into the component
  ledger.
- Choosing a creative direction because an asset record is incomplete.
- Routing to multiple owners instead of naming the ambiguity.

## Final self-check

- Did I identify the asset and source of truth?
- Did I validate or explicitly mark validation as unavailable?
- Did I route to exactly one owner or preserve ambiguity as a gap?
- Did I avoid mutating assets, ledgers, projections, code, or external tools?
- Did I preserve director authority over creative choices?
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
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 80000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read` | native |
| `content_search` | `Grep` | native |
| `directory_list` | `Bash ls` | native |
| `terminal_run` | `Bash` | native |
| `file_write` | `Write / Edit` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
