---
schema_version: 1
id: 2026-08-22-037
title: Compose a governed design foundation for the command center
type: project
status: active
state: design
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T20:14:02Z
updated_at: 2026-08-22T20:41:17Z
next_action: Run mandatory-nomination breadth-sweep grilling session on the three newly reopened properties.





---
## Intent

Compose a governed design-system foundation (a `foundation`-kind asset under
`.work-studio/design-assets/`) for `tools/ws/command_center.py`'s inline
styles, so its colors, typography, and spacing become named, reusable,
inherited-by-default tokens instead of the current bare, repeated hex/px
literals.

Grounded directly in `alawas-design-build-design-foundation`'s just-completed
token discovery (this session, read-only, no file changes): the command
center has zero CSS custom properties, five ad hoc font sizes, mixed rem/px
spacing with no declared scale, and no semantic color naming (`#b91c1c`
means "danger" in two unrelated places with nothing tying them together).

This is the first `foundation`-kind asset in this repo's design-assets
registry — no existing foundation to inherit from, so this is greenfield
composition, not a revision.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A composed foundation record is proposed (not yet mutated into code),
      naming every discovered raw value as a semantic token candidate
- [x] Every proposed token is classified as inherited (none, greenfield),
      overridden (n/a), prohibited (n/a), or awaiting creative confirmation
      — nothing is silently chosen as if already decided
- [x] The director confirms or revises the proposed token names/values
      before any asset record or code mutation happens
- [x] `python -m tools.ws validate design-assets` passes once the record is
      written


## Constraints and non-goals

**Constraints:**
- This skill (`design-compose-design-system`) never silently chooses a
  creative naming/value decision on the director's behalf — every proposed
  token is presented for confirmation, not asserted as settled.
- Does not re-discover tokens from code — that discovery already happened
  and is the input here, not repeated.
- Does not mutate `tools/ws/command_center.py`, `command-center.html`, or
  any canonical asset record until the director confirms the composition.

**Non-goals:**
- Fixing any of the 7 gaps the discovery found (dark mode, responsive
  breakpoints, etc.) — this Work Object only organizes what already exists
  into named tokens; expanding coverage is a separate, later decision.
- Implementing the foundation in code — that's
  `alawas-engineering-implement-bounded-change`'s job, after a confirmed
  direction via `design-apply-design-direction`.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Confirm command-center foundation token composition

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Compose asset.design.command-center-foundation naming every discovered raw CSS value from tools/ws/command_center.py as a semantic token. Three specific naming questions resolved: (1) color.text.muted and color.text.subtle consolidated into one token, color.text.muted = #666 -- the count-pill's current #555 usage becomes a noted divergence to reconcile at implementation, not silently changed here; (2) border widths standardized to one token, border.width.default = 1px -- the .row hairline's current 0.5px becomes a noted divergence to reconcile at implementation; (3) the 6-step px spacing scale (4/6/8/10/12/14) kept exactly as observed, not rounded to a stricter grid. |
| **Authorization** | Director: "Consolidate to one, standardize borders to 1px, keep spacing as-is" |
| **Confidence** | high -- these are naming/organization decisions over already-discovered values, not new creative choices; the two consolidations (color, border) are recorded as intentional future code changes, not yet applied to command_center.py |
| **Actor** | director |
| **Revisit trigger** | If implementing this foundation (via design-apply-design-direction) surfaces a real visual reason the retired #555/0.5px values were intentional rather than incidental drift. |
| **Rationale** | A studio-native foundation should name what the director actually wants going forward, not preserve every incidental inconsistency the discovery found. Consolidating and standardizing now, before any code implementation, keeps the foundation record and the eventual code change in sync rather than composing a foundation that documents inconsistency as if it were intentional. |

### Decision 2 — Grill and resolve the three open code/record divergences

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Applied the mandatory-nomination + breadth-sweep grilling override (WO `2026-08-22-038` Decision 1) to this foundation directly, on director request ("grill me the design system of the command center"). Three open branches, each with explicit multiple-choice options: (1) `.count-pill`'s `#555` vs. `color.text.muted`'s `#666` — resolved: update code to `#666`. (2) `.row`'s `0.5px` border vs. `border.width.default`'s `1px` — resolved: update code to `1px`. (3) `font.family.mono`'s bare `monospace` — resolved: expand to a real fallback stack (`ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`) in both token and code. |
| **Authorization** | Director: "A." (branch 1), "A" (branch 2), "A." (branch 3) — each a distinct multiple-choice answer to its own grill question. |
| **Confidence** | high — each was a direct multiple-choice selection by the director, not an inference. |
| **Actor** | director |
| **Revisit trigger** | None expected; if a future foundation revision reopens color/border/font tokens, re-grill those branches fresh rather than assuming this resolution still applies. |
| **Rationale** | This is the first real use of the mandatory-nomination + breadth-sweep grilling mechanism directly on `design-compose-design-system` since the mechanism was authored (WO `2026-08-22-038`). All three previously-deferred properties are now resolved, closing every open gap this foundation record carried. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|


## Open questions

- Whether to expand this foundation's coverage (dark mode, breakpoints,
  motion) is explicitly out of scope here and undecided.

## Next move

All three grilled divergences (`.count-pill` color, `.row` border,
`font.family.mono` fallback stack) are resolved to "update code." Route to
`design-apply-design-direction` to confirm the concrete code change, then
`alawas-engineering-implement-bounded-change`, then
`design-verify-design-implementation`.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T20:14:32Z — Routed from token discovery to design-compose-design-system

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director asked to route the just-completed command-center token discovery into a governed foundation. No creative-system Work Object existed, so one was created directly at design (not explore) since the discovery already resolved what tokens exist -- only their naming/organization into a foundation remains, which is design-compose-design-system's remit, not a divergent-exploration question.
### 2026-08-22T20:17:42Z — Foundation composed and confirmed -- all four success-evidence criteria met

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** asset.design.command-center-foundation composed and validated (6 assets, 0 gaps). All raw CSS values from command_center.py named as semantic tokens; the two director-confirmed consolidations (color, border) recorded as explicit divergences from current code, not silently applied. Nothing in code has changed yet.
### 2026-08-22T20:39:46Z — Grilled and resolved the foundation's 3 open divergences via breadth-sweep session

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Applied the mandatory-nomination + breadth-sweep grilling override directly to design-compose-design-system per director's explicit grill request. All three branches (.count-pill color, .row border, mono font fallback) resolved to update-code, recorded as Decision 2. Asset record updated to reflect resolution; no code changed yet.
### 2026-08-22T20:41:17Z — Reopen foundation to grill expanded scope (dark mode, breakpoints, motion tokens)

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director asked to grill and expand the command-center foundation's scope, reopening the three items explicitly deferred at composition time (dark-mode variants, responsive breakpoints, animation/transition tokens). This is new composition work, not verification, so moving back to design.
## artifacts

- `.work-studio/design-assets/command-center-foundation.asset.md` (fingerprint: `763187dc86f6`, commit: uncommitted at record time) — Composed foundation asset record: command-center design tokens, colors/typography/spacing
