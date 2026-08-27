# Agent execution architecture plan

**Work Object:** `2026-08-25-001` — Cross-harness agent-type adapter for execution-shaped skills
**Deliverable type:** plan — synthesis only. Every claim below is attributed to a specific Decision number (1–13, all recorded on this Work Object) or to the companion current-state deliverable ([`2026-08-25-001-agent-execution-current-state-reconstruction.md`](2026-08-25-001-agent-execution-current-state-reconstruction.md)). This document authors **no new architecture, no new decisions, and no invented steps** — where the underlying architecture-review request asked for something not yet decided, that section says so plainly and names the gap instead of filling it.
**Produced:** 2026-08-25

---

## A. Current-state reconstruction

Already produced as its own standalone document — see the companion deliverable linked above. Not repeated here.

## B. Gaps

`[decision]` Sorted per the original request's own framing (required now / likely later / explicitly unnecessary):

**Required now:**
- Copilot CLI dispatch is untested. `[system]` The evidence-ledger correction (2026-08-25) established `copilot` 1.0.65 is actually installed and callable — the earlier "unavailable" claim was wrong. Decision 13 sequences a real Copilot tracer bullet as the immediate next concrete action.

**Likely later (designed/decided, not yet built):**
- `AgentDescriptor` (Decision 8: shape decided — Pydantic model, `name`/`type`/`capabilities` — not yet added to `runtime/agents.py`).
- `runtime/graph.py` wiring — an `execute_specialist`-shaped node (Decision 11: director-approved to be *designed*, routed to `alawas-design-design-tracer-bullet`; the actual node spec does not exist).
- `runtime/tests/test_agents.py` (Decision 12: approach decided — real captured-output fixtures, matching the existing `test_handoff_graph.py` convention — file not yet written).
- Second adapter, `CopilotAgentAdapter` (Decision 9: approach decided — mirror `CodexAgentAdapter`'s shape via a real tracer bullet — adapter does not exist).
- `engineering-implement-bounded-change` migration (Decision 10: confirmed blocked pending a write-capable adapter — see Section G).
- Generator-script decision for agent-type portability (build a `tools/generate-adapters.py` equivalent, or continue hand-maintaining) — still an open item on this Work Object's success-evidence checklist, no Decision has resolved it.

**Explicitly unnecessary (per the original request's own list, and per Decision 2's accepted rationale — none proposed by any Decision):**
- Complex agent marketplace, agent-to-agent social protocols, persistent personas, dynamic cost optimization, autonomous hierarchy formation, dozens of agent classes, generalized distributed execution, a scoring/AI-routing resolver.

## C. Proposed architecture

`[inference]` Boundaries drawn below combine `[system]` facts from the current-state deliverable (Section A) with what Decisions 2, 3, and 8 actually settled. Only decided boundaries are drawn; where the original request asked for a boundary no Decision has resolved, that is marked as an open gap rather than invented.

```
Human Direction / Constitution / Domain Model / Governance layers
        -- unchanged, no Decision on this Work Object touches them --
                          |
                    Skills (skills/core/*)
                          |
              ┌───────────┴────────────┐
              |                        |
   Skill-config portability      Agent-type dispatch (NEW, this WO)
   (tools/generate-adapters.py,  runtime/agents.py: AgentRequest,
    adapters/*/skills/) --       AgentResult, AuthorityEnvelope,
    proven, unrelated layer      AgentAdapter (Protocol), AgentResolver
                                  (Decisions 2, 3, 8)
                                          |
                                  CodexAgentAdapter (Decisions 3-7, H below)
                                  CopilotAgentAdapter (not yet built, Decision 9)
                                          |
                          [OPEN GAP -- undecided]
                          Capability/tool adapters (deterministic
                          instruments: Lanser/FFmpeg/OPA-equivalent) --
                          the original request's own Section 10 model
                          distinguishes these from agent adapters; no
                          Decision on this WO has resolved where or
                          whether this distinct layer exists here.
                                          |
                          runtime/graph.py (LangGraph, Phase 6/research
                          graphs) -- sits BESIDE the agent-dispatch layer,
                          not inside it (Decision 3, grep evidence: the
                          graph today only builds HandoffEnvelope
                          *proposal* payloads, never dispatches for real).
                          An execute_specialist-shaped node to bridge them
                          is approved to be DESIGNED (Decision 11) but
                          does not exist yet.
                                          |
                          Canonical persistence (.work-studio/, tools/ws,
                          ADR 0025 single-writer rule) -- unchanged,
                          untouched by any Decision on this WO.
```

## D. Core contracts

`[system]` Read directly from `runtime/agents.py` as it exists today (not reconstructed from memory):

```python
class AuthorityEnvelope(BaseModel):
    inspect: bool = True
    modify_code: bool = False
    deploy: bool = False

class AgentRequest(BaseModel):
    task: str
    role: Optional[str] = None
    skill: Optional[str] = None
    work_object_id: Optional[str] = None
    context_refs: List[str] = []
    artifact_refs: List[str] = []
    required_capabilities: List[str] = []
    constraints: List[str] = []
    protected: List[str] = []
    authority: AuthorityEnvelope = AuthorityEnvelope()
    expected_output: str
    consequence: str = "low"

class AgentResult(BaseModel):
    status: Literal["completed", "blocked", "needs_approval", "failed"]
    summary: str
    outputs: List[str] = []
    evidence_candidates: List[str] = []
    proposed_actions: List[str] = []
    artifacts: List[str] = []
    unresolved_questions: List[str] = []
    tool_trace_ref: Optional[str] = None

@runtime_checkable
class AgentAdapter(Protocol):
    name: str
    async def run(self, request: AgentRequest) -> AgentResult: ...

class AgentResolver:
    def __init__(self, agents: List[AgentAdapter]): ...
    def resolve(self, required_type: str, required_capabilities: set[str]) -> Optional[AgentAdapter]: ...
```

`[decision]` Simplifications from the originating proposal, explicitly recorded in the code's own docstrings: `outputs`/`evidence_candidates`/`proposed_actions`/`artifacts` are `List[str]`, not the proposal's unspecified `ObjectRef`/`EvidenceCandidate`/`ActionProposal`/`ArtifactRef` types — a tracer bullet doesn't need a full type system for references it never populates with structured data.

`[decision]` **`AgentDescriptor` — decided in shape (Decision 8), not yet built.** A Pydantic model with `name`, `type`, `capabilities` fields, decoupled from any adapter instance so a future registry can describe an adapter without instantiating it. Does not exist in `runtime/agents.py` today — `CodexAgentAdapter` currently exposes these as plain class attributes (`name = "codex"`, `type = "coding"`, `capabilities = {...}`), not a separate descriptor object.

## E. Registry/configuration

`[decision]` Decision 8 resolved this directly: **in-code, no declarative config file.** `AgentResolver` is constructed from a plain Python list of adapters, matching the existing pattern (`AgentResolver([codex_adapter, ...])`). A YAML/JSON registry (mirroring `adapters/*/overlay.yaml`'s pattern) was explicitly considered and rejected as premature — nothing real to declare with only one working adapter and one undesigned candidate. **Revisit trigger (Decision 8):** if a non-engineer or external process ever needs to add/remove available agents without touching Python.

## F. Runtime integration

`[decision]` Decision 11: **director-approved to be designed, not yet designed.** The recommendation (wait until a real skill dispatch exists before wiring anything into `runtime/graph.py`) was explicitly overridden by the director. What was decided is narrower than "build the integration" — it's "produce a design for an `execute_specialist`-shaped node that would call `AgentResolver.resolve()` + an adapter's `run()` and feed `AgentResult` into graph state for routing," and that design work was routed to `alawas-design-design-tracer-bullet` as a separate next step, not authored inline in the decision itself. **No node spec exists yet.** Decision 11's own edge-case note: this design is being produced against zero real consumers (no skill has completed a real dispatch through any adapter yet), so revision once real evidence exists is an accepted, expected cost — not a failure of the design when it lands.

## G. Skill migration

`[decision]` `engineering-implement-bounded-change` remains an **explicit open gap** — no migration steps exist or are proposed. The full blocking chain, in order:
1. Decision 2 named it as the first migration target (needs `file_write`/`terminal_run`, genuinely execution-shaped).
2. Decision 6 attempted write-mode dispatch through `CodexAgentAdapter` — **failed**: Codex's patch tool was rejected as blocked by a read-only sandbox despite `--sandbox workspace-write` being requested; independently verified no file was written.
3. Decision 7 reverted `CodexAgentAdapter` to read-only-only and broadened its failure classification (see H) — the adapter is not currently write-capable in this environment.
4. Decision 10 confirmed the migration stays blocked pending some adapter demonstrating real write capability — Copilot's write-mode is explicitly deferred to its own later decision (Decision 10), not assumed.

## H. First adapter

`[system]` `CodexAgentAdapter` is real, built, and tested three times against actual `codex exec` dispatches (Decisions 3, 6, 7) — including one full pass→fail→fix cycle. Current invocation, read directly from the file:

```
codex exec --json --sandbox read-only --skip-git-repo-check --ignore-user-config -c mcp_servers={} <task>
```

`[system]` `--sandbox read-only` alone does not block MCP tool calls — Decision 5 found a live `rmcp` connection attempt to `mcp.cloudflare.com` even with `--ignore-user-config` set; `-c mcp_servers={}` is what actually verified clean (confirmed via direct trace inspection, no MCP-related lines).

`[system]` Classification logic, current code: parses `--json` stdout for `{"type":"item.completed","item":{"type":"agent_message","text":...}}` events for the final message. Maps to `status="blocked"` (not `"completed"`) when either (a) a `command_execution` item reports `status="failed"` (Decision 4), or (b) `stderr` contains `"error=patch rejected"` — a rejected internal patch-tool call, which never surfaces as a `command_execution` item (Decision 7). Both paths were independently verified against real dispatches, not just code review.

`[decision]` `capabilities = {"retrieve", "inspect_code", "hypothesize"}` — read-only only, per Decision 7's revert. `modify_code` was added in Decision 6, tested, found non-functional in this environment, and removed in Decision 7.

## I. Second validation adapter

`[decision]` Decision 9 resolved the **approach**, not the adapter: `CopilotAgentAdapter` will mirror `CodexAgentAdapter`'s exact shape (subprocess → parse JSONL → `AgentResult`), starting read-only-equivalent via Copilot's per-tool permission model (`--deny-tool`/`--allow-tool`, since no single sandbox-mode flag exists in `copilot --help`) plus `--disable-builtin-mcps`/`--disable-mcp-server`. Explicitly **not designed on paper** — Decision 9's own rationale: this Work Object already paid the cost once of an assumed event schema being wrong (Decision 3's first parser draft), and Copilot's real JSONL shape is unverified. Decision 13 sequences this as the very next concrete action.

## J. Testing plan

`[decision]` Decision 12: a real test file, `runtime/tests/test_agents.py`, matching the repo's existing `runtime/tests/test_handoff_graph.py` convention. **Fixture constraint, load-bearing:** fixtures must be real captured output from this session's actual `codex exec` dispatches — never hand-typed/invented mocks. This formalizes checks already performed manually across Decisions 3–7 and 10 (the clean "PONG" case, the blocked-on-failed-command case, the blocked-on-patch-rejected case, MCP suppression) rather than inventing new speculative coverage. **Not yet written.**

## K. Incremental implementation sequence

**Backward (what actually happened, Decisions 1–13, in order):**
1. Canonical agent-type body + 3 harness transcriptions, verified byte-identical (Decision 1).
2. Runtime dispatch layer built — `AgentRequest`/`AgentResult`/`AgentAdapter`/`AgentResolver`/`CodexAgentAdapter` (Decision 2, director override of a "wait" recommendation).
3. First real dispatch, parser fixed against real output (Decision 3).
4. Status-vocabulary gap found and fixed — `blocked` for failed commands (Decision 4).
5. `node_repl`/MCP sandboxing gap found and fixed — `mcp_servers={}` (Decision 5).
6. Write-mode attempted, failed (Decision 6).
7. Reverted to read-only-only, `blocked`-classification broadened for rejected patch calls, both re-verified (Decision 7).
8. `AgentDescriptor` shape decided (Decision 8).
9. Second-adapter approach decided (Decision 9).
10. Skill-migration path confirmed blocked, honestly (Decision 10).
11. Runtime-wiring design approved, director override (Decision 11).
12. Test-suite approach decided (Decision 12).
13. Sequencing set (Decision 13).

**Forward (Decision 13's own sequencing — not new authoring):**
1. Real Copilot read-only tracer bullet (Section I) — next concrete action.
2. `runtime/graph.py` wiring design (Section F) and the test suite (Section J), in either order after (1), explicitly revisable if Copilot's real evidence changes their shape (Decision 13's own revisit trigger).

## L. What NOT to build

`[decision]` Per Decision 2's accepted rationale and the original request's own explicit list — none proposed by any Decision on this Work Object: complex agent marketplace, agent-to-agent social protocols, persistent personas (`DesignAgent`/`ResearchAgent`/`CriticAgent`-style permanent roles), dynamic cost optimization, autonomous hierarchy formation, dozens of agent classes, generalized distributed execution, a scoring/AI-routing resolver (Decision 2: "no AI routing... no scoring model," reaffirmed by Decision 8's plain-list registry).

## M. Final recommended tracer

`[decision]` Decision 13's own resolution: the real Copilot read-only tracer bullet, exactly mirroring Decisions 3–5's discipline (real dispatch → discover the actual event schema → parse it → verify independently, never trusting the adapter's own summary), is the smallest next vertical slice. It is recommended ahead of the runtime-wiring design and the test suite because it is the only queued item that still generates genuinely new evidence — the other two are lower-risk and would benefit from having real Copilot output available first.

---

## Provenance summary

Every claim above traces to Decisions 1–13 on `2026-08-25-001`, the companion current-state deliverable, or a direct read of `runtime/agents.py` as it exists today. No new architecture, contract field, registry format, migration step, or test case was invented in this document. Every open gap (Copilot untested, `AgentDescriptor` unbuilt, no config registry, no graph node spec, `engineering-implement-bounded-change` blocked, second adapter undesigned, no test file, generator-script decision unmade) is named explicitly above, not papered over.
