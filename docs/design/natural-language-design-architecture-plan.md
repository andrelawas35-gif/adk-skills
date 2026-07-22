# Natural-Language Design Architecture — Implementation Plan

Produced by Grilling Session 12 (2026-07-22). 22 decisions accepted.

## Purpose

Implementation plan for a portable natural-language design skill set that
executes in host repositories, translating creative direction into structured
interface specifications, implementing through code, rendering into Figma
through governed Figwright MCP invocation, and verifying design-code parity.

## Accepted Decisions

### DEC-1: Portable design skills

Design skills execute in host repositories, not inside Work Studio. Work Studio
contains no application; design skills discover and operate on the pinning
project's code, routes, tokens, and Figma.

- **Enforcement:** Skills use host-project discovery, not hardcoded paths.
- **Revisit:** Work Studio itself gains a deployable UI.

### DEC-2: Convention-based discovery

Design skills discover host-project architecture by inspecting the codebase
(framework configs, directory conventions, file patterns), not from a
host-declared manifest. Zero onboarding cost.

- **Enforcement:** `audit-product-interface` skill contract.
- **Revisit:** Discovery proves unreliable across multiple host projects.

### DEC-3: Discovery performed once per pass

Architecture discovery runs once per design pass and is shared forward through
the Work Object. Downstream skills read the result rather than re-scanning.

- **Enforcement:** Downstream skill preconditions check for discovery entry.
- **Revisit:** Stale discovery within a long session causes downstream failures.

### DEC-4: Discovery stored in Evidence Ledger

The discovery snapshot is a `[system:discovery]` Evidence Ledger entry — an
ephemeral per-pass observation, not a durable artifact.

- **Enforcement:** `audit-product-interface` output contract.
- **Revisit:** Snapshots become too large for evidence ledger format.

### DEC-5: Design-domain skills only

Keep skills that represent genuinely new design-domain responsibilities. Do not
duplicate existing lifecycle skills (`implement-bounded-change`,
`verify-release-evidence`, `design-tracer-bullet`).

- **Enforcement:** Design skills own design-domain knowledge; lifecycle skills
  own execution mechanics.
- **Revisit:** Lifecycle skills prove unable to handle design work.

### DEC-6: Separate audit and foundation skills

`audit-product-interface` (structural discovery) and `build-design-foundation`
(token discovery) remain separate. Different expertise domains; token audit may
run independently.

- **Enforcement:** Audit owns routes/components; foundation owns tokens.
- **Revisit:** The two skills always run together and never independently.

### DEC-7: Conductor routes individually

The conductor routes to each design skill directly. No design-stage coordinator
layer. Same pattern as all existing skills.

- **Enforcement:** Conductor routing logic.
- **Revisit:** Routing logic becomes unwieldy.

### DEC-8: Code-first token ownership

Host-project code tokens are canonical. Figma tokens are generated
representations. Figma-side token edits are proposals requiring accept-back
into code. Sync direction: code → Figma.

- **Enforcement:** `build-design-foundation` reads code tokens; `render-to-figma`
  maps code → Figma; `verify-design-code-parity` flags divergence.
- **Revisit:** Figma-first token workflows prove common.

### DEC-9: Wrap and govern Figwright

Work Studio design skills wrap Figwright's skills (`figma-build`,
`figma-codegen`). Figwright provides execution (tech-stack detection, component
reuse, canvas operations). Work Studio provides authority gates, evidence
recording, preservation policy, capability degradation, and lifecycle.

- **Enforcement:** Design skill contracts require authority before and evidence
  after Figwright invocation.
- **Revisit:** Figwright gains its own governance, or skill interface changes.

### DEC-10: Always-new Figma output

`render-to-figma` always creates a new page/section (named WO ID + spec +
pass). Governed update of non-approved frames requires: node ID in Evidence
Ledger + frame not approved + explicit user direction. Approved frame update
requires explicit named confirmation (high consequence). Deletion is never
performed by any skill.

- **Enforcement:** `render-to-figma` and `apply-design-direction` contracts.
- **Revisit:** Stale page accumulation becomes a significant problem.

### DEC-11: Specifications in host project

Interface specifications are YAML files in the host project
(`design/specs/<slug>.yaml`), referenced by path from the Work Object. Durable,
version-controlled, code-reviewable.

- **Enforcement:** `define-interface-specification` output contract.
- **Revisit:** Host projects demonstrate conflicting conventions.

### DEC-12: Browser evidence gates Figma rendering

`render-to-figma` requires a `[system:browser-evidence]` Evidence Ledger entry
before invoking Figwright. Prevents Figma output from representing unverified
intent. Pauses with manual instruction when browser automation unavailable.

- **Enforcement:** `render-to-figma` precondition check.
- **Revisit:** Browser evidence consistently impractical.

### DEC-13: Durable component registry

Component registry (`design/components/registry.yaml`) is a durable file
mapping code components ↔ Figma components. Not regenerated each pass.
Created/updated by `connect-design-to-code` with authority.

- **Enforcement:** `connect-design-to-code` governs Figwright's `component_map`.
- **Revisit:** Mappings prove too volatile.

### DEC-14: Durable Figma manifest

Host project maintains `design/manifests/figma.yaml` tracking file keys, pages,
approved frames, and parity status across Work Objects.

- **Enforcement:** `render-to-figma` reads/updates; `verify-design-code-parity`
  reads approved frames.
- **Revisit:** Multiple Figma files per project exceed schema.

### DEC-15: Artifact location split

Durable files in host project: user flows (`design/flows/`), interface
architecture (`design/architecture/`). Ephemeral Evidence Ledger entries: token
inventory (`[system:token-inventory]`), parity reports
(`[system:parity-report]`).

- **Enforcement:** Owning skill output contracts.
- **Revisit:** Token inventory too large; parity reports need cross-session query.

### DEC-16: Capability degradation — Figwright

When Figwright unavailable, code-side workflow completes fully. Figma-dependent
steps deferred with `[system:capability-gap]` entries. `verify-design-code-parity`
runs two-way (spec ↔ browser), explicitly states Figma parity not checked.

- **Enforcement:** Figma-dependent skills check availability before invocation.
- **Revisit:** Deferred Figma steps are rarely resumed.

### DEC-17: Direction produces plans, not execution

`apply-design-direction` translates NL feedback into a structured revision
manifest (preserve/revise/prohibited per target). Conductor routes each target
to its owning skill. The skill does not directly modify code, tokens, or Figma.

- **Enforcement:** `apply-design-direction` contract.
- **Revisit:** Routing overhead makes simple revisions impractically slow.

### DEC-18: Structural and visual parity focus

`verify-design-code-parity` checks structural (layout, component, responsive)
and visual (typography, spacing, colors, dimensions). Behavioral, full-stack,
and accessibility dimensions explicitly deferred with honest status reporting.

- **Enforcement:** Parity report schema with per-dimension `checked|deferred`.
- **Revisit:** Automated behavioral/accessibility tooling becomes available.

### DEC-19: No new lifecycle states

Existing 8-state model accommodates all design skills. Conductor distinguishes
design work by artifact presence in Evidence Ledger, not by state name.

- **Enforcement:** Conductor routing table — artifact presence determines routing.
- **Revisit:** Artifact-presence routing becomes too complex.

### DEC-20: Three-tier authority for design actions

Low: reads and observations. Meaningful: new artifact creation, new Figma pages,
registry/manifest updates. High: approved frame modification, shared token
changes, artifact deletion.

- **Enforcement:** Each skill checks consequence level.
- **Revisit:** Artifact creation too frequent for meaningful-consequence ceremony.

### DEC-21: Phased test strategy

Contract tests ship with design skills from day one. Fixture host project and
integration tests ship after the tracer bullet validates the workflow.

- **Enforcement:** Contract tests verify inputs/outputs, forbidden actions,
  routing, authority, degradation.
- **Revisit:** Contract tests insufficient to catch real governance failures.

### DEC-22: Tracer bullet targets Figwright wrapping

First tracer bullet tests DEC-9 against an existing screen in a real host
project. Exercises the full artifact chain including capability degradation.

- **Enforcement:** Tracer bullet Work Object.
- **Revisit:** Results determine whether DEC-9 holds.

## Design Skill Set (9 skills)

| Skill | Purpose | Stage | Authority |
|---|---|---|---|
| audit-product-interface | Structural discovery (routes, components, layouts) | explore | low |
| build-design-foundation | Token discovery/audit (typography, spacing, themes) | explore | low |
| model-user-flow | Map user goals → actions → states → responses | explore/decide | meaningful |
| define-interface-architecture | Screen hierarchy, navigation, info architecture | decide | meaningful |
| define-interface-specification | Machine-readable spec connecting NL, code, Figma | design | meaningful |
| render-to-figma | Governed Figwright wrapper — creates Figma from verified code | build | meaningful |
| connect-design-to-code | Component/token mapping governance via Figwright | build | meaningful |
| apply-design-direction | NL revision → structured plan (does not execute) | design/build | low |
| verify-design-code-parity | Structural/visual parity across spec/browser/Figma | verify | low |

### Collapsed into existing skills

| Proposed | Disposition | Reason |
|---|---|---|
| implement-designed-interface | retire | Use `implement-bounded-change` |
| build-ui-branch | retire | Use `implement-bounded-change` |
| verify-design-implementation | retire | Collapses into `verify-design-code-parity` |
| design-from-codebase | retire | Collapses into `audit-product-interface` |
| model-user-flow-and-interface | retire | `model-user-flow` + `define-interface-architecture` |
| design-screen-in-figma | retire | Collapses into `render-to-figma` |

## Design Artifact Map

| Artifact | Location | Lifecycle | Owner |
|---|---|---|---|
| Discovery snapshot | Evidence Ledger `[system:discovery]` | Ephemeral | audit-product-interface |
| User flows | `design/flows/<slug>.yaml` | Durable | model-user-flow |
| Interface architecture | `design/architecture/<slug>.yaml` | Durable | define-interface-architecture |
| Interface specification | `design/specs/<slug>.yaml` | Durable | define-interface-specification |
| Token inventory | Evidence Ledger `[system:token-inventory]` | Ephemeral | build-design-foundation |
| Component registry | `design/components/registry.yaml` | Durable | connect-design-to-code |
| Figma manifest | `design/manifests/figma.yaml` | Durable | render-to-figma |
| Browser evidence | Evidence Ledger `[system:browser-evidence]` | Ephemeral | implementation step |
| Parity report | Evidence Ledger `[system:parity-report]` | Ephemeral | verify-design-code-parity |
| Revision manifest | Evidence Ledger | Ephemeral | apply-design-direction |

## Host Project Directory Structure

```
design/
├── specs/                   # interface specifications (YAML)
│   └── <screen-slug>.yaml
├── flows/                   # user flow definitions (YAML)
│   └── <flow-slug>.yaml
├── architecture/            # interface architecture (YAML)
│   └── <slug>.yaml
├── components/
│   └── registry.yaml        # code ↔ Figma component mappings
└── manifests/
    └── figma.yaml           # file keys, pages, approved frames
```

## Figwright MCP Contract

### Boundary

Figwright owns execution: tech-stack detection, component/token/icon mapping,
canvas read/write, design diff, `figma-build` and `figma-codegen` skills.

Work Studio owns governance: authority gates, evidence recording, preservation
policy, capability degradation, lifecycle integration.

### Write policy

- Default: always-new page/section
- Update: non-approved frames only, with node ID evidence + explicit direction
- Approved frame update: high-consequence explicit named confirmation
- Deletion: prohibited

### Capability degradation

When Figwright unavailable: code-side workflow completes; Figma steps deferred;
`[system:capability-gap]` recorded; parity drops to two-way.

### Undocumented capabilities (verify in tracer bullet)

Branch creation, node deletion behavior, node ID return after writes, content
preservation, section creation.

## Natural-Language Direction Contract

```
User NL direction
  → apply-design-direction reads spec + discovery + registry + tokens
  → Produces revision manifest: preserve / revise / prohibited
  → User accepts manifest
  → Conductor routes each target to owning skill
```

Vague language is rejected or translated into observable contracts. "Make it
feel more focused" becomes concrete specification changes with preserved
behavior explicitly named.

## Migration Plan

### Phase 0: Architecture Records

- **Objective:** Record key decisions as ADRs
- **Artifacts:** `docs/adr/0024-0028` — token ownership, Figwright wrapping,
  Figma write policy, browser evidence gate, design artifacts in host project
- **Changes:** ADR files only — no code, no Figma
- **Rollback:** Delete ADR files
- **Authority:** User approval of ADR content

### Phase 1: Contract Infrastructure

- **Objective:** Create 9 design skill shells with contracts; Figwright probe;
  contract tests
- **Artifacts:** `skills/core/<9 dirs>/SKILL.md`; `tools/figwright-probe.py`;
  `tests/test_<9 skills>.py`
- **Changes:** Skill contracts, test files, probe utility. No host-project
  interaction, no Figwright dependency
- **Rollback:** Delete new directories and files
- **Authority:** User approval to create skill files

### Phase 2: Tracer Bullet (DEC-22)

- **Objective:** Test DEC-9 end-to-end against a real host project screen
- **Artifacts:** Host project `design/` directory; Work Object with full chain
- **Changes:** Minimal implementation in 4 exercised skills; first Figma page
- **Rollback:** Delete `design/` in host project; Figma page is always-new
- **Authority:** User approval to write to host project and Figma

### Phase 3: Full Implementation

- **Objective:** Implement remaining 5 skills; extend conductor routing; create
  fixture host project for integration tests
- **Changes:** Skill logic, conductor routing, fixture project
- **Rollback:** Revert to contract shells; delete fixture
- **Authority:** Conductor modification is high consequence

## First Tracer Bullet

Tests DEC-9 (Figwright wrapping) as highest-risk assumption.

1. Select one existing screen from a real host project
2. `audit-product-interface` → `[system:discovery]`
3. `define-interface-specification` → `design/specs/<screen>.yaml`
4. Skip implementation (screen already exists)
5. Browser evidence → `[system:browser-evidence]`
6. `render-to-figma` → invoke Figwright `figma-build` governed → capture node IDs
7. `verify-design-code-parity` → `[system:parity-report]`
8. Capability degradation test → disconnect Figwright → verify deferral

### Success: Figwright accepts structured spec, returns node IDs, authority gate fires.
### Failure: DEC-9 must be revised before building skills on the assumption.

## Additional Components

### Justified

- **Figwright capability probe** — utility (not a skill) that checks MCP
  connectivity, enumerates tools, classifies capabilities. Required before
  tracer bullet. Phase 1.

### Not recommended (insufficient evidence)

- Design-request classifier — conductor routing handles classification
- Interface-specification validator — defer until schema stabilizes
- Token-sync tool — Figwright's `token_map` handles sync
- Visual-diff service — Figwright's `design_diff` provides baseline comparison

## ADR Candidates

- ADR-0024: Code-first token ownership (DEC-8)
- ADR-0025: Work Studio wraps Figwright (DEC-9)
- ADR-0026: Always-new Figma output (DEC-10)
- ADR-0027: Browser evidence gates Figma rendering (DEC-12)
- ADR-0028: Design artifacts in host project repository (DEC-11, 13, 14, 15)

## Implementation Readiness

**Ready for Phase 0 (architecture records) and Phase 1 (contract
infrastructure).** Both can proceed immediately with no external dependencies.

Phase 2 (tracer bullet) is blocked on: host project identification, Figwright
MCP configuration, and capability probe results.

Phase 3 is blocked on tracer bullet results validating DEC-9.
