# Local-First Design Review Layer — Implementation Plan

Produced by Grilling Session 13 (2026-07-23). 14 decisions accepted.

Supersedes the Figma-centered design workflow from Grilling Session 12
(2026-07-22) for all design surface decisions. Retains Grilling Session 12's
governance patterns (authority gates, evidence recording, capability degradation)
and code-first principles where applicable.

## Purpose

Implementation plan for a local-first governed design review and iteration
layer that lives inside the Creative Coding Studio. The review layer wraps the
user's existing NL → agent → code → browser workflow with multi-viewport
preview, design branch management, screenshot capture and comparison,
NL command history, automatic governance, and lightweight specification
extraction.

This is NOT a visual design editor. The user does not drag components onto a
canvas. The user describes what they want in natural language, the agent
proposes an interpretation, the user confirms, the agent writes code, and the
browser renders the result. The review layer provides the governed environment
for reviewing, comparing, and recording that process.

## Relationship to Grilling Session 12

Grilling Session 12 produced 22 decisions (DEC-1 through DEC-22) and 5 ADRs
(0024–0028) for a Figma-centered design workflow. Key findings from this
session that change that direction:

1. **Figma was never used.** The entire Figma architecture was aspirational.
   No Figma file, MCP connection, or artifact exists. (OBS-3, OBS-7)
2. **The user's workflow is NL → code → browser, not visual editor → spec → code.**
   The code IS the design. The browser IS the design surface. (DEC-A2)
3. **The user wants a review and iteration layer, not a visual composition editor.**
   The gap is governance, comparison, and history — not visual creation. (DEC-A3)
4. **The design tool lives in the Creative Coding Studio** as one practice
   among several in a personal multi-practice creative platform. (DEC-A1)

### What survives from Grilling Session 12

- Code-first token ownership principle (ADR 0024 core)
- Browser as canonical visual evidence (ADR 0027 core concept)
- Convention-based host project discovery (DEC-2)
- Discovery performed once per pass (DEC-3)
- Separate audit and foundation skills (DEC-6)
- Three-tier authority model (DEC-20, adapted)
- Capability degradation pattern (DEC-16, adapted)

### What is superseded

- Figwright wrapping (DEC-9, ADR 0025)
- Always-new Figma output (DEC-10, ADR 0026)
- Browser evidence gates Figma rendering (DEC-12, ADR 0027 as written)
- Authored interface specifications (DEC-11, ADR 0028 as written)
- Authored user flows and interface architecture documents
- Component registry for Figma mapping (DEC-13)
- Figma manifest (DEC-14)
- Revision manifest routing through conductor (DEC-17 as written)
- Phase 2 tracer bullet targeting Figwright (DEC-22)

## Accepted Decisions

### DEC-A1: Design practice lives in Creative Coding Studio

The visual design playground is a practice within the Creative Coding Studio
(`~/Documents/Creative coding/`), not a Work Studio capability or a per-project
tool. The Creative Coding Studio is the user's personal multi-practice creative
platform.

- **Enforcement:** Design tool code lives in Creative Coding Studio repo.
- **Revisit:** The Creative Coding Studio proves too coupled to specific needs.

### DEC-A2: Workflow is NL → agent → code → browser

The design workflow is natural language → LLM agent → code → browser rendering.
Code precedes design. The browser IS the design surface. There is no visual
editor step between intent and implementation.

- **Enforcement:** No visual editor code; review layer reads from code and browser.
- **Revisit:** User discovers they need visual composition before code.

### DEC-A3: Product is a governed review and iteration layer

The Creative Coding Studio's design practice is a governed design review and
iteration layer on top of NL → code → browser. It is not a visual composition
editor, page builder, infinite canvas, or Figma replacement.

The review layer provides:
- Multi-viewport preview (mobile, tablet, desktop simultaneously)
- Application state cycling (default, loading, error, empty)
- Design branch snapshots and comparison
- NL command history with visual diffs
- Annotation on rendered output
- Automatic governance (Work Studio integration)
- Lightweight specification extraction

The review layer does NOT provide:
- Spatial canvas / infinite canvas
- Component drag-and-drop
- Property panel editing
- Layout manipulation
- Code generation from visual input

- **Enforcement:** Review layer consumes rendered output; never produces visual input.
- **Revisit:** User needs spatial composition for a class of work.

### DEC-A4: Review artifacts live locally in the studio

Review artifacts (screenshots, branch metadata, NL history, annotations,
comparisons, decisions, extracted specs) live in the Creative Coding Studio,
not in target projects. Target projects contain only code and git history.

- **Enforcement:** Review layer writes to its own storage, never to target project filesystem.
- **Revisit:** Collaboration with another developer on a target project.

### DEC-A5: Figma deferred entirely

Figma was never used. No Figma-related code, skills, or ADR implementations
are needed. Figma becomes a potential future adapter with no current investment.

- **Enforcement:** No Figma-dependent code paths.
- **Revisit:** Collaboration with a designer who uses Figma.

### DEC-A6: Human retains creative authority

The human retains creative authority. Agents are collaborators that propose
interpretations of NL direction and execute only after the user confirms
the interpretation matches their intent.

The creative authority loop:
1. User describes creative intent in natural language.
2. Agent interprets and proposes what it would change (preserve/revise).
3. User confirms: "yes, that's what I mean" or "no, what I mean is…"
4. Agent executes the confirmed interpretation.
5. User reviews the result in the browser.
6. Iterate.

- **Enforcement:** Agent always proposes before executing; confirmation required.
- **Revisit:** User wants to grant the agent more autonomy for routine changes.

### DEC-A7: Review layer iframes the target project's dev server

The review layer renders target projects by iframing their running dev server.
Zero build-time coupling to target projects. The studio provides review tooling
around the iframe — viewports, screenshots, comparison, annotations.

- **Enforcement:** Review layer never imports target project code; always consumes via HTTP.
- **Revisit:** Need to inspect component props or inject state not controllable via URL.

### DEC-A8: Design branches support alternatives via git branches

Design branches support exploring alternatives, not just linear history. The
user can direct the agent to try multiple approaches, compare rendered results
side by side, and pick one. Design branches map to git branches in the target
project.

Branch workflow:
1. User says "try it two ways."
2. Agent creates two git branches in the target project, implements each.
3. Studio renders both in side-by-side iframes.
4. User picks one; agent merges the chosen branch, deletes the other.
5. Studio records the decision and archives the comparison.

Branch states: `exploring` | `review` | `accepted` | `archived`

- **Enforcement:** Studio branch metadata references git branch names and SHAs.
- **Revisit:** Branch management overhead exceeds creative value.

### DEC-A9: IndexedDB + automatic filesystem sync

IndexedDB is the runtime store. The filesystem in the Creative Coding Studio
repo is the durable backup, version-controlled by git. Every IndexedDB write
triggers a debounced filesystem write. Two-way recovery: filesystem can rebuild
IndexedDB, IndexedDB can rebuild filesystem.

Storage structure:
```
design-history/
├── branches/
│   ├── branch-001.yaml
│   └── branch-002.yaml
├── screenshots/
│   ├── branch-001-mobile.png
│   ├── branch-001-desktop.png
│   └── ...
└── comparisons/
    └── comp-001.yaml
```

- **Enforcement:** Sync layer runs on every write; recovery tested in both directions.
- **Revisit:** Design history files become too large for git; sync lag causes data loss.

### DEC-A10: Governance by default, deterministic to creative workflow

Governance is always on but invisible. Creative actions map deterministically
to governance events. The user never manually creates Work Objects or records
evidence.

Mapping:
| Creative action | Governance event |
|---|---|
| Open target project for review | Work Object created (explore) |
| "Change the sidebar" | NL command recorded in evidence |
| Agent proposes interpretation | Proposal recorded |
| User confirms | Decision recorded (authority: user) |
| Agent writes code | Implementation evidence (git SHA) |
| User reviews in browser | Browser evidence captured |
| "Try it two ways" | Two design branches created |
| User compares side by side | Comparison recorded |
| "I pick this one" | Branch accepted, other archived |
| "Done with this screen" | Work Object → accepted |

Work Object lifecycle maps to creative stages:
- `explore` → opening a project, looking at what exists
- `decide` → "try it two ways" — exploring alternatives
- `build` → "make this change" — agent implementing confirmed direction
- `verify` → reviewing the rendered result in the browser
- `accepted` → "this is right" — design direction confirmed

- **Enforcement:** Review layer emits governance events automatically.
- **Revisit:** Automatic governance produces too much noise.

### DEC-A11: All structure emerges from conversation

No pre-code specification, flow modeling, or architecture definition. All
design structure emerges from the NL conversation between the user and the
agent. Specifications are extracted after the fact for documentation, not
authored before implementation.

- **Enforcement:** No skills require pre-authored specs as input to implementation.
- **Revisit:** Project complexity requires upfront structural planning.

### DEC-A12: All failure modes tested

Testing covers every identified failure mode. No failure mode is deprioritized.

Categories:
1. Iframe rendering (dev server availability, CORS, error handling)
2. Screenshot capture (dimensions, cross-origin, blank detection)
3. Git branch coordination (create, switch, compare, recover, concurrent ops)
4. IndexedDB ↔ filesystem sync (two-way recovery, schema migration, partial writes)
5. Viewport fidelity (CSS media queries, device simulation accuracy)
6. History growth (storage size tracking, purge capability, git LFS fallback)

- **Enforcement:** Tracer bullet exercises each category; test suite covers each.
- **Revisit:** A failure mode proves impossible to test reliably.

### DEC-A13: Automatic lightweight specification extraction

The review layer automatically extracts a lightweight specification from
conversation history. The spec is a readable summary of what was designed
and why — derived from governance events, not authored manually.

Example:
```yaml
screen: dashboard
route: /dashboard
last_updated: 2026-07-23
git_sha: abc123

components_discussed:
  - sidebar (collapsible, accepted from branch-001)
  - header (unchanged)
  - metric cards (3-column grid, confirmed)

decisions:
  - "Collapsible sidebar preferred over always-visible"
  - "Metric cards use 3-column grid on desktop, stack on mobile"

direction_history:
  - input: "Make the navigation feel less cluttered"
    confirmed: "Collapse secondary links into menu, increase spacing"
    sha: def456
```

- **Enforcement:** Spec regenerated after each accepted design change.
- **Revisit:** Extracted specs prove too noisy or drift from implementation.

### DEC-A14: Tracer bullet targets Creative Coding Studio's own app

First tracer bullet uses the Creative Coding Studio's own app (`apps/studio`)
as the target project. Tests the full chain: iframe rendering, screenshot
capture, git branch coordination, NL → propose → confirm → execute, branch
comparison, filesystem sync, and spec extraction.

- **Enforcement:** Tracer bullet Work Object tracks all success evidence.
- **Revisit:** Studio app proves too atypical to validate the review layer.

## Current-State Findings

### Observed

- **OBS-1:** Work Studio contains no frontend application — no React, no
  `package.json`, no build tooling. (`/Users/andrelawas/Documents/andrelawas-work-studio/`)
- **OBS-2:** 9 design skills exist as contract shells with no implementation
  logic. (`.work-studio/component-ledger.md` COMP-015 through COMP-023)
- **OBS-3:** No Figma integration exists — no MCP config, no file keys, no
  artifacts, no rendered output. (`tools/figwright-probe.py` only)
- **OBS-4:** Phase 2 tracer bullet (WO 2026-07-22-007) is in notice state —
  DEC-9 (Figwright wrapping) has never been tested.
- **OBS-5:** 6 of 9 design skills have no Figma dependency even in their contracts.
- **OBS-6:** The host project for the original tracer bullet (Creative Coding)
  is a Vite+TypeScript single-screen interactive simulation.
- **OBS-7:** Figma was never used — the entire Figma architecture was aspirational.

### Claimed (from Grilling Session 12, now partially superseded)

- **CLM-1:** Design skills are portable and execute in host repositories.
  (DEC-1 — retained in principle)
- **CLM-2:** Figwright wrapping is the highest-risk assumption. (DEC-22 — superseded;
  the review layer architecture is now the highest-risk assumption)
- **CLM-3:** Code-first tokens are canonical. (DEC-8 — retained)

### Inferred

- **INF-1:** The proposed review layer is the first application component in the
  Creative Coding Studio that integrates with Work Studio governance.
- **INF-2:** The 5 deferred skills and their contract tests represent recoverable
  investment if Figma integration is ever needed.
- **INF-3:** The 4 active skills need contract amendments to reflect the
  review layer architecture.
- **INF-4:** IndexedDB + filesystem sync in the Creative Coding Studio is
  sufficient for all review artifacts.

## ADR Disposition Plan

### Retain (amend)

```yaml
adr: "0024 — Code-First Token Ownership"
current_status: Accepted
recommended_action: Amend
new_status: Accepted (amended)
reason: >
  Core principle (code tokens are canonical) remains valid. Remove all
  references to Figma token sync, Figwright token_map, and code→Figma
  sync direction. Retain: code tokens discovered by build-design-foundation;
  agent uses discovered tokens when implementing; no second token system.
replacement_or_superseding_adr: None
implementation_effect: Simplify skill contracts to remove Figma token references
migration_dependency: None
```

```yaml
adr: "0027 — Browser Evidence Gates Figma Rendering"
current_status: Accepted
recommended_action: Amend
new_status: Accepted (amended)
reason: >
  Core concept (browser rendering is canonical visual evidence) remains valid
  and is strengthened — the browser is now the ONLY design surface, not a
  gate before Figma. Remove: Figma rendering gate, Figwright invocation
  precondition, render-to-figma references. Retain: browser as verification
  evidence, screenshot capture as evidence, capability degradation for
  browser automation.
replacement_or_superseding_adr: None
implementation_effect: >
  Reframe as "browser is canonical design evidence" rather than
  "browser gates Figma"
migration_dependency: None
```

```yaml
adr: "0028 — Design Artifacts in Host Project Repository"
current_status: Accepted
recommended_action: Amend
new_status: Accepted (amended)
reason: >
  The durable/ephemeral artifact split principle remains valid. Change:
  durable design artifacts now live in the Creative Coding Studio
  (design-history/), not in target project design/ directory. Target project
  design/ directory becomes an optional export destination. Remove: Figma
  manifest, component registry for Figma mapping, authored specifications.
  Add: review branch metadata, screenshot storage, extracted specifications,
  comparison records. Retain: YAML format, meaningful-consequence creation.
replacement_or_superseding_adr: None
implementation_effect: >
  Design artifacts move from target project to Creative Coding Studio.
  Target project contains only code and git history.
migration_dependency: None
```

### Defer

```yaml
adr: "0025 — Work Studio Wraps Figwright"
current_status: Accepted
recommended_action: Defer
new_status: Deferred
reason: >
  Figma was never used. Figwright wrapping was never tested. The review layer
  replaces the need for Figma as a design surface. The ADR's governance
  patterns (authority gates, evidence recording, capability degradation)
  survive in the review layer architecture. The wrapping decision itself
  is deferred until Figma collaboration is needed.
replacement_or_superseding_adr: None (defer, not supersede — may be reactivated)
implementation_effect: >
  render-to-figma, connect-design-to-code skills deferred. No Figwright
  MCP configuration needed.
migration_dependency: None
```

```yaml
adr: "0026 — Always-New Figma Output"
current_status: Accepted
recommended_action: Defer
new_status: Deferred
reason: >
  No Figma output exists or is planned. The always-new write policy concept
  is partially preserved in the review layer's branch model — each design
  alternative is a separate branch, not an overwrite. The Figma-specific
  naming convention and write policy tiers are deferred.
replacement_or_superseding_adr: None (defer, not supersede)
implementation_effect: No Figma write code needed
migration_dependency: None
```

### Not affected

ADRs 0001–0023 are unaffected by this plan. They govern Work Studio's core
architecture (personalization, protocols, lifecycle, evidence, grilling,
documentation contract, component ledger), which remains unchanged.

## Target Architecture

### Creative Coding Studio — Review Layer

```
apps/design-review/                  # New app in Creative Coding monorepo
├── src/
│   ├── shell/                       # Main application shell
│   │   ├── app.tsx                  # Root component
│   │   ├── project-selector.tsx     # Open target project by dev server URL
│   │   └── layout.tsx               # Split panels
│   │
│   ├── viewport/                    # Iframe preview management
│   │   ├── viewport-host.tsx        # Single iframe at a given width
│   │   ├── multi-viewport.tsx       # Side-by-side viewports (mobile/tablet/desktop)
│   │   ├── viewport-config.ts       # Device presets and custom sizes
│   │   └── url-navigator.tsx        # Route navigation within target project
│   │
│   ├── screenshots/                 # Capture and manage screenshots
│   │   ├── capture.ts               # Iframe screenshot capture
│   │   ├── compare.tsx              # Side-by-side screenshot comparison
│   │   └── diff.ts                  # Visual diff between screenshots
│   │
│   ├── branches/                    # Design branch management
│   │   ├── branch-manager.tsx       # Create, switch, compare, archive
│   │   ├── branch-store.ts          # Branch metadata model
│   │   ├── git-coordinator.ts       # Git operations on target project
│   │   └── comparison-view.tsx      # Side-by-side branch rendering
│   │
│   ├── history/                     # NL command and decision history
│   │   ├── command-log.tsx          # Timeline of NL commands and confirmations
│   │   ├── decision-record.ts       # Structured decision entries
│   │   └── spec-extractor.ts        # Lightweight spec extraction from history
│   │
│   ├── annotations/                 # Review annotations on rendered output
│   │   ├── annotation-overlay.tsx   # Draw/pin annotations on iframe
│   │   └── annotation-store.ts      # Annotation persistence
│   │
│   ├── governance/                  # Work Studio integration
│   │   ├── auto-work-object.ts      # Automatic WO creation from creative actions
│   │   ├── evidence-emitter.ts      # Map creative actions to evidence entries
│   │   └── authority-check.ts       # Creative authority confirmation loop
│   │
│   └── storage/                     # Persistence
│       ├── indexed-db.ts            # Runtime store
│       ├── filesystem-sync.ts       # Debounced sync to design-history/
│       ├── migrations.ts            # Schema versioning
│       └── recovery.ts              # Two-way recovery (IDB ↔ filesystem)
│
├── design-history/                  # Git-tracked durable storage
│   ├── branches/                    # Branch metadata YAML files
│   ├── screenshots/                 # Captured PNGs
│   ├── comparisons/                 # Comparison records
│   └── specs/                       # Extracted specifications
│
├── index.html
├── vite.config.ts
├── package.json
└── tsconfig.json
```

### Work Studio — Skill Changes

```
skills/core/
├── audit-product-interface/         # RETAIN — auto-discovers target project
│   └── SKILL.md                     # Amend: remove Figma references
├── build-design-foundation/         # RETAIN — auto-discovers tokens
│   └── SKILL.md                     # Amend: remove Figma sync references
├── apply-design-direction/          # RETAIN — core creative authority loop
│   └── SKILL.md                     # Amend: simplify to conversational propose/confirm
├── verify-design-code-parity/       # SIMPLIFY → verify-design-implementation
│   └── SKILL.md                     # Amend: remove Figma parity; browser-only verification
│
├── model-user-flow/                 # DEFER — structure emerges from conversation
├── define-interface-architecture/   # DEFER — structure emerges from conversation
├── define-interface-specification/  # DEFER — specs extracted, not authored
├── render-to-figma/                 # DEFER — no Figma
└── connect-design-to-code/          # DEFER — no Figma component mapping
```

## Final Skill Set

### Active skills (4)

```yaml
skill: audit-product-interface
purpose: "Auto-discover target project's framework, routes, components, and layout conventions when opened for review"
accepted_states: [explore]
required_inputs: ["Target project root path"]
required_outputs: ["[system:discovery] evidence entry"]
reads: ["Target project source files"]
writes: ["Evidence Ledger only"]
required_capabilities: [file_read, directory_list, content_search, structured_output]
authority: "Low — reads only"
forbidden_actions: ["Modify target project files"]
forbidden_claims: ["Claim discovery is complete when gaps exist"]
routes_to: "build-design-foundation, apply-design-direction"
```

```yaml
skill: build-design-foundation
purpose: "Auto-discover target project's design tokens (CSS properties, theme objects, token files) for agent use"
accepted_states: [explore]
required_inputs: ["Target project root path"]
required_outputs: ["[system:token-inventory] evidence entry"]
reads: ["Target project CSS, theme configs, token files"]
writes: ["Evidence Ledger only"]
required_capabilities: [file_read, directory_list, glob_search, content_search, structured_output]
authority: "Low — reads only"
forbidden_actions: ["Modify target project files", "Create or recommend new tokens"]
forbidden_claims: ["Claim token coverage is complete when gaps exist"]
routes_to: "apply-design-direction"
```

```yaml
skill: apply-design-direction
purpose: "Core creative authority loop — interpret NL direction, propose changes, execute after user confirmation"
accepted_states: [decide, build]
required_inputs: ["User NL direction", "Discovery and token inventory"]
required_outputs: ["Confirmed interpretation recorded as evidence", "Code changes in target project"]
reads: ["Target project code, discovery, tokens"]
writes: ["Target project code (after confirmation)", "Evidence Ledger"]
required_capabilities: [file_read, file_write, content_search, structured_output, user_confirmation]
authority: "Meaningful — writes code after confirmation"
forbidden_actions: ["Execute without user confirmation", "Modify code beyond confirmed scope"]
forbidden_claims: ["Claim the interpretation matches intent without confirmation"]
routes_to: "verify-design-implementation"
```

```yaml
skill: verify-design-implementation
purpose: "Verify that the agent's implementation matches what the user confirmed — browser rendering matches confirmed proposal"
accepted_states: [verify]
required_inputs: ["Confirmed proposal from apply-design-direction", "Running target project in browser"]
required_outputs: ["[system:verification] evidence entry with pass/fail per confirmed change"]
reads: ["Browser rendering, confirmed proposal, target project code"]
writes: ["Evidence Ledger only"]
required_capabilities: [file_read, browser_automation, structured_output]
optional_capabilities: [screenshot capture]
authority: "Low — reads and observes only"
forbidden_actions: ["Modify code", "Modify the confirmed proposal"]
forbidden_claims: ["Claim verification passed without checking each confirmed change"]
routes_to: "apply-design-direction (if corrections needed)"
```

### Deferred skills (5)

```yaml
- skill: model-user-flow
  reason_deferred: "All structure emerges from conversation (DEC-A11)"
  revisit_trigger: "Project complexity requires upfront flow planning"

- skill: define-interface-architecture
  reason_deferred: "All structure emerges from conversation (DEC-A11)"
  revisit_trigger: "Project complexity requires upfront architectural planning"

- skill: define-interface-specification
  reason_deferred: "Specs are extracted, not authored (DEC-A11, DEC-A13)"
  revisit_trigger: "User needs to communicate design intent before implementation"

- skill: render-to-figma
  reason_deferred: "Figma never used (DEC-A5)"
  revisit_trigger: "Collaboration with a designer who uses Figma"

- skill: connect-design-to-code
  reason_deferred: "No Figma component mapping needed (DEC-A5)"
  revisit_trigger: "External design tool integration requires component mapping"
```

## Responsibility Matrix

| Operation | Owner |
|---|---|
| Creative direction | Human |
| NL interpretation and proposal | Coding agent (apply-design-direction) |
| Confirmation of interpretation | Human |
| Code implementation | Coding agent |
| Target project discovery | audit-product-interface (automatic) |
| Token discovery | build-design-foundation (automatic) |
| Browser rendering | Target project dev server (iframe) |
| Multi-viewport preview | Review layer (viewport host) |
| Screenshot capture | Review layer (capture module) |
| Design branch creation | Review layer + git coordinator |
| Branch comparison | Review layer (comparison view) |
| Branch acceptance/archival | Human (via review layer) |
| NL command history | Review layer (automatic) |
| Decision recording | Review layer (automatic, DEC-A10) |
| Work Object lifecycle | Review layer (automatic, DEC-A10) |
| Evidence recording | Review layer (automatic, DEC-A10) |
| Spec extraction | Review layer (automatic, DEC-A13) |
| Annotation | Human (via review layer) |
| IndexedDB persistence | Review layer (storage module) |
| Filesystem sync | Review layer (automatic) |
| Git operations on target project | Review layer (git coordinator) |
| Implementation verification | verify-design-implementation |
| Schema migration | Review layer (migrations module) |

## Machine-Readable Contracts

### Design branch metadata

```yaml
schema: design-branch
version: 1

branch:
  id: string           # UUID
  name: string         # Human-readable name
  git_branch: string   # Git branch name in target project
  git_sha: string      # Current HEAD SHA
  target_project: string # Absolute path to target project
  dev_server_url: string # e.g., http://localhost:5173
  status: enum         # exploring | review | accepted | archived
  created_at: datetime
  updated_at: datetime
  created_from_direction: string # The NL command that spawned this branch
  parent_branch: string | null   # Branch ID this was forked from
  compared_against: string[]     # Branch IDs this was compared with
  accepted_over: string[]        # Branch IDs this was chosen over

screenshots:
  - viewport: string   # mobile | tablet | desktop | custom
    width: number
    path: string        # Relative path to PNG in design-history/screenshots/
    captured_at: datetime

annotations:
  - id: string
    text: string
    position: { x: number, y: number, viewport: string }
    created_at: datetime
```

### NL command history entry

```yaml
schema: nl-command
version: 1

entry:
  id: string
  branch_id: string
  timestamp: datetime
  direction: string        # What the user said
  proposal: string         # What the agent proposed
  confirmed: boolean       # Whether the user confirmed
  correction: string | null # What the user corrected (if not confirmed)
  git_sha_before: string
  git_sha_after: string | null # Null if not yet executed
  screenshots_before: string[] # Paths to pre-change screenshots
  screenshots_after: string[]  # Paths to post-change screenshots
```

### Comparison record

```yaml
schema: design-comparison
version: 1

comparison:
  id: string
  branch_ids: string[]     # The branches being compared
  created_at: datetime
  resolved_at: datetime | null
  chosen_branch: string | null
  reason: string | null    # Why this branch was chosen
  screenshots:             # Side-by-side captures
    - branch_id: string
      viewport: string
      path: string
```

### Extracted specification

```yaml
schema: extracted-spec
version: 1

screen:
  route: string
  purpose: string
  last_updated: datetime
  git_sha: string
  branch_id: string

components_discussed:
  - name: string
    status: string         # e.g., "accepted from branch-001"
    description: string

decisions:
  - summary: string
    branch_id: string
    timestamp: datetime

direction_history:
  - input: string          # User's NL direction
    confirmed: string      # Confirmed interpretation
    sha: string
    timestamp: datetime
```

### Governance event (Work Studio integration)

```yaml
schema: governance-event
version: 1

event:
  type: enum               # wo_created | direction_given | proposal_made |
                           # confirmed | implemented | verified |
                           # branch_created | branch_compared |
                           # branch_accepted | branch_archived | wo_accepted
  timestamp: datetime
  work_object_id: string
  branch_id: string | null
  data: object             # Type-specific payload
  auto_generated: true     # Always true — governance events are automatic
```

## NL Operation Contract

```
User describes creative intent in natural language
    → Agent reads discovery snapshot and token inventory
    → Agent interprets direction against current code state
    → Agent proposes: "I would [preserve X] and [change Y to Z]"
    → User confirms or corrects
    → Agent writes code to target project
    → Review layer captures:
        - NL command history entry
        - Git SHA before and after
        - Screenshots before and after
        - Governance event (confirmed + implemented)
    → User reviews rendered result in browser
    → If correct: continue or accept
    → If wrong: user gives correction, loop restarts
```

No formal operation set — the agent uses full coding capability, constrained
by user confirmation. The review layer records what happened, not what was
allowed.

## Local Persistence Design

### Runtime store: IndexedDB

- **Library:** Native IndexedDB API (or Dexie if ergonomics justify it)
- **Object stores:** branches, commands, comparisons, screenshots (blobs),
  annotations, specs, governance-events
- **Schema version:** Integer, incremented on structure changes
- **Transactions:** Each creative action is a single transaction

### Durable store: Filesystem (git-tracked)

- **Location:** `apps/design-review/design-history/`
- **Format:** YAML for metadata, PNG for screenshots
- **Sync:** Debounced write (500ms) after every IndexedDB transaction
- **Recovery:**
  - IndexedDB cleared → rebuild from filesystem YAML + PNGs
  - Filesystem deleted → rebuild from IndexedDB, write to filesystem
  - Both cleared → lost (user's responsibility to commit to git)

### Schema migration

- Migration files in `src/storage/migrations/`
- Each migration: version number, up function, down function
- Run on app startup if IndexedDB version < current schema version
- Filesystem files include schema version in YAML for compatibility checking

### Failure handling

- **Partial write:** Detect via checksums in YAML metadata
- **Quota exceeded:** Alert user; suggest purging archived branch screenshots
- **Private browsing:** Detect and warn; filesystem sync still works
- **Corrupted data:** Validate on read; fall back to filesystem copy

### Growth management

- Track total screenshot storage size
- Warn at configurable threshold (default: 500MB)
- Archived branches: screenshots purgeable, metadata retained
- Git LFS `.gitattributes` rule for `design-history/screenshots/*.png`
  if repo size exceeds comfortable threshold

## Testing Strategy

### Iframe rendering

```
├── Target dev server running → iframe loads and renders correctly
├── Target dev server not running → clear error message, not blank screen
├── Wrong port or URL → meaningful failure with suggested fix
├── CORS restrictions → documented workaround (proxy or dev server config)
├── Multiple iframes at different viewports → independent rendering
└── Route navigation within iframe → URL updates correctly
```

### Screenshot capture

```
├── Loaded iframe → capture produces correct-dimension PNG
├── Blank or errored iframe → capture reports failure, not silent blank
├── Cross-origin iframe → fallback documented and tested
├── Three viewport sizes → three distinct correct screenshots
└── PNG files are valid, openable, and correctly sized
```

### Git branch coordination

```
├── Create design branch → git branch exists in target project
├── Switch design branch → dev server serves correct branch code
├── Compare two branches → both render in parallel iframes
├── Delete archived branch → git branch cleaned up in target project
├── Target project has uncommitted changes → warning before branching
├── Studio metadata references deleted git branch → graceful recovery
├── Concurrent git operations outside studio → detect and recover
├── Branch accepted → merge into parent succeeds
├── Branch rejected → clean delete, no orphaned state
└── Multiple target projects → branches isolated per project
```

### IndexedDB ↔ filesystem sync

```
├── IndexedDB write → file appears in design-history/ within debounce window
├── Rapid successive writes → final state persisted (no dropped writes)
├── Browser crash mid-write → filesystem has last complete state
├── Filesystem deleted → IndexedDB rebuilds it on next sync cycle
├── IndexedDB cleared → filesystem rebuilds IndexedDB on app start
├── Schema migration → both stores updated consistently
├── Partial filesystem write → detected via checksum, re-synced
├── Large screenshot blobs → don't block metadata sync
└── Concurrent browser tabs → last-write-wins with conflict detection
```

### Viewport fidelity

```
├── 375px iframe → CSS media queries fire as mobile
├── 768px iframe → CSS media queries fire as tablet
├── 1280px iframe → CSS media queries fire as desktop
├── Responsive resize → iframe content reflows correctly
├── Viewport meta tag behavior inside iframe → documented
└── Touch vs pointer media queries → documented limitations
```

### History growth

```
├── Screenshot count and total size tracked per project
├── Warning emitted when design-history/ exceeds size threshold
├── Archived branch screenshots purgeable without losing metadata
├── Git LFS configuration generated when threshold exceeded
├── Branch archival reduces active IndexedDB storage
└── Old comparisons cleanly removable
```

### Governance integration

```
├── Opening target project → Work Object created automatically
├── NL command → evidence recorded automatically
├── Confirmation → decision recorded with user authority
├── Branch creation → branch event recorded
├── Branch comparison → comparison event recorded
├── Branch acceptance → decision event with rationale
├── "Done" → Work Object transitions to accepted
└── All events recoverable from filesystem after IndexedDB clear
```

### Specification extraction

```
├── After accepted change → spec YAML regenerated
├── Spec includes all confirmed directions and decisions
├── Spec references correct git SHAs
├── Spec is valid YAML and machine-parseable
├── Empty history → no spec generated (not empty spec)
└── Multiple screens → separate spec files per route
```

## Migration Plan

### Phase 0: ADR Amendments (reversible)

- **Objective:** Update ADRs 0024, 0027, 0028 to reflect review layer
  architecture. Defer ADRs 0025, 0026.
- **Affected skills:** None (ADR text only)
- **Affected ADRs:** 0024 (amend), 0025 (defer), 0026 (defer), 0027 (amend),
  0028 (amend)
- **Code changes:** ADR markdown files only
- **Tests:** None
- **Acceptance criteria:** ADRs accurately describe the review layer decisions
- **Rollback:** Revert ADR file changes
- **Authority:** User approval of ADR content

### Phase 1: Skill Contract Amendments (reversible)

- **Objective:** Amend 4 active skill contracts. Mark 5 deferred skills.
  Rename `verify-design-code-parity` to `verify-design-implementation`.
- **Affected skills:** All 9 design skills
- **Affected ADRs:** None
- **Code changes:** SKILL.md files, contract tests, platform adapter regeneration
- **Tests:** Contract tests pass for amended skills
- **Acceptance criteria:** Active skill contracts reflect review layer architecture;
  deferred skills clearly marked
- **Rollback:** Revert SKILL.md changes; regenerate adapters
- **Authority:** User approval of skill contract changes

### Phase 2: Review Layer Scaffold (reversible)

- **Objective:** Create the `apps/design-review/` application shell in the
  Creative Coding Studio with Vite + React + TypeScript. Establish the project
  structure, build tooling, and empty module stubs.
- **Affected skills:** None
- **Affected ADRs:** None
- **Code changes:** New app in Creative Coding Studio monorepo
- **Tests:** App builds and runs (empty shell)
- **Acceptance criteria:** `pnpm dev` starts the review layer; empty shell renders
- **Rollback:** Delete `apps/design-review/`
- **Authority:** User approval to create new app in Creative Coding Studio

### Phase 3: Tracer Bullet (the critical test)

- **Objective:** End-to-end test of the highest-risk assumptions using the
  Creative Coding Studio's own `apps/studio` as the target project.
- **Affected skills:** audit-product-interface, apply-design-direction (minimal
  implementation for tracer bullet)
- **Code changes:** Review layer modules: viewport host, screenshot capture,
  git coordinator, IndexedDB store, filesystem sync, governance event emitter
- **Tests:** All 7 test categories exercised
- **Acceptance criteria:**
  1. `apps/studio` dev server opens in iframe at 3 viewports
  2. Screenshots captured at each viewport
  3. One NL direction given → agent proposes → user confirms → code changes
  4. Git branch created in Creative Coding Studio repo for the change
  5. Second NL direction → second git branch → side-by-side comparison
  6. User picks one → accepted, other archived → decision recorded
  7. Lightweight spec extracted from command history
  8. IndexedDB cleared → recovers from filesystem
  9. Filesystem deleted → recovers from IndexedDB
  10. Screenshot storage size tracked and reported
  11. Work Object created and transitioned automatically
- **Rollback:** Delete review layer modules; revert git branches in target project
- **Authority:** User approval to implement review layer modules
- **Intentionally deferred:** Annotations, advanced diffing, state cycling,
  multiple target projects, NL operation constraints

### Phase 4: Full Implementation (after tracer bullet validates)

- **Objective:** Complete all review layer modules based on tracer bullet findings.
- **Modules:** Annotations, visual diff, state cycling, route navigation,
  multi-project support, spec export to target project, history purge,
  Git LFS configuration
- **Tests:** Full test suite
- **Acceptance criteria:** All test categories pass; review layer is daily-usable
- **Rollback:** Revert to tracer bullet baseline
- **Authority:** User approval per module
- **Deferred:** Figma adapter, cloud sync, collaboration, Excalidraw

## First Tracer Bullet

### Target

Creative Coding Studio's own app: `apps/studio` (Vite + TypeScript,
"The Water Refuses the Map" interactive audiovisual simulation).

### Highest-risk assumptions being tested

1. **Can the review layer reliably iframe another app in the same monorepo?**
   (DEC-A7 — iframe architecture)
2. **Can screenshots be captured from a cross-origin or same-origin iframe?**
   (Screenshot module feasibility)
3. **Can git branches in the same repo be coordinated without breaking the
   review layer's own running dev server?** (Git coordinator — the review
   layer and target app are in the same monorepo, so branch switching
   affects both)
4. **Does IndexedDB ↔ filesystem two-way sync actually recover?**
   (DEC-A9 — persistence reliability)
5. **Can governance events be emitted automatically without blocking the
   creative flow?** (DEC-A10 — invisible governance)

### Critical risk: same-repo branching

Because the target app (`apps/studio`) and the review layer
(`apps/design-review`) are in the same monorepo, a git branch switch
affects both apps. This means either:

- **git worktrees** — the target app runs from a worktree while the review
  layer runs from the main working tree. Isolates branch switching.
- **The target app is a separate repo** — contradicts using the studio's own
  app for the tracer bullet.
- **Branch switching is fast enough** — the dev server hot-reloads on branch
  switch. Review layer survives because its code doesn't change across
  design branches (design branches only modify target app code).

The tracer bullet must validate which approach works before Phase 4.

### Sequence

```
1. Start review layer dev server (apps/design-review)
2. Start target app dev server (apps/studio)
3. Review layer opens target app in iframe at 375px, 768px, 1280px
4. Capture screenshots at all three viewports → verify PNGs valid
5. Governance: Work Object auto-created → verify in evidence
6. User gives NL direction: "Change the background color to deep navy"
7. Agent proposes interpretation → user confirms
8. Agent writes code change to apps/studio
9. Git branch 'design/navy-background' created
10. Iframe refreshes → screenshots captured → before/after diff available
11. User gives second direction: "Try dark charcoal instead"
12. Git branch 'design/charcoal-background' created from same parent
13. Both branches rendered in side-by-side iframes
14. User picks navy → branch accepted, charcoal archived
15. Decision recorded with rationale
16. Lightweight spec extracted → YAML file in design-history/specs/
17. Clear IndexedDB → app recovers from design-history/ filesystem
18. Delete design-history/ → app recovers from IndexedDB
19. Check screenshot storage size → reported correctly
20. Work Object auto-transitioned to accepted
```

### Success criteria

All 20 steps complete without manual intervention (except user confirmations
in steps 7 and 14). Any failure identifies which architectural assumption
is wrong and what needs revision.

## Deferred Capabilities

```yaml
- capability: Figma integration
  reason_deferred: "Never used; no current need (DEC-A5)"
  dependencies: [Figma account, Figwright MCP, component mapping]
  evidence_needed: "Collaboration with a designer who uses Figma"
  revisit_trigger: "External stakeholder requires Figma review"

- capability: Figwright wrapping
  reason_deferred: "No Figma integration (DEC-A5)"
  dependencies: [Figma integration]
  evidence_needed: "Figma integration is activated"
  revisit_trigger: "Figma integration revisit trigger fires"

- capability: Excalidraw sketching layer
  reason_deferred: "Review layer, not creation tool (DEC-A3)"
  dependencies: [Excalidraw library, integration architecture]
  evidence_needed: "User needs freeform sketching before or alongside code"
  revisit_trigger: "NL → code workflow insufficient for spatial ideation"

- capability: Advanced infinite canvas
  reason_deferred: "Review layer, not spatial editor (DEC-A3)"
  dependencies: [React Flow or equivalent, canvas architecture]
  evidence_needed: "User needs to compare many screens spatially"
  revisit_trigger: "Side-by-side comparison insufficient for complex projects"

- capability: Backend / cloud database
  reason_deferred: "Solo developer, local-first (DEC-A4, DEC-A9)"
  dependencies: [Database, API, authentication]
  evidence_needed: "Cross-device access or data loss from local storage"
  revisit_trigger: "Repeated need to access design history from another machine"

- capability: Cloud sync
  reason_deferred: "Solo developer (DEC-A4)"
  dependencies: [Backend]
  evidence_needed: "Cross-device access"
  revisit_trigger: "Backend revisit trigger fires"

- capability: Collaboration / multiplayer
  reason_deferred: "Solo developer (DEC-A4)"
  dependencies: [Backend, authentication, conflict resolution]
  evidence_needed: "Working with another person on the same design"
  revisit_trigger: "Repeated collaboration need"

- capability: Code generation from visual input
  reason_deferred: "Workflow is NL → code, not visual → code (DEC-A2)"
  dependencies: [Visual editor, code generation engine]
  evidence_needed: "User needs visual composition before code"
  revisit_trigger: "DEC-A2 revisit trigger fires"

- capability: Authored interface specifications
  reason_deferred: "Structure emerges from conversation (DEC-A11)"
  dependencies: [Specification schema, authoring UI]
  evidence_needed: "Project complexity requires upfront planning"
  revisit_trigger: "DEC-A11 revisit trigger fires"

- capability: User flow modeling
  reason_deferred: "Structure emerges from conversation (DEC-A11)"
  dependencies: [Flow schema, flow visualization]
  evidence_needed: "Complex multi-screen flows need explicit modeling"
  revisit_trigger: "DEC-A11 revisit trigger fires"

- capability: Interface architecture definition
  reason_deferred: "Structure emerges from conversation (DEC-A11)"
  dependencies: [Architecture schema]
  evidence_needed: "Screen hierarchy needs explicit planning"
  revisit_trigger: "DEC-A11 revisit trigger fires"

- capability: Remote assets
  reason_deferred: "Local-first (DEC-A4)"
  dependencies: [Asset storage, CDN]
  evidence_needed: "Design assets need sharing or hosting"
  revisit_trigger: "Asset management becomes a bottleneck"
```

## New ADR Candidates

### ADR 0029: Local-First Design Review Layer Replaces Figma-First Workflow

- **Decision:** The design surface is the browser rendering of code produced by
  an NL → agent → code workflow. The Creative Coding Studio provides a governed
  review and iteration layer, not a visual design editor. Figma is deferred.
- **Context:** Grilling Session 13 found that Figma was never used, the user's
  workflow is NL → code → browser, and the gap is review/governance, not creation.
- **Alternatives:** Visual composition editor (rejected — fights natural workflow);
  Figma adoption (rejected — cost, vendor dependency); no review layer (rejected —
  loses governance, history, and comparison).
- **Consequences:** 5 design skills deferred; 3 ADRs deferred/amended; review
  layer is new application code in Creative Coding Studio.
- **Enforcement:** No visual editor code; review layer consumes rendered output.
- **Validation:** Tracer bullet (Phase 3).
- **Migration:** 4-phase plan with rollback at each phase.
- **Revisit trigger:** User needs visual composition before code.

### ADR 0030: Design Branches Map to Git Branches

- **Decision:** Design alternatives are explored via git branches in the target
  project. The review layer tracks branch metadata and comparison results.
  Design branches are not a separate state system.
- **Context:** The user explores alternatives by directing the agent to try
  multiple approaches. Each approach is code in a git branch.
- **Alternatives:** Review-layer-only branches with snapshots (rejected — can't
  render live alternatives); specification-level branches (rejected — no
  authored specs).
- **Consequences:** Git coordinator needed in review layer; same-repo branching
  requires worktree investigation.
- **Enforcement:** Branch metadata references git branch name and SHA.
- **Validation:** Tracer bullet step 9–14.
- **Revisit trigger:** Branch management overhead exceeds creative value.

### ADR 0031: Automatic Governance for Creative Workflows

- **Decision:** Creative actions in the review layer automatically produce
  Work Studio governance events. No manual Work Object creation or evidence
  recording. The creative workflow IS the governance workflow.
- **Context:** The user wants governance by default without creative friction.
- **Alternatives:** Manual governance (rejected — friction); no governance
  (rejected — loses history and authority tracking); opt-in governance
  (rejected — user wants default-on).
- **Consequences:** Review layer must emit structured governance events;
  Work Object lifecycle maps to creative stages.
- **Enforcement:** Every creative action has a deterministic governance mapping.
- **Validation:** Tracer bullet steps 5, 15, 20.
- **Revisit trigger:** Automatic governance produces too much noise.

## Implementation Readiness

**Status: Ready for Phase 0 (ADR amendments).**

Blockers for subsequent phases:
- **Phase 1** (skill amendments): No blockers after Phase 0.
- **Phase 2** (review layer scaffold): Requires confirming Creative Coding Studio
  monorepo can accept a new `apps/design-review/` app with its existing pnpm
  workspace configuration.
- **Phase 3** (tracer bullet): Requires Phase 2 complete; requires resolving
  the same-repo branching risk (git worktrees vs. branch isolation).
- **Phase 4** (full implementation): Requires Phase 3 success.

## Authorization Question

Which approved migration phase should I convert into a bounded Work Object,
ADR update set, and implementation task?
