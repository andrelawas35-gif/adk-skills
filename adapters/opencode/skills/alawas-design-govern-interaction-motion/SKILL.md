---
name: alawas-design-govern-interaction-motion
description: "Use when governed motion or interaction behavior needs timing, easing, or state rules; records direction and never implements code or mutates canonical assets."
default_tier: high
platform: opencode
---
# Govern Interaction Motion

## Governing principle

`alawas-design-build-design-foundation` discovers animation and transition tokens that
already exist in code; `alawas-design-verify-design-implementation` checks whether a
state transition fires correctly, as one behavioral dimension among others
it does not focus on. Neither composes or stewards motion as a reusable
design asset the way tokens, themes, and UX patterns already are governed.
This skill closes that gap: it composes and stewards motion/interaction
behavior — timing, easing, per-state behavior, and reduced-motion handling
— as a governed asset record, the same discipline `alawas-design-compose-design-system`
already applies to tokens and themes. It keeps creative authority with the
director: this skill proposes and records motion composition, and it never
silently chooses a motion decision or mutates canonical assets itself.

## Boundaries and non-goals

This skill does:

- Compose and revise governed motion/interaction asset records: named
  motion recipes, timing and easing semantics, per-state interaction
  behavior, and `prefers-reduced-motion` handling.
- Record which motion properties are inherited from a foundation, overridden
  for a specific case, prohibited, or awaiting creative confirmation.
- Inspect local asset records under `.work-studio/design-assets/`, the
  routing rules in `references/DESIGN-ASSET-PIPELINE.md`, and the record
  shape in `references/DESIGN-ASSET-REGISTRY.md`.
- Route discovery of existing animation/transition tokens to the skill that
  owns it, and consume that discovery as an input rather than re-scanning.
- Return a compact composition record through the conductor for
  confirmation, implementation, and verification.

This skill does not:

- Discover existing animation/transition tokens from code; route to
  `alawas-design-build-design-foundation`.
- Check whether an interaction fires correctly in a running application;
  route to `alawas-design-verify-design-implementation`.
- Silently choose a motion/timing decision or approve a motion recipe on
  the director's behalf.
- Mutate canonical asset records, the component ledger, code, or external
  design tools by itself.
- Implement any motion or interaction in code — composition produces a
  governed asset record; implementation routes through
  `alawas-engineering-implement-bounded-change`.

## Inputs and preconditions

**Required input:** an activated Work Object that names the motion/interaction
outcome. Minimum evidence is asset or project identity, the requested motion
or interaction outcome, any current animation/transition token inventory
when discoverable, confirmed creative direction or an explicit gap, and
constraints on inheritance, overrides, prohibited properties, and reduced-
motion handling. Missing fields remain gaps.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. No particular Work Object state is required —
motion composition can begin once a motion/interaction outcome is named,
independent of whether a specific visual direction has been confirmed
elsewhere.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback,
or unsupported and follows `references/CAPABILITY-DEGRADATION.md` when
needed.

- `file_read` and `content_search` — inspect permitted asset records,
  pipeline references, Work Objects, and component-ledger pointers.
- `directory_list` — discover local design asset records.
- `terminal_run` — run focused validation such as
  `python -m tools.ws validate design-assets`.
- `file_write` — return a compact composition record through the conductor.
- `user_confirmation` — obtain scoped authority before creative selection,
  source-token mutation, code writes, external design-tool sync, export, or
  schema migration.
- `structured_output` — report composition, inheritance, overrides,
  prohibitions, gaps, authority boundary, and revisit trigger.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only classification inside the current workspace is allowed.
- Creative selection, source-token mutation, code writes, external
  design-tool sync, export, and schema migration require scoped authority.
- For a high-consequence Work Object, confirmation must name the exact
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full, with one explicit override
for this skill (WO `2026-08-22-038` Decision 1): every motion or
interaction property proposed for composition — timing, easing, trigger,
reduced-motion behavior — is always nominated as a Grilling Candidate; the
standing three-part threshold does not gate nomination here. All
properties proposed for one motion asset are grilled as a single
continuous `breadth-sweep`-mode session (`AGREEMENT-LOOP.md`'s existing
mode), one branch per property, one multiple-choice question per turn.
Every grill question must offer explicit options — never an open-ended
prompt. Proven in practice: `asset.design.toggle-expand-collapse-motion`'s
duration, easing, and reduced-motion behavior were each resolved this way.

## Skill Grilling Profile

Apply the `alawas-design-govern-interaction-motion` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge whether each motion
property is truly inherited, overridden, or prohibited; whether creative
authority was confirmed for every non-trivial timing or easing choice;
whether reduced-motion handling was addressed rather than assumed; and
whether composition stays in one owning frontier.

## Design asset pipeline

Use `references/DESIGN-ASSET-PIPELINE.md` to keep intake distinct from
system composition, UX-pattern stewardship, creative application,
implementation, verification, component governance, and workbench
projection. Use `references/DESIGN-ASSET-REGISTRY.md` for the local
file-backed asset record shape — `motion` is a valid `Asset kind`.

## Stage workflow

### 1. Identify the asset or project record

Identify the motion/interaction asset by explicit asset ID or file path, or
recognize that none yet exists and this is a new draft.

### 2. Validate the local registry shape

Run `python -m tools.ws validate design-assets` when possible. A motion
asset record uses the same generic record shape as every other asset kind
(`Asset Summary`, `Lifecycle`, `Verification Notes`, `Rollback`) — no
kind-specific structured fields exist for motion properties. Timing,
easing, trigger, and reduced-motion behavior are recorded as clear prose in
`Asset Summary`, matching the studio's decision not to add a bespoke
structural carve-out for one asset kind ahead of real use showing prose is
insufficient (see Revisit trigger).

### 3. Confirm the requested outcome and creative direction

Confirm what motion/interaction behavior is being composed and whether a
creative direction (timing feel, easing curve, choreography) has already
been confirmed elsewhere, or remains an explicit gap.

### 4. Classify inheritance, overrides, and prohibitions

Classify which motion properties are inherited from a foundation or shared
motion recipe, which are overridden for this specific case, which are
explicitly prohibited (e.g., no motion at all under
`prefers-reduced-motion`), and which await creative confirmation.

### 5. Compose the record

Compose the motion/interaction asset as a record for the director's
confirmation. Do not mutate canonical assets, ledgers, code, or external
tools.

### 6. Route the confirmed composition

Route the confirmed composition to the next owning skill.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; local asset records, validation
  output, Work Objects, and component-ledger entries are `[system]`.
- User creative choices and accepted routes are `[decision]`.
- Composition and inheritance judgments are `[inference]` unless already
  recorded as decisions.
- Missing fields, unconfirmed creative choices, and source-of-truth
  conflicts are `[gap]`.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the asset identifier, source record, requested outcome, composition
record, confirmed creative direction, inheritance/override/prohibition
summary, reduced-motion handling, gaps, authority needs, and revisit
trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Existing animation/transition token discovery ->
  `alawas-design-build-design-foundation`.
- Existing route, layout, component, or interface discovery ->
  `alawas-design-audit-product-interface`.
- Reusable user goals, flows, states, accessibility, or content behavior ->
  `alawas-design-steward-experience-patterns`.
- Confirmed creative interpretation and execution boundary ->
  `alawas-design-apply-design-direction`.
- Reversible implementation of an accepted tracer or bounded change ->
  `alawas-engineering-implement-bounded-change`.
- Browser-visible behavioral parity (does the interaction fire correctly) ->
  `alawas-design-verify-design-implementation`.
- Durable shipped component registration -> `alawas-design-track-components`.
- Read-only catalog, graph, comparison, or trace view ->
  `alawas-design-project-asset-workbench`.
- Ambiguous owner, unconfirmed creative direction, or scope expansion ->
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
## Motion/interaction composition

- **Asset/Project:** <asset ID or project identity and source record>
- **Work Object:** <provenance and current lifecycle state>
- **Requested outcome:** <motion recipe, timing/easing, or interaction-behavior goal>
- **Creative direction:** <confirmed choice or explicit gap>
- **Composition:** <inherited, overridden, prohibited, and awaiting-confirmation properties>
- **Reduced-motion handling:** <addressed, or explicit gap>
- **Validation:** <executed registry check, result, and gaps>
- **Authority boundary:** <what this composition does not authorize>
- **Revisit trigger:** <when to recompose or reopen>
```

## Anti-patterns

- Treating composition as permission to choose a timing or easing decision
  silently.
- Assuming reduced-motion handling rather than recording it as addressed
  or an explicit gap.
- Copying motion, token, theme, UX-pattern, or projection truth into the
  component ledger.
- Mutating canonical asset records, code, or external design tools from the
  composition step.
- Letting a workbench projection become the source of truth.
- Routing to multiple owners instead of naming the ambiguity.

## Final self-check

- [ ] Did I identify the asset/project and its source of truth?
- [ ] Did I validate or explicitly mark validation as unavailable?
- [ ] Did I preserve director authority over every creative timing/easing
      choice?
- [ ] Did I address reduced-motion handling rather than assume it?
- [ ] Did I avoid mutating assets, ledgers, projections, code, or external
      tools?
- [ ] Did I route to exactly one owner or preserve ambiguity as a gap?

## Revisit trigger

Reopen the decision to keep motion properties as prose (not a structured
subsection) if real motion asset records accumulate and show that prose in
`Asset Summary` cannot clearly carry timing/easing/trigger information —
at that point, add a structured `Motion Properties` subsection to
`references/DESIGN-ASSET-REGISTRY.md` and this skill's stage workflow,
rather than continuing to force it into prose.
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
