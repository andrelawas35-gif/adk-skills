---
schema_version: 1
id: 2026-08-22-028
title: Build design-audit-accessibility skill
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T14:52:10Z
updated_at: 2026-08-22T15:05:57Z
next_action: Director decision: commit these changes (SKILL.md, routing map, pipeline doc, adapters, generated command-center.html fixes), or continue working uncommitted.







---
## Intent

Add `design-audit-accessibility` as a new skill in the design pipeline, owning
a frontier the pipeline currently disowns: accessibility *conformance*.

Grounded in `.work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md`
(produced by `alawas-research-produce-report`, WO `2026-08-22-027`), carried
forward as accepted source material. That report already established, with
file-level evidence, that:
- `design-steward-experience-patterns` explicitly disowns accessibility
  *compliance* claims (its SKILL.md:37 non-goal) — it only stewards
  accessibility *expectations* as pattern knowledge.
- `design-verify-design-implementation` marks WCAG/keyboard/screen-reader
  checks as **`deferred`** (SKILL.md:146) and states accessibility dimensions
  are explicitly not its focus (SKILL.md:20).
- No frontier in `tools/ws/design_asset_routing.py:FRONTIER_OWNERS` covers
  accessibility at all.

The report's proposed shape (not yet a binding decision, carried forward as a
starting point): a **read-only audit** skill mirroring
`design-audit-product-interface`'s posture — inspect the rendered interface
and codebase for WCAG conformance (contrast, keyboard nav, focus order,
ARIA/semantic structure, screen-reader labels) against expectations
`design-steward-experience-patterns` already stewards, and report findings.
Never mutates; never claims compliance without the evidence. New `accessibility`
frontier alongside `verify`; findings route to `design-apply-design-direction`
(as fix candidates) or the conductor (linked Work Object).

Not yet resolved: this is a *new skill for the studio itself*, not a design
asset flowing through the pipeline — so the exact authoring path (full
SKILL.md draft, boundaries, capability mappings, Grilling Profile, adapter
wiring) still needs to be designed, matching the studio's existing skill
structure and conventions rather than invented ad hoc.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A bounded tracer bullet tests the smallest real slice of the audit
      (e.g., contrast-ratio and semantic-structure checks against one real
      rendered page) before the full skill is authored
- [x] `design-audit-accessibility/SKILL.md` exists with boundaries,
      capability mappings, and Grilling Profile matching the other 10 design
      skills' structure
- [x] The new `accessibility` frontier is registered in
      `tools/ws/design_asset_routing.py:FRONTIER_OWNERS` and
      `references/DESIGN-ASSET-PIPELINE.md`'s ownership map and canonical
      route
- [x] The skill never mutates code/assets and never asserts compliance
      without cited evidence (mirrors steward's own guardrail)


## Constraints and non-goals

**Constraints:**
- Read-only posture, matching every other audit/verify skill in the pipeline
  — reports findings, never fixes or mutates.
- Must consume `design-steward-experience-patterns`'s stewarded accessibility
  *expectations* as the spec to test against, rather than inventing its own
  accessibility requirements.
- New frontier must be added to both the routing map and the pipeline
  reference doc — not left as an undeclared owner.

**Non-goals:**
- Claiming legal/regulatory accessibility compliance — the skill reports
  conformance findings against declared expectations, not a certification.
- Fixing any finding it surfaces — fixes route through
  `design-apply-design-direction` and `alawas-engineering-implement-bounded-change`
  like any other design-direction change.
- Reopening the other two recommendations from WO `2026-08-22-027`
  (`design-critique-usability`, `design-govern-interaction-motion`) — those
  remain separate, un-advanced recommendations unless the director opens
  their own Work Objects.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accept tracer bullet: static contrast/semantic-structure check against a real repo HTML file

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A one-off script parses `.work-studio/command-center.html`'s inline styles, computes WCAG contrast ratios for text/background pairs, and checks basic semantic structure (single `<h1>`, discernible accessible names on interactive elements, no color-only signal on `.cons-high`). Emits a plain findings report (check name, pass/fail/undetermined, concrete value). Read-only: no mutation of the target file, no browser automation, no network, no external target project. Explicitly excludes: full `design-audit-accessibility/SKILL.md`, frontier registration, dynamic checks needing a real browser (keyboard nav, focus order, screen-reader behavior), and any accessibility-expectations pattern authoring. |
| **Authorization** | Director: "Yes, go with that tracer" |
| **Confidence** | high that static parsing is the right first mechanism to test — the riskiest assumption (can contrast/structure be computed from static HTML alone, without a populated expectations pattern) is falsifiable cheaply this way; low confidence on whether static parsing will prove sufficient long-term, since real color values can depend on cascade/computed styles this script won't model — that gap is the tracer's own exit criterion, not a blocker to running it |
| **Actor** | director |
| **Revisit trigger** | Result of running the script against the real `command-center.html`. Concrete, legible findings (including at least one genuine finding, pass or fail) -> proceed to authoring the full skill using this mechanism. Signal only resolvable post-render (undetermined on most/all checks) -> stop, the audit needs real browser rendering instead of static parsing — a materially different mechanism requiring a fresh design pass. |
| **Rationale** | Building the full skill before verifying whether static analysis is even the right family of mechanism risks authoring around a technique that can't answer the real question. Testing against a real file already in this workspace (no external project needed) is the cheapest way to know before further design or implementation investment. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | design-steward-experience-patterns/SKILL.md:37 | "Claim accessibility compliance from a written [pattern]" is listed as an explicit non-goal — steward governs accessibility as *expectations*, never verifies them. |
| [system] | design-verify-design-implementation/SKILL.md:20,146 | Accessibility dimensions (WCAG, keyboard, screen reader) are explicitly not verify's focus and marked `deferred` in its dimensions table. |
| [system] | tools/ws/design_asset_routing.py:FRONTIER_OWNERS | No `accessibility` key exists in the frontier-ownership map — confirmed structurally, not just by SKILL.md text. |
| [system] | .work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md | Full report carried forward as source material; this Work Object advances only its highest-confidence recommendation (design-audit-accessibility), not the other two. |
| [decision] | director: "Advance design-audit-accessibility into its own Work Object" | Director selected this recommendation to advance from WO 2026-08-22-027's report; the other two (design-critique-usability, design-govern-interaction-motion) remain un-advanced. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | scratchpad/accessibility_tracer.py, executed against real .work-studio/command-center.html | Tracer bullet result: 15 static text/background color pairs computed via WCAG relative-luminance contrast formula -- 9 pass, 6 fail the 4.5:1 threshold (.id, .cons default, .stale, .attn, .count-empty, .card-link -- all using #888/#999 gray on white). 3 semantic-structure checks manually inspected against real source: single-h1 passes; the closed-Work-Objects toggle button lacks aria-controls/aria-expanded (fails); .cons-high conveys severity by color alone with no icon/text backup (fails), while .banner correctly pairs its icon with color (passes). Assumption holds: concrete, legible findings were produced from static HTML alone, without any populated accessibility-expectations pattern -- the tracer needed only WCAG's own generic thresholds as a baseline. Real, previously-unknown accessibility issues were surfaced as a side effect: command-center.html itself now has 6 known contrast fails and 2 structure fails to fix. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | tools/ws/command_center.py (fixed) + scratchpad/accessibility_tracer.py re-run | Director requested fixing exactly what the tracer found, nothing more. Fixed in the generator source (never the generated HTML directly): six #888/#999 gray text colors (.id, .cons, .stale, .attn, .count-empty, .card-link) changed to #666 (already validated passing elsewhere in the file at 5.74:1, kept the muted-secondary visual intent); .cons-high gained font-weight:600 as a non-color severity cue; the closed-Work-Objects toggle button gained aria-controls="closed-wrap" and aria-expanded, updated live by its click handler. Deliberately left .card-flag (red-only, same pattern as cons-high) unchanged -- it was not in the tracer's original findings, so touching it would exceed 'fix what it found'. Re-ran the tracer script against the regenerated command-center.html: 15/15 contrast pairs and 3/3 structure checks now pass, 0 failures. .work-studio/command-center.html regenerated via 'ws command-center' (29 active, 10 closed, 0 parse failures). |
| [system] | skills/core/design-audit-accessibility/SKILL.md, tools/generate-adapters.py --check | Authored the full skill: SKILL.md with Governing principle, Boundaries/non-goals, Inputs/preconditions, Required capabilities (file_read, browser_automation with manual-fallback, content_search, structured_output), Consequence/authority rules (low consequence, read-only), Grilling Profile entry added to references/SKILL-AWARE-GRILLING.md, 6-stage workflow, [system:accessibility-audit] output contract, and Final self-check -- matching the structure of the other 10 design skills. Mechanism upgraded from the tracer's pure-static approach to prefer browser-computed styles (via browser_automation) with static-parsing as the disclosed fallback, resolving Decision 1's low-confidence note about cascade/computed-style blind spots. Registered the new 'accessibility' frontier in tools/ws/design_asset_routing.py:FRONTIER_OWNERS and in references/DESIGN-ASSET-PIPELINE.md's ownership map and canonical route. Ran tools/generate-adapters.py: all three platform adapters (claude-code, codex, github-copilot) generated with zero drift on --check. |
## Open questions

- **Authoring path for a new studio skill.** This is not a design asset
  flowing through the pipeline — it is a new skill *for* the pipeline. The
  exact process (SKILL.md structure, adapter generation via
  `tools/generate-adapters.py`, Grilling Profile authoring, capability
  mapping table) needs to follow the studio's existing skill-authoring
  convention. Not yet investigated in this Work Object.
- **Tracer scope.** What is the smallest real slice to test first — a single
  accessibility check (e.g., contrast ratio) against one real rendered page,
  or a broader pass? Not yet decided.
- **Where accessibility expectations come from in practice.** Steward
  stewards these as pattern knowledge, but no real Work Object has yet
  produced a populated accessibility-expectations pattern to audit against —
  the tracer may need to produce one first, or use a synthetic expectation
  set.

## Next move

Route to `alawas-design-design-tracer-bullet`: design the smallest bounded,
observable, reversible tracer for the accessibility audit — e.g., verify
that a real accessibility check (contrast ratio, semantic structure) can run
read-only against one real rendered interface and produce a findings report,
before the full `design-audit-accessibility/SKILL.md` is authored and wired
into the frontier map. Carry forward the three Evidence ledger entries above
(disowned-frontier evidence) as given context, not re-derived.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T14:53:07Z — Classified and staged for design-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director advanced the design-audit-accessibility recommendation from WO 2026-08-22-027's report. Intent, Success evidence, Constraints/non-goals, and three carried-forward Evidence entries recorded. Skipping explore -- the prior report already resolved which frontier is disowned and why (accessibility conformance), with file-level evidence. Remaining open questions (studio skill-authoring path, tracer scope, source of real accessibility expectations) are design-tracer-bullet's remit.
### 2026-08-22T14:58:11Z — Tracer bullet accepted, running accessibility check

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted: static contrast/semantic-structure check against .work-studio/command-center.html as the smallest real slice.
### 2026-08-22T14:59:16Z — Tracer bullet passed -- static contrast/structure checks produced concrete findings

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Real static analysis against command-center.html: 6/15 contrast pairs fail 4.5:1, 2/3 semantic-structure checks fail. Assumption confirmed: static parsing can produce legible, concrete findings without a populated accessibility-expectations pattern. Per Decision 1's exit criteria, proceeding is warranted -- next is authoring the full design-audit-accessibility/SKILL.md and registering the accessibility frontier, plus a separate decision on whether to fix the two real issues this tracer surfaced in command-center.html itself.
### 2026-08-22T15:05:57Z — Full skill authored, wired, and adapter-generated -- all four success-evidence criteria met

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** design-audit-accessibility/SKILL.md authored matching the 10-skill design pipeline's structure. New accessibility frontier registered in both the routing map and pipeline reference doc. All three platform adapters (claude-code, codex, github-copilot) regenerated with zero drift. Nothing committed yet -- director decision on committing these changes is the same open item the command-center Work Object (2026-08-22-006) already surfaced for this repo's uncommitted work.
