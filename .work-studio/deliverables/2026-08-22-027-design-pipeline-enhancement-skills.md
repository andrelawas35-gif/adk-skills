# Design pipeline enhancement — recommended additional skills

- **Deliverable type:** report (research)
- **Work Object:** provisional `2026-08-22-027` (awaiting conductor registration; see routing note at end)
- **Request:** "Recommend additional skills that should be added to my design pipeline to enhance it."
- **Method:** each recommendation is grounded in a *verified* gap in the current
  10-skill design pipeline — the frontier map in `tools/ws/design_asset_routing.py`
  and `references/DESIGN-ASSET-PIPELINE.md`. A capability counts as a gap only when
  no existing skill *owns* it. Mentions-in-passing were checked against ownership and
  rejected where a skill only references a concern it explicitly disowns.

> This report synthesizes an investigation of the current pipeline. It authors no
> new architecture or roadmap — each proposed skill is a *recommendation with its
> evidence*, to be accepted, reshaped, or declined through the normal Work Object
> route. Ranking and "this is a gap" judgments are `[inference]`; file-level facts
> are `[system]`.

## The current pipeline (baseline)

Ten design skills plus two cross-domain handoffs, routed by design-asset *frontier*
(`design_asset_routing.py:FRONTIER_OWNERS`):

| Frontier | Owner |
|----------|-------|
| identity / intake | `design-manage-assets` |
| interface discovery | `design-audit-product-interface` |
| token discovery | `design-build-design-foundation` |
| system composition (foundation, tokens, themes, variants, families) | `design-compose-design-system` |
| UX patterns (goals, flows, states, accessibility *expectations*, content *behavior*) | `design-steward-experience-patterns` |
| creative direction + execution | `design-apply-design-direction` |
| implementation | `alawas-engineering-implement-bounded-change` |
| browser parity vs. confirmed direction | `design-verify-design-implementation` |
| component registration | `design-track-components` |
| read-only projection | `design-project-asset-workbench` |

The pipeline is strong on **discovery → composition → direction → implement → verify →
register → project**. The gaps below are the frontiers nothing owns.

---

## Recommended skills (ranked by evidence strength)

### 1. `design-audit-accessibility` — HIGHEST confidence

**The gap.** Accessibility *conformance* is owned by no one — and is explicitly
disowned by the two skills a reader would expect to cover it:

- `[system]` `design-steward-experience-patterns/SKILL.md:37` lists "claim
  accessibility compliance from a written [pattern]" as a **non-goal**. It stewards
  accessibility *expectations* as pattern knowledge, and cannot verify them.
- `[system]` `design-verify-design-implementation/SKILL.md:146` — its dimensions
  table marks `Accessibility (WCAG, keyboard, screen reader)` as **`deferred`**;
  line 20 confirms accessibility "dimensions are [not the focus]."

So the pipeline *defines* accessibility expectations (steward) and *defers* testing
them (verify) — a clean structural hole. `[inference]` This is the single highest-value
addition: it converts a disowned concern into an owned frontier.

**Proposed shape.** A **read-only audit** skill, mirroring `design-audit-product-interface`'s
posture (inspect, never mutate): run against the rendered interface and codebase for
WCAG conformance — contrast ratios, keyboard navigation, focus order, ARIA/semantic
structure, screen-reader labels — and report findings against declared expectations.
- **Frontier entry:** new `accessibility` frontier, sits alongside `verify`.
- **Handoffs:** consumes steward's accessibility *expectations* as the spec to test
  against; reports failures back to `design-apply-design-direction` (fix as direction)
  or the conductor (linked Work Object).
- **Authority posture:** read-only, like the other audit/verify skills. It *reports*
  conformance; it never *claims* compliance without the evidence, matching steward's
  own guardrail.

### 2. `design-critique-usability` — HIGH confidence

**The gap.** `[system]` A grep across all 10 design skills for
`heuristic | critique | usability evaluation | nielsen` returns **zero** matches.
`design-verify-design-implementation` checks *parity to the confirmed direction* — i.e.
"did we build what was agreed" — but nothing evaluates whether the design is actually
*good*: heuristic evaluation independent of a specific direction. `[inference]` A design
can pass verify (matches the mock exactly) and still be a poor experience; nothing in
the pipeline catches that.

**Proposed shape.** A skill that evaluates a design/interface against usability
heuristics (visibility of system status, error prevention, recognition over recall,
consistency, etc.), producing ranked, evidence-linked findings — not a pass/fail
against a mock, but a critique of the design on its own terms.
- **Frontier entry:** new `critique` frontier, positioned *before* implementation
  (critique the direction/tracer) and optionally *after* verify (critique what shipped).
- **Handoffs:** findings route to `design-apply-design-direction` as candidate
  direction changes, never auto-applied.
- **Authority posture:** read-only evaluation; produces findings, holds no creative
  authority (director still decides which critiques to act on).

### 3. `design-govern-interaction-motion` — MEDIUM-HIGH confidence

**The gap.** Motion/interaction exists only as *discovered tokens*, never as a
*designed and governed asset*:

- `[system]` `design-build-design-foundation/SKILL.md:93,125` inventories
  "animation/transition tokens" — read-only discovery of what already exists.
- `[system]` `design-verify-design-implementation/SKILL.md:43` checks "state
  transitions" only as *behavioral correctness*, and behavioral is explicitly not its
  focus (line 20).
- `[inference]` No skill *composes or stewards* interaction behavior — timing curves,
  motion choreography, micro-interaction states, reduced-motion accessibility. The
  `FRONTIER_OWNERS` map has no motion/interaction frontier at all.

**Proposed shape.** A composition/stewardship skill (sibling to
`design-compose-design-system` and `design-steward-experience-patterns`) that governs
motion and interaction as reusable assets: named motion recipes, timing/easing
semantics, per-state interaction behavior, and `prefers-reduced-motion` handling.
- **Frontier entry:** new `interaction-motion` frontier, between system composition
  and experience-pattern stewardship.
- **Authority posture:** composes/stewards asset truth like its siblings; preserves
  director creative authority; never mutates canonical assets without route.

---

## Partial gaps — noted honestly, weaker recommendations

These are frontiers *partially* covered. `[inference]` Each could become a skill, but
the case is softer because an existing skill already carries part of the load. Recorded
so they are not silently dropped, and not oversold.

- **Visual divergent exploration (comps).** `[system]`
  `thinking-develop-idea/SKILL.md` is "the system's first and only divergent" step and
  "generates strongly differentiated directions." So *direction* divergence exists. What
  is absent is *visual* divergence — multiple comparable layout/mock alternatives to
  look at, not just described directions. `[system]`
  `design-apply-design-direction/SKILL.md:99` handles vagueness by asking *one*
  clarifying question, not by generating options. **Recommendation:** likely reuse
  `thinking-develop-idea` rather than build a new skill, unless visual comps become a
  recurring need.

- **Design↔code token/theme drift.** `[system]` `design-track-components` reopens
  entries on "git drift," but scoped to *component-contract* grilling debt
  (`SKILL.md:67,121`), not to divergence between a design-system token/theme asset and
  its code implementation. **Recommendation:** consider *extending* `track-components`
  or `build-design-foundation` (which already reads live tokens) to flag token/theme
  drift, before adding a standalone skill.

- **Content / UX-writing craft.** `[system]` `design-steward-experience-patterns`
  stewards "content behavior" and "content requirements" as *expectations*
  (`SKILL.md:21,47`) — but, exactly as with accessibility, stewarding an expectation is
  not crafting or reviewing the copy. **Recommendation:** lower priority; revisit if
  microcopy/voice-and-tone becomes a repeated frontier.

---

## What I deliberately did **not** recommend, and why

- **A "design exploration" skill** — `[system]` divergent generation already exists
  (`thinking-develop-idea`); recommending a duplicate would violate the pipeline's
  one-owner-per-frontier rule (`DESIGN-ASSET-PIPELINE.md:92`).
- **An external-tool sync / Figma skill** — `[system]` external tool sync is an
  explicitly *gated* action outside this pipeline's scope
  (`DESIGN-ASSET-PIPELINE.md:64–67`); it belongs behind scoped authority, not as a
  routine pipeline skill.
- **A deployment/publishing skill** — already owned outside the design pipeline by
  `alawas-operations-deploy-with-recovery`.

## Provenance summary

- `[system]` facts: file/line references above, and
  `tools/ws/design_asset_routing.py`, `references/DESIGN-ASSET-PIPELINE.md`.
- `[inference]` (synthesis/editorial): the ranking, the "structural hole" framing, the
  partial-vs-hard gap distinction, and each proposed skill's shape. None of these are
  accepted decisions — they are recommendations pending director choice.
- No sub-question required contacting people, production, or sensitive sources.

## Gaps carried into this deliverable

- No live usability/user evidence was gathered — recommendations rest on pipeline
  structure, not observed user harm. If the director wants a gap prioritized by *impact
  evidence* rather than *structural absence*, that is a separate investigation.
