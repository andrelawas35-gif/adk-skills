# Claude Design MCP — Model-Agnostic Integration Plan

**Source:** Claude Design MCP Model-Agnostic Integration Grilling Session
**Date:** 2026-07-27
**Status:** Decided — 25 human-accepted decisions
**Work Objects:** 2026-07-27-004, -005, -006, -007

---

## 1. Executive summary

Work Studio integrates Claude Design as an **abstract capability** (`claude_design`)
in its existing capability classification system, reached through **direct MCP**
from any runtime that supports it. No gateway, no adapter service, no new
infrastructure.

The integration is model-agnostic because of one decision: the **implementation
brief is self-sufficient**. An agent with no Claude Design access — on any
runtime, from any provider — can implement an approved design from the brief
alone, using only what is committed to Git.

Everything else follows from that. Coordination is the Work Object. Approval is
an Evidence Ledger entry. Agent selection is the user opening a terminal.

---

## 2. What the repository already provides

The grilling session found that Work Studio's existing machinery covers most of
what the integration needs. Nothing below was built for this integration; all of
it is reused as-is.

| Existing mechanism | Location | Role in the integration |
|---|---|---|
| Capability classification | `adapters/*/overlay.yaml` | Declares `claude_design` availability per platform |
| Capability degradation | `references/CAPABILITY-DEGRADATION.md` | Handles unauthenticated and unavailable states |
| Lazy detection | `CAPABILITY-DEGRADATION.md:16-23` | Exactly the "tool present, execution fails" case |
| Consequence authority | `references/CONSEQUENCE-AUTHORITY.md` | External writes already require human confirmation |
| Evidence Ledger + provenance tags | ADR 0016 | Carries all cross-agent design state |
| Work Objects | `.work-studio/objects/` | Mediates agent coordination |
| Single-session assumption | ADR 0020 | Makes concurrency low-risk |
| Adapter generator | `tools/generate-adapters.py` | Propagates contracts to all platforms mechanically |

**Correction found during plan production:** the five retired design skills
(`render-to-figma`, `connect-design-to-code`, `model-user-flow`,
`define-interface-architecture`, `define-interface-specification`) are already
absent from `skills/core/`, from all three adapter skill directories, and from
all three manifests as of commit `936b4af`. DEC-CD-12 and the originally planned
prune Work Object are **already satisfied**. The five-Work-Object sequence from
DEC-CD-23 is therefore executed as four.

---

## 3. Architecture

```
Human natural-language direction
        ↓
design-apply-design-direction
        ↓
   ┌────┴────┐
Path A     Path B
(code)   (Claude Design)
   │         │
   │    auth probe → fail → manual-fallback ("run /design-login")
   │         ↓
   │    Claude Design MCP (tools discovered at runtime)
   │         ↓
   │    [system:design-project-ref]  claude-design:<id>
   │    [system:design-direction]    + structured implementation brief
   └────┬────┘
        ↓
   Human review (Claude Design canvas / browser)
        ↓
   [system:design-approval]  version ref + brief ref + scope
        ↓
   ═══ Git commit — the agent boundary ═══
        ↓
   ANY runtime reads the Evidence Ledger
   (no Claude Design access required)
        ↓
   engineering-implement-bounded-change  ← works from brief alone
        ↓
   design-verify-design-implementation   ← brief-to-browser
        ↓
   [system:verification-report]
```

**The hypothesised gateway was rejected.** All three supported platforms speak
MCP, so a gateway would add a hop, a failure mode, and a component to maintain
without adding reach. Runtimes that cannot reach Claude Design are served by the
brief, not by a proxy.

---

## 4. The 25 decisions

### Access and capability

| ID | Decision |
|----|----------|
| DEC-CD-1 | Claude Design is an abstract capability (`claude_design`) in the existing classification system |
| DEC-CD-2 | Direct MCP. No gateway, adapter service, or delegated executor |
| DEC-CD-5 | `native` on all MCP runtimes; mandatory pre-invocation authentication probe |
| DEC-CD-19 | Authentication is the only gate. No runtime trust hierarchy, no per-runtime scoping |
| DEC-CD-21 | Two adapter units: skill exclusion (already done), capability addition |

### Evidence and identity

| ID | Decision |
|----|----------|
| DEC-CD-3 | External reference recorded as `[system:design-project-ref]` |
| DEC-CD-4 | Convention-within-prose format, not a new structured schema |
| DEC-CD-6 | Self-reported runtime and model attribution on design evidence |
| DEC-CD-16 | Provider prefix: `claude-design:<identifier>` |
| DEC-CD-24 | No new visualization tooling — greppable evidence is sufficient |

### Contracts and routing

| ID | Decision |
|----|----------|
| DEC-CD-7 | Contracts describe intent; implementations hold tool calls; adapters stay mechanical |
| DEC-CD-8 | Token inventory per-pass with git revision tracking; sync explicit, not standalone |
| DEC-CD-9 | `design-apply-design-direction` gains Path A / Path B routing |
| DEC-CD-10 | **Path B brief is self-sufficient** — the load-bearing decision |
| DEC-CD-11 | Verification is brief-to-browser; Claude Design comparison optional |
| DEC-CD-25 | The brief is the universal revision request, for MCP and non-MCP agents alike |

### Governance

| ID | Decision |
|----|----------|
| DEC-CD-14 | Version-ref freshness check before revision; stale → surface and pause |
| DEC-CD-15 | Authority tiers; no unattended invocation; no automatic retry; alternatives uncapped |
| DEC-CD-17 | Approval is an Evidence Ledger entry, not a state machine |
| DEC-CD-18 | The user selects the implementation agent; portability is the contract |
| DEC-CD-20 | Failures use the existing degradation pattern; Path B → Path A fallback always explicit |

### Records and validation

| ID | Decision |
|----|----------|
| DEC-CD-12 | Five retired design skills stop generating — **already satisfied at commit 936b4af** |
| DEC-CD-13 | ADR dispositions: 0024 retain, 0025 supersede, 0026 archive, 0027 retain, 0028 amend; two new ADRs |
| DEC-CD-22 | Tracer bullet: one component, Claude Code designs, Codex implements |
| DEC-CD-23 | Sequential migration — revised from five Work Objects to four |

---

## 5. Authority mapping

| Operation | Tier | Gate |
|---|---|---|
| Authentication probe | low | none |
| Read or inspect existing project | low | none |
| Design-system sync | meaningful | explicit authorization (DEC-CD-8) |
| Create project | meaningful | human confirmation |
| Create alternatives | meaningful | human confirmation — the confirmation *is* the cap |
| Revise design | meaningful | human confirmation + freshness check |
| Branch direction | meaningful | human confirmation |
| Export prototype | meaningful | human confirmation |

**No unattended invocation.** Background and scheduled agents cannot invoke
Claude Design. **No automatic retry** — a failure is recorded and surfaced.

---

## 6. Failure behavior

All failure modes route through the existing `CAPABILITY-DEGRADATION` tiers. No
new machinery.

| Failure | Behavior |
|---|---|
| Not authenticated | `manual-fallback`; one instruction: run `/design-login`; gap recorded |
| Service unavailable | Native attempted and failed; recorded; Path A offered |
| Rate limited | Recorded; surfaced; paused |
| Mid-operation error | Partial state recorded; no retry; user decides |
| Stale version detected | Conflict surfaced; paused (DEC-CD-14) |
| User rejects the design | Not a failure — no approval entry, revision cycle continues |

**Path B → Path A fallback is never silent.**

---

## 7. Execution sequence

| Work Object | Scope | Decisions | Depends on |
|---|---|---|---|
| ~~prune~~ | ~~exclude retired skills~~ | ~~DEC-CD-12~~ | **already complete (936b4af)** |
| [2026-07-27-004](../../.work-studio/objects/2026/07/2026-07-27-004-add-claude-design-capability-to-platform-overlays-and-degradation-catalog.md) | `claude_design` capability in catalog + 3 overlays; regenerate | 1, 5, 20, 21 | — |
| [2026-07-27-005](../../.work-studio/objects/2026/07/2026-07-27-005-extend-design-skill-contracts-with-claude-design-routing-brief-and-approval.md) | Path A/B routing, brief, approval, verification, evidence conventions | 3, 4, 6–11, 14–19, 25 | -004 |
| [2026-07-27-006](../../.work-studio/objects/2026/07/2026-07-27-006-execute-adr-dispositions-for-claude-design-integration.md) | Five ADR dispositions + two new ADRs | 13 | -005 |
| [2026-07-27-007](../../.work-studio/objects/2026/07/2026-07-27-007-claude-design-cross-agent-tracer-bullet.md) | Cross-agent tracer bullet | 22 | -006 |

Strictly sequential. ADRs are written after the contracts they describe so they
record what was built rather than what was planned.

---

## 8. What is deliberately not built

| Not built | Because |
|---|---|
| Capability gateway / adapter service | All three platforms speak MCP directly (DEC-CD-2) |
| Design artifact registry | Work Objects and the Evidence Ledger already carry this |
| Approval state machine | An evidence entry provides the same traceability (DEC-CD-17) |
| Work Object locking | ADR 0020 assumes one session per workspace (DEC-CD-14) |
| Agent routing or capability scoring | The user picks the agent (DEC-CD-18) |
| Runtime trust hierarchy | Authentication is the gate (DEC-CD-19) |
| Governance dashboard | Evidence entries are greppable (DEC-CD-24) |
| Abstract design-artifact schema | Premature — one provider so far (DEC-CD-16) |
| Automatic retry / conflict resolution | Surfacing beats guessing (DEC-CD-15, DEC-CD-14) |

---

## 9. Known unknowns

| Unknown | Resolved by |
|---|---|
| Claude Design MCP tool names, arguments, version semantics | First authenticated discovery (WO -007). Never hardcoded. |
| Whether the tool surface supports the freshness check assumed by DEC-CD-14 | WO -007. If unsupported, DEC-CD-14 returns for revision. |
| Exact required fields of a self-sufficient brief | WO -007. If Codex cannot implement from the brief, the schema returns to WO -005. |
| Which Creative Coding Studio component is the tracer bullet target | Named at WO -007 `frame` time |

The session rule against inventing Claude Design MCP tool names was held
throughout. No decision depends on a specific tool signature.

---

## 10. The falsifiable claim

> A structured implementation brief, committed to Git, contains enough for an
> agent with no Claude Design access to implement an approved design correctly.

If WO 2026-07-27-007 shows otherwise, the integration is not model-agnostic and
the brief schema returns to WO 2026-07-27-005. That outcome is a valid result,
not a failure of the run.
