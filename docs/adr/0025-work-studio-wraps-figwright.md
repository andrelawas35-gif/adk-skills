# Work Studio Wraps Figwright

- **Status:** Deferred (2026-07-23)
- **Date:** 2026-07-22
- **Deferred:** 2026-07-23
- **Component:** Design skill architecture
- **Decision owners:** Human-approved (Grilling Session 12, ephemeral; deferred per Grilling Session 13)
- **Related Work Object:** `2026-07-22-006` (original), `2026-07-23-001` (deferral)
- **Related ADRs:**
  - related to: ADR 0024 (code-first tokens — Figwright executes the code→Figma token sync)
  - related to: ADR 0026 (always-new Figma output — write policy Figwright must follow)
  - related to: ADR 0027 (browser evidence gate — precondition before Figwright invocation)
- **Supersedes:** None
- **Superseded by:** None

## Context

Figwright (the Figma MCP server) provides design execution capabilities: tech-stack detection, component reuse, canvas read/write, design diffing, and the `figma-build` and `figma-codegen` skills. Work Studio provides governance: authority gates, evidence recording, preservation policy, capability degradation, and lifecycle integration.

The question: should Work Studio's design skills invoke Figwright directly, wrap it with governance, or build independent Figma capabilities?

## Decision

Work Studio design skills wrap Figwright's skills (`figma-build`, `figma-codegen`). Figwright provides execution; Work Studio provides governance. The boundary is explicit and the wrapping is the highest-risk assumption in the architecture — the first tracer bullet (DEC-22) tests this decision specifically.

### Boundary

**Figwright owns execution:**
- Tech-stack detection
- Component and token mapping
- Icon mapping
- Canvas read and write operations
- Design diff
- `figma-build` and `figma-codegen` skill invocations

**Work Studio owns governance:**
- Authority gates (check consequence level before any Figwright invocation)
- Evidence recording (capture inputs and outputs of Figwright calls)
- Preservation policy (always-new pages, approved frame protection)
- Capability degradation (complete code-side workflow when Figwright unavailable)
- Lifecycle integration (map Figwright operations to Work Object states)

### Wrapping contract

1. **Authority before invocation.** Every Figwright call is preceded by a consequence-level check. Meaningful-consequence calls proceed; high-consequence calls require explicit named confirmation.

2. **Evidence after invocation.** Every Figwright response is recorded in the Evidence Ledger with inputs, outputs (including node IDs), and success/failure status.

3. **Preservation policy enforced.** Figwright is instructed via its input parameters to create new pages/sections. Work Studio never passes parameters that would modify approved frames without high-consequence confirmation.

4. **Capability degradation.** When Figwright is unavailable, the code-side workflow completes fully. Figma-dependent steps are deferred with `[system:capability-gap]` entries. The workflow does not fail — it completes with explicit gaps.

### Undocumented capabilities to verify

The tracer bullet must verify before full implementation:

- Branch creation behavior
- Node deletion behavior
- Node ID return format after writes
- Content preservation on update
- Section creation support

## Scope

This decision applies to:

- `render-to-figma` (primary Figwright consumer)
- `connect-design-to-code` (component mapping via Figwright)
- `verify-design-code-parity` (design diff via Figwright)
- Any future skill that needs Figma read/write

This decision does not apply to:

- Skills that only operate on code (audit, foundation, specification)
- Direct user invocation of Figwright outside Work Studio
- Figwright's internal behavior or governance

## Rationale

**Wrapping preserves both capabilities.** Figwright already handles the complex Figma API interaction, tech-stack detection, and component mapping. Rebuilding these capabilities would be wasteful and fragile. Wrapping adds governance without duplicating execution.

**The governance gap is real.** Figwright has no concept of Work Objects, evidence ledgers, authority levels, or preservation policy. Without wrapping, a design skill could modify approved frames, create output from unverified input, or fail silently when Figma is unavailable. The governance layer ensures design work follows the same authority and evidence patterns as all other Work Studio work.

**The tracer bullet validates the assumption.** This is the highest-risk decision in the architecture because it depends on Figwright's behavior matching Work Studio's expectations. DEC-22 tests this explicitly — if Figwright's interface doesn't support the wrapping contract, this decision must be revised before building skills on the assumption.

## Alternatives Considered

### Build independent Figma capabilities

Work Studio implements its own Figma API integration, bypassing Figwright entirely.

Rejected because: the Figma API is complex, and Figwright already handles tech-stack detection, component reuse, and canvas operations. Building independently would duplicate significant effort and create a maintenance burden for Figma API changes.

### Use Figwright directly without wrapping

Design skills invoke Figwright's tools directly, treating them as any other MCP tool.

Rejected because: Figwright has no governance layer. Direct invocation bypasses authority gates, evidence recording, and preservation policy. A skill could modify approved frames or create Figma output from unverified input without any checkpoint.

### Build a Figma governance middleware

Create a separate MCP server that sits between Work Studio and Figwright, handling governance at the protocol level.

Rejected because: an MCP middleware adds infrastructure complexity (another server to configure, maintain, and debug) for a problem that skill-level wrapping solves. The governance logic is specific to Work Studio's authority model — it belongs in the skills, not in a generic middleware.

## Consequences

**Positive:**
- Figwright's execution capabilities are available without reimplementation
- Governance (authority, evidence, preservation) applies uniformly to all Figma operations
- Capability degradation is explicit — workflows complete with documented gaps rather than failing
- The tracer bullet provides concrete evidence for or against this approach before full investment

**Negative:**
- Wrapping depends on Figwright's interface remaining stable — changes to Figwright's tool signatures require skill updates
- Undocumented Figwright behaviors (branch creation, node deletion, content preservation) may invalidate assumptions
- If the tracer bullet fails, significant rework is needed — the wrapping assumption is load-bearing for 3 of 9 design skills

**Neutral:**
- Figwright configuration (MCP setup, API keys) remains the host project's responsibility
- Figwright's own governance (if it develops one) would be complementary, not competing

## Deferral record

### 2026-07-23 — Grilling Session 13: Deferred

**Authority:** DEC-A2 (workflow is NL → agent → code → browser), DEC-A3
(tool is a governed review/iteration layer, not a visual editor), Grilling
Session 13 (14 accepted decisions)

**Reason:** Figma was never adopted. The entire Figma architecture (Figwright
wrapping, Figma output, Figma token sync) was aspirational. Grilling Session 13
established that the design workflow is NL → agent → code → browser, with a
local-first design review layer replacing the need for Figma as a design
surface. The governance patterns from this ADR (authority gates, evidence
recording, capability degradation) survive in the review layer architecture.
The wrapping decision itself is deferred until Figma collaboration is needed.

**Revisit trigger:** Figma collaboration becomes a real requirement (not
aspirational). At that point, reassess whether Figwright wrapping or a
different integration pattern is appropriate.

**Related skills deferred:** `render-to-figma`, `connect-design-to-code`

**Full plan:** `docs/design/local-first-design-review-layer-plan.md`
