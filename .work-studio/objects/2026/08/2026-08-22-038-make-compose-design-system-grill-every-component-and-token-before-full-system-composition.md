---
schema_version: 1
id: 2026-08-22-038
title: Make compose-design-system grill every component and token before full-system composition
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T20:20:17Z
updated_at: 2026-08-22T20:33:04Z
next_action: Director decision: commit these changes, or continue working uncommitted.









---
## Intent

Explore how to make `design-compose-design-system` grill every component and
token before it reaches a composed design system, so composition stays
aligned with the director's actual intent rather than accepting values or
names on request alone. Director wants every grill question to offer
options, not open-ended prompts.

Grounded in this session's own `command-center-foundation` composition
(WO `2026-08-22-037`): that composition asked confirmation questions, but
never ran an actual Grilling Session — a real, live example of the gap this
idea targets. Also grounded in a concrete discovery: `design-compose-design-system/SKILL.md`
already claims to apply a Grilling Profile in
`references/SKILL-AWARE-GRILLING.md`, but no such profile section exists
there — whatever direction is chosen, that profile must be authored, not
just tuned.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] At least three materially different directions are grounded in the
      current studio's actual grilling mechanics (Candidate Card, threshold,
      serial-depth/breadth-sweep modes) and compose-design-system's real gap
      (no authored profile).
- [x] Each direction states plainly whether it changes *when* grilling
      triggers (mandatory vs. threshold-gated) or *what* it asks, since
      "every component and token" is in tension with the studio's existing
      default (nominate only under a three-part threshold, never
      universally).
- [x] The director selects one or more directions before design begins.
- [x] A tracer bullet proves the combined mechanism against a real pending
      decision before any profile is authored.
- [x] All three Grilling Profiles (compose-design-system,
      govern-interaction-motion, steward-experience-patterns) are authored
      and wired, with zero adapter drift.


## Constraints and non-goals

**Constraints:**
- Preserve the director's stated requirement: every grill question offers
  options, never an open-ended prompt.
- Ground directions in the real Grilling Session engine
  (`references/AGREEMENT-LOOP.md`) rather than inventing a parallel
  mechanism.

**Superseded by Decision 1** (recorded here, not silently dropped): this
Inquiry originally scoped itself to `design-compose-design-system` only and
named cross-skill extension as an explicit non-goal. The director's
selection explicitly extended scope to `design-govern-interaction-motion`
and `design-steward-experience-patterns` as well — the original single-skill
scoping no longer governs.

**Non-goals (still standing):**
- Authoring the actual Grilling Profile text, SKILL.md changes, or any
  schema/tooling change before a tracer bullet tests the combined
  mandatory + breadth-sweep mechanism.
- Retroactively re-grilling the already-composed `command-center-foundation`
  asset (WO `2026-08-22-037`) — that asset stands as composed; this Inquiry
  is about future compositions.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 2 — Accept tracer bullet: live breadth-sweep session resolving the toggle-motion asset's pending properties

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Resolve `toggle-expand-collapse-motion.asset.md`'s three unconfirmed properties (duration, easing curve, reduced-motion behavior) as one breadth-sweep-mode Grilling Session: mandatory nomination (no threshold check), one branch per property, every question multiple-choice only. Tests the combined mechanism (Direction 1 + Direction 2) against a real, already-pending asset. Explicitly excludes: authoring the actual Grilling Profile text for any of the three skills, touching compose-design-system or steward-experience-patterns, implementing motion in code. |
| **Authorization** | Director: "Yes, go with that tracer" |
| **Confidence** | high that this is a real, non-fabricated test case since the asset record already states these properties as unresolved; medium on whether all three properties can be cleanly forced into multiple-choice form without distorting the real answer -- that is exactly what this tracer tests |
| **Actor** | director |
| **Revisit trigger** | Any property resists multiple-choice framing without distorting the real answer -> mechanism needs adjustment before authoring any profile. All three resolve cleanly and the asset validates -> proceed to author all three Grilling Profiles. |
| **Rationale** | Testing the mechanism against a real, already-open decision is cheaper and more honest than a fabricated scenario, and it produces real value (the motion asset actually gets resolved) regardless of the tracer's outcome for the broader mechanism question. |

### Direction 1: Mandatory Pre-Composition Grill Gate (local override of the standing threshold)

- **Core idea**: `design-compose-design-system`'s stage workflow gains a new
  mandatory step before classifying any property as inherited/overridden/
  prohibited: every token or component input is always nominated as a
  Grilling Candidate — never gated by the studio's standing three-part
  threshold (`AGREEMENT-LOOP.md`). The Candidate Card still shows every time,
  and the director can still decline any individual card; what changes is
  that nomination itself becomes unconditional for this one skill, an
  explicit, scoped deviation from the studio-wide default.
- **Distinctness claim**: this is the only direction that changes *when*
  grilling triggers (mandatory vs. threshold-gated) while leaving every
  other mechanic (Candidate Card, one-question-per-turn, serial-depth/
  breadth-sweep modes) exactly as it already exists.
- **Key assumption**: the value of catching misalignment on every single
  token/component outweighs a Candidate Card appearing even for trivial,
  low-risk additions.
- **Smallest test**: run compose-design-system once on a real 3-token
  addition to an existing foundation; count how many Candidate Cards
  appear and how many the director actually accepts vs. declines.

### Direction 2: Per-Composition Breadth-Sweep Grilling Round

- **Core idea**: instead of one Candidate Card per individual token or
  component, every artifact proposed in a single composition pass becomes
  one branch inside a single continuous `breadth-sweep`-mode Grilling
  Session (`AGREEMENT-LOOP.md`'s existing mode, not a new one). One
  decision-bearing question per turn, rotating across branches, and the
  session doesn't end until every branch — every token/component in that
  composition — has been explicitly resolved or explicitly deferred.
- **Distinctness claim**: centers on session *structure* (one sustained
  multi-branch session per composition) rather than a gate per individual
  item; reuses the existing breadth-sweep mode rather than inventing new
  per-item gating logic.
- **Key assumption**: the director wants one sustained back-and-forth that
  walks the whole proposed system in one sitting, not repeated
  interruptions per item.
- **Smallest test**: compose a foundation with 4 new tokens as one
  breadth-sweep session; check whether the branch-rotation clause
  (`AGREEMENT-LOOP.md:186`) stays legible across all 4 items without the
  director losing track of which branch is active.

### Direction 3: Author and Sharpen the Missing Grilling Profile (no new trigger)

- **Core idea**: don't add any new mandatory gate. Instead, author the
  Grilling Profile `design-compose-design-system/SKILL.md` already claims
  to use but that does not actually exist in `SKILL-AWARE-GRILLING.md` —
  and make its Gates and Pressure scenario genuinely per-token/per-component
  specific (e.g., "does this token's semantic name match its actual CSS
  usage," "does this component variant silently duplicate an existing
  one"). The nomination trigger stays exactly the studio default
  (threshold-gated, opt-in) — only the *questions asked once triggered*
  get sharper.
- **Distinctness claim**: the lightest-touch, most standard-preserving
  direction — doesn't touch frequency or session structure, only content.
  Directly closes the concrete gap found this session (the profile section
  doesn't exist).
- **Key assumption**: the studio's existing threshold discipline is
  already right; what's missing is specificity in what gets asked, not how
  often grilling happens.
- **Smallest test**: apply the sharpened profile retroactively (as a
  thought experiment only, not a re-grill) to this session's real
  `command-center-foundation` composition (WO `2026-08-22-037`) — would
  sharper gates have surfaced the `#555`/`#666` and `0.5px`/`1px`
  consolidation questions as actual grilling turns, rather than the single
  plain confirmation message I sent?

### Direction 4: Mechanical Alignment Checklist (no Grilling engine at all)

- **Core idea**: add a structural, schema-enforced checklist instead of a
  conversational session — e.g., a required "Token/Component Alignment"
  section in the asset-record schema (`DESIGN-ASSET-REGISTRY.md`) with
  explicit fields per artifact: semantic name matches usage (yes/no),
  conflicts with an existing token (yes/no/named conflict), value already
  used under a different name (yes/no/named), inheritance status
  confirmed (yes/no). `validate_asset_record()` rejects a composed
  foundation missing this section, the same way it already rejects missing
  required fields today.
- **Distinctness claim**: the only direction that doesn't invoke the
  Grilling Session engine at all — trades conversational depth for
  deterministic, scriptable, always-enforced coverage. No Candidate Cards,
  no continuous session, no "declining" a question.
- **Key assumption**: what the director actually wants is *guaranteed
  completeness* (nothing skipped, ever, enforced by tooling), not
  necessarily a Socratic back-and-forth that could in principle be rushed
  through.
- **Smallest test**: add the checklist section to
  `asset-template.asset.md` and to `validate_asset_record()`'s
  `REQUIRED_SECTIONS`; test against the already-composed
  `command-center-foundation` record to see whether it would fail
  validation retroactively (illustrating the gap, not re-grilling it).

### Decision 1 — Combine Direction 1 + Direction 2; extend scope beyond compose-design-system

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Combine Direction 1 (mandatory pre-composition grilling — every token/component is always nominated as a Grilling Candidate, overriding the studio's standing three-part threshold for these skills specifically) with Direction 2 (session structure — every artifact proposed in one composition pass becomes one branch inside a single continuous `breadth-sweep`-mode session, not a separate Candidate Card per item). Applied to three skills, expanding beyond this Inquiry's original scope: `design-compose-design-system`, `design-govern-interaction-motion`, and `design-steward-experience-patterns` — the studio's three asset-composing/stewarding skills. Each needs its own authored Grilling Profile (none currently exist for compose-design-system or govern-interaction-motion in a findable form; steward-experience-patterns' status was not checked in this Inquiry and is a carried gap). Every grilling question in all three profiles must offer options, never an open-ended prompt, per the director's original constraint. |
| **Authorization** | Director: "combination of 1 and 2 and apply only to compose-design-system, motion, and steward" |
| **Confidence** | high on the combination logic (mandatory trigger + breadth-sweep structure compose cleanly, per Directions 1 and 2's own text); medium on scope completeness — steward-experience-patterns' current Grilling Profile status was never checked in this Inquiry (only compose-design-system's absence was confirmed), so this Decision inherits that gap rather than resolving it |
| **Actor** | director |
| **Revisit trigger** | If steward-experience-patterns turns out to already have a working Grilling Profile, the "author from scratch" assumption for that skill is wrong and needs correcting before authoring proceeds. |
| **Rationale** | The director wants no token, component, or governed property to reach any of these three skills' composed output without being explicitly grilled with option-based questions, structured as one sustained session per composition rather than scattered single-item interruptions. Extending beyond compose-design-system reflects that this is a property of "asset composition/stewardship" generally, not one skill specifically. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | design-compose-design-system/SKILL.md 'Apply the design-compose-design-system profile in SKILL-AWARE-GRILLING.md'; grep of that file | No design-compose-design-system Grilling Profile section exists in references/SKILL-AWARE-GRILLING.md. Two orphaned, unheaded blocks sit between build-design-foundation and verify-design-implementation's entries, but they cover screen architecture and user-flow topics, not composition -- likely leftover from skills that predate the current design-* set. Whichever direction is selected, this profile has to be authored, not merely tuned. |
| [system] | grep of references/SKILL-AWARE-GRILLING.md for alawas-design-steward-experience-patterns | Confirmed: no Grilling Profile section exists for design-steward-experience-patterns either, same as design-compose-design-system. All three skills in scope (compose-design-system, govern-interaction-motion, steward-experience-patterns) need a profile authored from scratch, not tuned. Closes the medium-confidence gap noted in Decision 1. |
| [system] | live breadth-sweep Grilling Session, WO 2026-08-22-038, applied to .work-studio/design-assets/toggle-expand-collapse-motion.asset.md | Tracer bullet result: all 3 branches (duration, easing, reduced-motion) resolved cleanly via multiple-choice-only questions, rotating one branch per turn -- duration=150ms, easing=ease-in-out, reduced-motion=shorten to 50ms rather than remove. No branch needed to escape into an open-ended answer; the director's 'options for every grill question' constraint held for all three. Asset record updated with confirmed recipe, re-validated (6 assets, 0 gaps). Assumption holds: the combined mandatory-nomination + breadth-sweep mechanism can compose a real governed asset end-to-end without becoming confusing or forcing an artificial choice. |
| [system] | skills/core/design-compose-design-system/SKILL.md, skills/core/design-govern-interaction-motion/SKILL.md, skills/core/design-steward-experience-patterns/SKILL.md, references/SKILL-AWARE-GRILLING.md, tools/generate-adapters.py --check | Authored the mandatory-nomination + breadth-sweep override into all three skills' Grilling entry sections, replacing their prior threshold-gated language. Authored new Grilling Profile sections in SKILL-AWARE-GRILLING.md for compose-design-system and steward-experience-patterns (neither existed before); updated the existing govern-interaction-motion profile with the mandatory override, an option-only honesty gate, and the real toggle-motion precedent. Fixed two profile-name references (compose-design-system, steward-experience-patterns) that omitted the alawas- prefix used by every actual header in that file -- a pre-existing drift, not introduced by this change, but one that would have made 'Apply the X profile' resolve to nothing. All three platform adapters regenerated with zero drift. |
## Open questions

- **Discoverable, not yet checked**: does the studio have an existing
  precedent for "always-multiple-choice" grilling questions anywhere, or
  would Direction 1/2/3 need to establish that pattern for the first time?
  (Direction 4 sidesteps this — a checklist's fields are inherently
  yes/no/named, not open questions.)
- **Not discoverable — needs director input**: should this same pattern
  (whichever is selected) extend to `design-steward-experience-patterns`
  and `design-govern-interaction-motion`, the other two skills that also
  compose/steward governed assets? This Inquiry is scoped to
  `design-compose-design-system` only, per its own non-goals.
- **Not discoverable — needs director input**: is "every component and
  token" meant as a hard, no-exceptions requirement (favoring Direction 1
  or 4), or a strong default that can still be waived by explicit director
  request (favoring Direction 2 or 3, which preserve more of the existing
  threshold discipline)?

## Next move

Route to `alawas-design-design-tracer-bullet`: design the smallest bounded
test of the combined mechanism (mandatory nomination + breadth-sweep
session structure) before authoring three Grilling Profiles from scratch.
No profile, SKILL.md change, or schema change has been authored yet.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T20:21:32Z — Generated four differentiated directions for grilling every component/token

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director's idea is genuinely ambiguous across two independent dimensions: when grilling triggers (mandatory vs threshold-gated) and what mechanism enforces it (conversational session vs mechanical checklist). Grounded directions in the real Agreement Loop engine and the concrete discovery that design-compose-design-system has no authored Grilling Profile at all.
### 2026-08-22T20:26:04Z — Director selected combination of Direction 1 + Direction 2, scope extended to 3 skills

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director combined mandatory nomination (Direction 1) with breadth-sweep session structure (Direction 2), and extended scope beyond the original single-skill framing to all three asset-composing/stewarding skills: design-compose-design-system, design-govern-interaction-motion, design-steward-experience-patterns. Confirmed none of the three currently has an authored Grilling Profile. Routing to design-tracer-bullet to test the combined mechanism before authoring three profiles from scratch.
### 2026-08-22T20:27:33Z — Tracer bullet accepted, running live breadth-sweep grilling session

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted: resolve toggle-expand-collapse-motion's three pending properties as one breadth-sweep session, mandatory nomination, multiple-choice only.
### 2026-08-22T20:29:47Z — Tracer bullet passed -- combined mechanism resolved a real pending decision cleanly

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Live breadth-sweep session resolved all 3 pending properties on toggle-expand-collapse-motion.asset.md via multiple-choice-only questions; asset re-validated (6 assets, 0 gaps). Per Decision 2's exit criteria, proceeding to author all three Grilling Profiles is warranted.
### 2026-08-22T20:33:04Z — All three Grilling Profiles authored and wired -- all five success-evidence criteria met

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Mandatory nomination + breadth-sweep override applied to compose-design-system, govern-interaction-motion, and steward-experience-patterns' Grilling entry sections. Three Grilling Profile sections authored/updated in SKILL-AWARE-GRILLING.md, each with an option-only honesty gate matching the director's 'options for every grill question' requirement. A pre-existing profile-name reference drift (missing alawas- prefix) was found and fixed in two skills. All three platform adapters regenerated with zero drift. Nothing committed yet.
