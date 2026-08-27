# Skills needed to comfortably work with Claude Design, tied to asset management

- **Deliverable type:** report (research)
- **Work Object:** `2026-08-22-035`
- **Request:** "What additional skills are needed in my Work Studio that I can
  comfortably work with Claude Design. What do you recommend. Make sure it is
  also tied to my asset management."
- **Method:** three falsifiable sub-questions, each answered directly from
  repository evidence (skill files, the registry schema, and this session's
  confirmed Claude Design tool capabilities) — no external research needed,
  the gap is structural and internal to this repo.

> This report recommends; it does not implement. Each recommendation is a
> candidate for its own Work Object if accepted — nothing here is built.

## Grounding: what Claude Design integration exists today

`[system]` Exactly two skills mention Claude Design at all, and neither is a
dedicated integration:

- `design-apply-design-direction` — Path B routes to Claude Design for
  *generation/editing*, gated behind an authentication probe and per-operation
  confirmation (SKILL.md:58,149-169). It defines two evidence-entry formats
  for Work Objects: `[system:design-project-ref]` (a Claude Design project
  reference) and `[system:design-approval]`.
- `design-verify-design-implementation` — treats a Claude Design visual
  reference as strictly *optional*, browser evidence is always primary
  (SKILL.md:117).

`[system]` The Claude Design tool itself (`DesignSync`, confirmed connected
and authenticated this session) supports: `list_projects`, `create_project`,
`list_files`, `get_file`, `finalize_plan`, `write_files`, `delete_files`,
`register_assets`. Its own description states it is meant to pair with a
`/design-sync` skill — no such skill file exists locally in this repo's
`skills/core/` (confirmed by direct search).

## Sub-question 1 — Does any skill own "sync to an external design tool" as its frontier?

**Answer: no, and the gap is repeated, not a one-off oversight.**

`[system]` Five separate places in the pipeline name external-design-tool sync
as an explicitly *excluded* or *gated* action, and none of them name an owner:

- `design-build-design-foundation/SKILL.md:35` — "Sync tokens to external
  design tools" listed as something this skill does *not* do.
- `design-compose-design-system/SKILL.md:166`, `design-govern-interaction-motion/SKILL.md:223`,
  `design-steward-experience-patterns/SKILL.md:166` — each lists "mutating...
  or external design tools" as an anti-pattern.
- `references/DESIGN-ASSET-PIPELINE.md:71` (Handoff rule 4) — "Treat external
  design tools... as gated actions requiring scoped authority" — a rule with
  no corresponding owner in the Ownership map.
- `design-manage-assets/SKILL.md` — lists "external design tool sync" among
  actions that "require the owning specialist," but its own Routing and
  termination section names exactly 7 owners, none of them for this action.

`[gap]` `design-project-asset-workbench` (the read-only projection skill) also
has no Claude Design awareness — it cannot even *display* that an asset's
truth lives partly in a Claude Design project.

## Sub-question 2 — Is a Claude Design project linked to the asset registry that already governs everything else?

**Answer: no — they are two disconnected identity systems today.**

`[system]` `apply-design-direction`'s Path B records a Claude Design link as
`[system:design-project-ref]` with fields `provider: claude-design`,
`project_ref: claude-design:<project-identifier>` — but this lives only in a
Work Object's Evidence Ledger.

`[system]` `references/DESIGN-ASSET-REGISTRY.md`'s Required Fields for a
canonical asset record (`Work Object`, `Pipeline`, `Status`, `Asset ID`,
`Asset kind`, `Source of truth`, `Projection status`) have no field for an
external provider reference. `Source of truth` is free plain text, not a
structured pointer.

`[inference]` Consequence: an asset actively being designed in Claude Design
can exist with a real, real project reference on some Work Object, while
`.work-studio/design-assets/*.asset.md` — the file `design-manage-assets` and
`asset-workbench.html` both treat as the canonical index of what assets
exist — has no way to say "this asset's current work lives in Claude Design
project X." The two truths can silently diverge.

## Sub-question 3 — What would the mechanical Claude Design workflow require if a skill owned it?

`[system]` `DesignSync`'s own tool description specifies a required order:
list/read → `finalize_plan` → write/delete, with `finalize_plan` as a
mandatory human-visible review checkpoint before any write. No skill in this
repo currently documents that six-step sequence as its stage workflow — the
closest, `apply-design-direction` Path B, references invoking "Claude Design
tools" abstractly via the `claude_design` capability without walking through
the actual method sequence a session must follow, the same abstraction level
`references/CAPABILITY-DEGRADATION.md:74` uses ("Access Claude Design MCP
tools for design generation and editing").

## Recommendations

### 1. Extend the asset registry schema with an external-reference field — not a new skill

**Confidence: high.** This is squarely inside `design-manage-assets`'
existing governing principle ("know... where its truth lives... provenance")
— it does not need a new frontier or a new skill, only a schema addition,
the same shape of change as the `motion` asset-kind addition made earlier
this session (WO `2026-08-22-032`).

- Add an optional field to `references/DESIGN-ASSET-REGISTRY.md`'s Required
  Fields (or a new optional field class) — e.g. `External reference:
  claude-design:<project-id>` — so an asset record can point at the Claude
  Design project holding its current working state.
- `design-manage-assets`'s classification stage reports this reference when
  present, and flags a `[gap]` when a Work Object has a
  `[system:design-project-ref]` entry but the corresponding asset record has
  no matching `External reference` — this is exactly the divergence
  Sub-question 2 found possible.
- `asset-workbench.html`'s per-asset card (already extended this session to
  show real Lifecycle owners) gains one more `dt`/`dd` row when the field is
  present, consistent with its existing labeled-metadata pattern.

### 2. A new skill: own the mechanical Claude Design sync sequence — portable-first, Claude Design always optional

**Confidence: high.** This is a genuine new frontier — no skill currently
documents or owns DesignSync's actual method sequence
(list → finalize_plan → write/delete → optional register), and the gap is
named five separate times across the pipeline (Sub-question 1) without an
owner.

**Director-confirmed constraint (not this report's inference):** the studio's
canonical asset truth must stay the local, file-backed
`.work-studio/design-assets/*.asset.md` record — readable and actionable by
every platform adapter (`claude-code`, `codex`, `github-copilot`) with zero
dependency on a live Claude Design connection. Claude Design is always an
*optional export/import destination* for an asset, never where its identity
or lifecycle lives. This mirrors the posture `apply-design-direction` already
uses for Path A vs. Path B — Path A (code-first) is the agent-agnostic
default; Path B (Claude Design) only runs when `claude_design` is actually
available and explicitly degrades, never silently depends on it.

- Proposed shape: a skill (e.g. `design-sync-claude-design`) that
  `apply-design-direction`'s Path B routes to for the actual mechanical
  execution, rather than Path B trying to inline it. It would own:
  running the auth probe (and reporting plainly when unavailable — e.g. in
  a Codex session with no Claude Design MCP wired up, this skill must
  degrade the same way Path B already does, never fail silently or block
  the portable workflow), listing/reading current project state, presenting
  the write/delete plan for confirmation (mirroring `finalize_plan`'s own
  human-checkpoint design), executing the plan, and recording
  `[system:design-project-ref]` / `[system:design-approval]` evidence —
  the same evidence formats `apply-design-direction` already defines, so
  this is composition, not a competing authority.
- The local asset record (Recommendation 1's external-reference field) is
  read *from* to know what to sync, and the sync's result updates that same
  field — Claude Design never becomes a second, competing source of truth.
  If the Claude Design capability is absent for a session, the asset record
  and every other skill that reads it remain fully functional; only the
  sync action itself is unavailable.
- New frontier: `external-design-sync`, owned by this new skill, closing the
  gap Sub-question 1 found in `design-manage-assets`' routing table and the
  pipeline's Ownership map.
- Explicitly does not choose creative direction, approve a design, or decide
  what gets synced — that stays `apply-design-direction`'s and the
  director's call; this skill only executes an already-confirmed sync.

### 3. Wire the new frontier into `design-manage-assets`' routing table

**Confidence: high, and small.** Once recommendation 2 exists, `design-manage-assets`'s
own Routing and termination list (currently exactly 7 named owners) gets an
8th line: "External design-tool sync -> `design-sync-claude-design`" — closing
the exact structural gap Sub-question 1 identified in that skill's own
Consequence and authority rules section, which already *names* the action
without an owner.

## What I deliberately did not recommend

- **A skill that makes creative decisions inside Claude Design** — that
  authority already and correctly belongs to `apply-design-direction` and the
  director; a sync skill should execute, not decide.
- **Making the asset-registry external-reference field required** — most
  assets have no Claude Design presence; forcing the field would be false
  precision. Optional, present-when-applicable.
- **A separate Claude Design skill for `verify-design-implementation`'s
  optional visual comparison** — that skill already correctly treats it as
  optional and subordinate to browser evidence; no gap was found there.

## Provenance summary

- `[system]` facts: file/line references above, this session's confirmed
  `DesignSync` connection and method list, and the registry schema.
- `[inference]`: the "two disconnected identity systems" framing, and each
  recommendation's shape — none are accepted decisions.
- No sub-question required contacting people, production, or external
  sources beyond this session's own already-established tool capabilities.

## Gaps carried into this deliverable

- No real Claude Design project currently maps to any real asset record in
  this repo (both are hypothetical/undemonstrated) — recommendations rest on
  structural absence, the same honest limitation the design-pipeline report
  (WO `2026-08-22-027`) carried for its own recommendations.
