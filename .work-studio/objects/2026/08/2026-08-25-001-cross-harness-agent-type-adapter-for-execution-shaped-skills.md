---
schema_version: 1
id: 2026-08-25-001
title: Cross-harness agent-type adapter for execution-shaped skills
type: project
status: active
state: design
consequence: meaningful
sensitivity: ordinary
domain: [governance, engineering]
created_at: 2026-08-25T17:50:06Z
updated_at: 2026-08-25T23:35:52Z
next_action: execute_specialist node implemented (Decision 19). Awaiting director: (1) test suite (Decision 12); (2) real skill dispatch through the graph; or (3) close this Work Object.





































---
## Intent

<!-- Describe what this Work Object accomplishes and why it exists. -->

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Canonical Blender-operator agent-type body authored, grounded in alawas-production-operate-blender/SKILL.md.
- [x] Body transcribed verbatim into three native harness formats (.claude/agents/*.md, .codex/agents/*.toml, .copilot/agents/*.md).
- [x] Instruction-body content diffed across all three — confirmed byte-identical after correcting one transcription slip (dropped backticks/arrow in first TOML draft).
- [x] Codex CLI dispatch-and-parse path verified real (runtime/agents.py, CodexAgentAdapter): two real codex exec calls made, correctly mapped to AgentResult. One task succeeded cleanly (status=completed, summary="PONG"); one task's honest failure (sandbox helper missing in this environment) also mapped to status=completed, exposing a real vocabulary gap.
- [x] Native .codex/agents/blender-operator.toml loading confirmed broken (not merely unverified) -- real Codex parser rejects it: "invalid type: sequence, expected a map" for mcp_servers. Independently corroborated by a separate, concurrent Codex Desktop session's own evidence entry, which dispatched the blender-operator contract successfully via its subagent runner but explicitly caveated that this "does not prove native loading" of the same file.
- [ ] ~~Copilot harness dispatch remains untested.~~ [REMOVED] CopilotAgentAdapter removed from plan by director decision. Copilot CLI confirmed installed (v1.0.65) but adapter path no longer pursued.
- [ ] Generator-script decision made (build `tools/generate-adapters.py`-equivalent for agent types, or continue hand-maintaining).
- [x] Write-mode reverted (Decision 7); CodexAgentAdapter treated as read-only-only for now. Decision 6's exact failing task re-run against the reverted adapter -- reproduced the same real "patch rejected" failure, independently confirmed output.txt still not created, and AgentResult now correctly returns status=blocked instead of completed. Regression-checked: the clean "PONG" case still returns completed with no change in behavior.
- [x] OpenCodeAgentAdapter tracer bullet verified (Decision 15): two real `opencode run --format json --auto` dispatches made. PONG test passed (status=completed). Nonexistent-file test correctly detected tool_use failure (status=blocked). Zero model-tier binding confirmed — model passed via --model at invocation time, never hardcoded. Replaces previously-proposed DeepSeek adapter target with OpenCode (75+ providers via Models.dev).
- [x] OpenCodeAgentAdapter write capability verified (Decision 16): real write dispatch created output.txt with correct content. Independent verification confirmed. Regression check: PONG test unaffected. Closes Decision 10's open gap — an adapter now demonstrates real write capability, unblocking skill migration.


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->

**Non-goals:**
<!-- Explicitly excluded work. -->

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Hand-author canonical Blender-operator agent-type body plus three format transcriptions as tracer bullet

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Test whether one canonical agent-type persona body (name, description, tools allowlist, instruction prose) can be reused verbatim across three harness wrapper formats — `.claude/agents/blender-operator.md` (YAML frontmatter + Markdown body), `.codex/agents/blender-operator.toml` (TOML fields, body in `developer_instructions`), and a GitHub Copilot custom-agent Markdown+frontmatter file — for the production-operate-blender pilot. Hand-authored, not scripted; no generator, no registration, no live dispatch through any of the three files. |
| **Authorization** | Director accepted the tracer-bullet recommendation in chat, 2026-08-25: "accept, hand-author the canonical body and three transcriptions." |
| **Confidence** | medium — the wrapper-shape claim (YAML+MD vs YAML+MD vs TOML-field) is well-evidenced from confirmed harness docs; whether the body content survives unchanged is exactly what this tracer bullet tests, so confidence in the outcome itself is deliberately unresolved pending the diff. |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design) |
| **Revisit trigger** | If the three transcribed bodies require real content divergence (not just wrapper syntax) to be valid/usable in their format, the "single canonical body" assumption fails and this Work Object returns to Design to pick a fallback (shared prose fragments composed per format, or accepted hand-maintained bodies) instead of building a generator. |
| **Rationale** | Smallest reversible slice that tests the riskiest assumption (canonical body portability) before committing to build a generator script — isolates the content-portability question from generator-tooling risk. |

### Decision 2 — Build runtime AgentRequest/AgentAdapter/AgentResolver dispatch layer now (director override)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Build exactly four pieces: `AgentRequest` and `AgentResult` (Pydantic models), `AgentAdapter` (Protocol), `AgentResolver` (registry-iteration match on agent type + capabilities, no scoring/routing AI). Implement one adapter, `CodexAgentAdapter`. Migrate one existing skill, `alawas-engineering-implement-bounded-change`, through the new seam as its first real caller. Nothing broader (no second adapter, no other skills migrated) until this pilot is verified. |
| **Authorization** | Director explicit override, chat 2026-08-25: "go build now" — rejecting the recommended Branch B (wait for a confirmed second case) in favor of Branch A (build now), after the pressure test surfaced both branches' evidence, costs, and edge cases. |
| **Confidence** | medium-high for Branch B (wait) going in, per the pressure test; director overrode with no stated concrete near-term dispatch case on record — this is a deliberate bet against the studio's own "two real cases earn an abstraction" working method, not a case where new evidence flipped the recommendation. Recorded plainly as an override, not as evidence-driven agreement. |
| **Actor** | Director (decision), alawas-thinking-pressure-test-decision (pressure test) |
| **Revisit trigger** | If `CodexAgentAdapter` sits unused after the one pilot skill migration — no second adapter, no second skill, no real dispatch call in practice within a reasonable working period — this is the "dead abstraction" edge case named during the pressure test and should trigger a revisit via `alawas-governance-maintain-working-method`. Also revisit if `CodexAgentAdapter.run()` needs execution context only `runtime/graph.py`'s checkpointed model can supply cleanly — that would mean this layer belongs inside the graph, not beside it, and is a design question, not an implementation surprise. |
| **Rationale** | Director's explicit call, made with full visibility into the pressure test's evidence for both branches. Overrides this session's own prior "wait" reasoning by choice, not by new fact. |

### Decision 3 — Tracer bullet for the dispatch layer: runtime/agents.py + one real codex exec call

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Write `runtime/agents.py` (new module, sits beside `runtime/graph.py`, not inside it) containing `AgentRequest`, `AgentResult` (Pydantic models), `AgentAdapter` (Protocol), `AgentResolver` (registry-iteration match), and `CodexAgentAdapter`. Make one real `codex exec` subprocess call from `CodexAgentAdapter.run()` against a harmless, throwaway prompt in an isolated scratch directory (not this repo). No real bounded-change work dispatched through it yet -- that is a separate, later authorization. |
| **Authorization** | Director accepted the tracer-bullet recommendation, chat 2026-08-25: "accept, make the real codex exec call." |
| **Confidence** | medium — grep confirmed `runtime/graph.py` performs no real model/subprocess dispatch today (only builds HandoffEnvelope proposal payloads), resolving where this layer sits; `codex` CLI confirmed installed and has a documented `codex exec` non-interactive subcommand. What's untested is whether its output maps cleanly into `AgentResult`'s fixed status vocabulary. |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design) |
| **Revisit trigger** | If `codex exec` requires auth/config unavailable in this environment, or its output can't be mapped into `AgentResult` without loss, the contract or adapter needs revision before Decision 2's pilot can be called verified. |
| **Rationale** | Tests the one real uncertainty (does dispatch actually work) rather than the trivial part (contract shape); isolates real command execution to a scratch directory so failure carries no repo-state cost. |

### Decision 4 — Fix AgentResult status-vocabulary gap by reusing `blocked`, not adding a new status value

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | `CodexAgentAdapter.run()` now tracks whether any `command_execution` item in a `codex exec --json` run reported `status: "failed"`. If so, the result maps to `status="blocked"` (task prevented from completing by an external constraint) even when Codex still produced a final `agent_message`. Only maps to `completed` when no command failed. No schema change to `AgentResult`'s four-value Literal. |
| **Authorization** | Director accepted, chat 2026-08-25: "accept, use blocked." |
| **Confidence** | medium — reused vocabulary correctly separates the two real cases already exercised (Test 1 file-read now `blocked`; Test 2 PONG still `completed`). Acknowledged as a heuristic: a failed command does not always mean the overall task failed (Codex might recover via another path) -- errs toward `blocked` over a silently-trusted `completed`, which is the safer direction for a dispatch layer feeding a governed system, not a fully precise classifier. |
| **Actor** | Director (accept), alawas-engineering-implement-bounded-change (implementation) |
| **Revisit trigger** | If a real dispatch produces a case where Codex recovers from a failed command and genuinely completes the task, but this heuristic still reports `blocked`, the classification needs refinement (e.g. checking whether the final agent_message content itself asserts success despite the earlier failure) rather than a blanket any-failure-means-blocked rule. |
| **Rationale** | Reusing existing vocabulary avoids widening `AgentResult`'s contract for a gap closeable with adapter-side logic; `blocked` is semantically the correct existing word for "prevented from completing," not `failed` (which implies the adapter/process itself errored) or `completed` (which implies the task was achieved). |

### Decision 5 — Close the node_repl/MCP sandboxing gap: `-c mcp_servers={}` (not `--ignore-user-config` alone)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | `CodexAgentAdapter.run()`'s command line now includes `--ignore-user-config -c mcp_servers={}` in addition to `--sandbox read-only --skip-git-repo-check`. First attempt (`--ignore-user-config` alone) was tested and found insufficient -- a live `rmcp` worker still tried to connect to `mcp.cloudflare.com` (a server not even in `~/.codex/config.toml`, so likely project-level config `--ignore-user-config` does not reach). The explicit empty-table override was tested directly and confirmed no MCP connection attempts occur. |
| **Authorization** | Director accepted, chat 2026-08-25: "accept, add ignore-user-config and verify." The verification step itself is what surfaced that the initial fix was insufficient -- corrected before recording, not after. |
| **Confidence** | medium-high on the MCP suppression itself (directly observed: zero MCP-related lines in the raw trace with the override, versus a live connection attempt without it). Lower confidence on one adjacent observation: the same re-run's file-read test (Test 1, previously `blocked` due to a missing Windows sandbox helper) unexpectedly returned `completed` with a correct answer this time. Cause unconfirmed -- may be unrelated to this fix (flaky infra, first-run helper caching) -- not claimed as caused by the MCP change. |
| **Actor** | Director (accept), alawas-engineering-implement-bounded-change (implementation and correction) |
| **Revisit trigger** | If a future real dispatch genuinely needs a specific MCP tool, `mcp_servers={}` needs to become an explicit allowlist (e.g. `mcp_servers={name={...}}`) rather than a blanket empty override -- deliberate, not inherited. Also revisit if the Windows-sandbox-helper failure recurs; its apparent resolution here is unexplained and unverified as fixed. |
| **Rationale** | A bounded dispatch layer should not inherit whatever MCP servers happen to be configured in the operator's personal Codex install -- unsandboxed code execution reachable through an inherited tool is a real risk for any future non-tracer-bullet dispatch. |

### Decision 6 — Write+verify tracer bullet for CodexAgentAdapter (second real case toward engineering-implement-bounded-change migration)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Switch `CodexAgentAdapter` to `--sandbox workspace-write` (confined to the existing scratch directory via `--cd`, never `danger-full-access`) and add `modify_code` to its declared `capabilities`. Dispatch one task: create `output.txt` in the scratch directory containing exactly `tracer-bullet-write-ok`. Verify independently (read the file myself, not trust the adapter's self-reported summary). No repository files touched, no `alawas-engineering-implement-bounded-change` SKILL.md changes, no real skill migration yet -- this tests only whether the adapter can write and be trusted about it. |
| **Authorization** | Director accepted, chat 2026-08-25: "i accpet" [sic]. |
| **Confidence** | medium — read-mode dispatch is proven (Decisions 3-5); write-mode has never been exercised through this adapter. This is exactly the untested gap named when evaluating the migration target. |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design) |
| **Revisit trigger** | If `output.txt`'s content doesn't match after dispatch, or the adapter reports `completed` when the file is actually missing/wrong (an honest-failure-misclassified-as-success case, same shape as Decision 4's original bug), the write path needs its own fix before any real skill migration is attempted. If it passes cleanly, the next separate decision is whether to route an actual scoped piece of `engineering-implement-bounded-change`'s work through the adapter -- not automatic from this passing. |
| **Rationale** | Smallest reversible step toward the second real dispatch case Decision 2's own rationale asked for, isolating "can this adapter write and be trusted" from "should a real governed skill be migrated," which is a separately-authorized, larger question. |

### Decision 7 — CodexAgentAdapter treated as read-only-only for now; broaden blocked-classification unconditionally; defer sandbox investigation

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Three-part resolution of Decision 6's open question: (1) `CodexAgentAdapter`'s `capabilities` reverts write-related entries (`modify_code` removed; the `--sandbox workspace-write` change is reverted back to `read-only`) -- the adapter is treated as read-only-only in this environment until further notice. (2) `CodexAgentAdapter`'s failure classification is broadened to also map a rejected patch-tool call (the `codex_core::tools::router: error=patch rejected...` pattern) to `status="blocked"`, independent of whether (3) ever happens. (3) Diagnosing/fixing the underlying Windows sandbox enforcement gap is explicitly deferred as optional future work, not decided or scheduled today. |
| **Authorization** | Director accepted, chat 2026-08-25: "i accept," following the pressure test's recommendation. |
| **Confidence** | medium-high on (1) and (2) -- both are grounded directly in Decisions 3 and 6's real evidence. Lower, explicitly unscored confidence on deferring (3) -- this is a judgment call about appetite for open-ended third-party/Windows debugging, not evidence-driven either way. |
| **Actor** | Director (accept), alawas-thinking-pressure-test-decision (pressure test) |
| **Revisit trigger** | Read-only-only status goes stale silently if a future `codex exec`/Windows sandbox update fixes write support transparently -- nothing in this adapter would notice or re-test that on its own. Revisit either on a Codex CLI version bump, or the next time write-capable dispatch is actually needed (e.g. a genuine attempt to migrate `engineering-implement-bounded-change` or another execution-shaped skill through this adapter, which would immediately re-surface the same blocker and force the (a) investigation this decision deferred). |
| **Rationale** | (2) is a bounded, low-cost, unconditionally useful fix (accurate failure reporting matters regardless of the sandbox outcome). (1) matches what's actually verified working rather than what was hoped to work. (3) is explicitly NOT rejected -- deferred, because its cost is unknown and open-ended, and forcing it now would violate this Work Object's own tracer-bullet discipline of bounded, evidence-first steps. |
| **Edge cases noted** | If a future Codex CLI version silently fixes Windows sandbox write support, this decision's core assumption (read-only-only) goes stale with no automatic detection -- captured explicitly as the revisit trigger rather than left implicit. |

### Decision 8 — AgentDescriptor is in-code (Pydantic model), no declarative config file

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | `AgentDescriptor` (a Pydantic model: `name`, `type`, `capabilities`) is added to `runtime/agents.py`; `AgentResolver` continues to be constructed from a plain Python list of descriptors, not loaded from a config file. No `runtime/agents.yaml` or equivalent is built now. |
| **Alternatives considered** | Declarative YAML/JSON registry mirroring `adapters/*/overlay.yaml`'s pattern -- rejected as premature with only one working adapter (Codex, read-only) and one undesigned candidate (Copilot); nothing real to declare yet. |
| **Authorization** | Director accepted, chat 2026-08-25: "do recommendation." |
| **Confidence** | high -- directly consistent with Decision 2's own accepted rationale ("no scoring model," plainest mechanism first). |
| **Revisit trigger** | If a non-engineer or external process ever needs to add/remove available agents without touching Python, the config-file branch becomes worth reconsidering -- not before. |
| **Edge cases noted** | A config file can be added later without changing `AgentDescriptor`'s shape -- waiting doesn't foreclose branch B. |
| **Actor** | human |

### Decision 9 — CopilotAgentAdapter gets a real tracer-bullet dispatch, not a paper design [SUPERSEDED]

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | `CopilotAgentAdapter` will mirror `CodexAgentAdapter`'s shape (subprocess -> parse JSONL -> `AgentResult`), starting read-only-equivalent (via Copilot's per-tool `--deny-tool`/`--allow-tool` model, since no single sandbox-mode flag exists) plus `--disable-builtin-mcps`/`--disable-mcp-server`. Not designed in full here -- routes to a real tracer-bullet dispatch (mirroring Decisions 3-5's discipline) as the next specialist step, not authored on paper in this grilling session. |
| **Alternatives considered** | Designing the full adapter now, deferring the real dispatch test to implementation -- rejected: this Work Object already paid the cost once (Decision 3's first parser draft was wrong until tested against real Codex output) and Copilot's JSONL event schema is unverified against real output. |
| **Authorization** | Director accepted, chat 2026-08-25: "i accept." |
| **Confidence** | high -- directly grounded in this Work Object's own repeated lesson (don't trust an assumed event schema without a real dispatch). |
| **Revisit trigger** | If Copilot's per-tool permission model cannot cleanly express read-only behavior the way `--sandbox read-only` did for Codex, that itself becomes a new finding requiring its own decision. |
| **Actor** | human |
| **Superseded** | Director removed CopilotAgentAdapter from the plan, chat 2026-08-25: "remove copilotagentdapater in the plan." OpenCodeAgentAdapter (Decision 15) provides the cross-harness adapter path instead. |

### Decision 10 — Copilot's read-only path proven first; write-capability testing is a separate later decision; skill migration stays an open gap [SUPERSEDED]

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The upcoming `CopilotAgentAdapter` tracer bullet (Decision 9) tests read-only dispatch only, mirroring Codex's Decisions 3-5 sequence. Write-capability testing for Copilot is deferred as its own separate, later decision -- not folded into the same tracer bullet. `engineering-implement-bounded-change`'s actual migration remains explicitly `[gap]` -- no migration steps are decided or invented; it stays blocked until some adapter demonstrates real write capability. |
| **Alternatives considered** | Testing Copilot's write capability as part of the same upcoming tracer bullet -- rejected: conflates two separable risks (does dispatch/parsing work at all vs. can it write) into one test, making a failure ambiguous about which assumption broke. |
| **Authorization** | Director accepted, chat 2026-08-25: "i accept B." |
| **Confidence** | high -- mirrors the exact sequence (Decisions 3-5-6-7) that already produced clean, unambiguous evidence once. |
| **Revisit trigger** | Once Copilot's read-only path is proven, write-capability testing becomes its own next decision -- not automatic, still requires separate acceptance. |
| **Actor** | human |
| **Superseded** | Director removed CopilotAgentAdapter from the plan. Decision 16 (OpenCodeAgentAdapter write capability) already closed the write-capability gap this decision deferred. |

### Decision 11 — Design runtime/graph.py wiring now (director override), routes to design-tracer-bullet

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Design a graph node (e.g. `execute_specialist`) that would call `AgentResolver.resolve()` + an adapter's `run()` and feed `AgentResult` into graph state for routing -- despite no skill yet having completed a real dispatch through any adapter. This is a design commitment, not an implementation; the actual node spec routes to `alawas-design-design-tracer-bullet` as its own next step, not authored inline in this pressure test. |
| **Alternatives considered** | No wiring designed until a real skill dispatch exists (the recommended branch) -- overridden by director. |
| **Authorization** | Director explicit override, chat 2026-08-25: "accept B" -- rejecting the recommendation (wait for a real consumer) in favor of designing now. |
| **Confidence** | high on the recommendation that was overridden (mirrors two prior accepted "wait for two real cases" decisions this session); no confidence claimed on the override itself -- recorded plainly as a director choice, not evidence-driven agreement, same pattern as Decision 2's override. |
| **Revisit trigger** | If the resulting design, once a real skill dispatch actually exists, needs material revision to fit reality -- expected, given zero real consumers exist at design time. Not a failure of this decision, an accepted cost of designing early. |
| **Edge cases noted** | Designing wiring for a consumer that doesn't exist yet risks the same class of error Decision 3's first parser draft hit (wrong until tested against real behavior) -- except here there is no real behavior to test against yet, so the risk is structurally higher and unresolvable until a real dispatch exists. |
| **Actor** | human |

### Decision 12 — Write runtime/tests/test_agents.py using real captured output as fixtures

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A real test file, `runtime/tests/test_agents.py` (matching the repo's existing `runtime/tests/test_handoff_graph.py` convention), formalizes the manual verification already performed across Decisions 3-7 and 10: the clean "PONG" case, the blocked-on-failed-command case, the blocked-on-patch-rejected case, and MCP suppression. Fixtures use only already-captured real `codex exec --json` output from this session's actual dispatches, never hand-typed/invented mock output. Queued as a bounded implementation step, not authored inline in this decision. |
| **Alternatives considered** | Continue manual ad-hoc verification only (branch A) -- rejected: already caught one real regression (Decision 5) that a durable test would catch automatically in the future; nothing currently guards against a future edit silently breaking the blocked-classification or MCP-suppression logic. |
| **Authorization** | Director accepted, chat 2026-08-25: "accept B." |
| **Confidence** | high -- this formalizes already-proven manual checks rather than inventing new speculative test infrastructure; the fixture constraint (real captured output only) directly guards against calcifying a wrong assumption. |
| **Revisit trigger** | If maintaining fixtures as literal captured output becomes impractical (e.g. Codex's real output format changes upstream and fixtures go stale), the fixture strategy itself needs revisiting -- not a reason to switch to hand-typed mocks silently. |
| **Actor** | human |

### Decision 13 — Sequencing: graph-wiring design and test suite (closes grilling session) [REVISED]

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Of the items queued this session (runtime/graph.py wiring design -- Decision 11; test suite -- Decision 12), the graph-wiring design and test suite follow in either order. Copilot tracer bullet (Decisions 9-10) removed from sequencing per director instruction. Closes this grilling session. |
| **Authorization** | Director accepted, chat 2026-08-25: "i accept." Revised 2026-08-25: director removed CopilotAgentAdapter from plan. |
| **Confidence** | high -- same real-evidence-before-infrastructure ordering applied consistently across Decisions 2, 3. |
| **Revisit trigger** | If a third-party harness adapter is needed in the future, the Copilot path can be reopened. |
| **Actor** | human |

### Decision 14 — Revised Copilot read-only tracer bullet: execute through the actual VS Code Copilot + DeepSeek session, not the copilot CLI [SUPERSEDED]

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Execute the Copilot read-only tracer bullet through the actual GitHub Copilot-in-VS-Code runtime with a DeepSeek model (this session), not a `copilot` CLI subprocess adapter. Smallest slice: run `alawas-research-investigate-live-question` read-only on a trivial, harmless falsifiable question; observe (a) skill activation and governing principle, (b) each required capability maps to a real tool as classified, (c) `web_search` (manual-fallback) degrades per the adapter — asks for one source or manual lookup rather than fabricating, (d) output matches the skill's declared template, (e) zero `.work-studio` writes without explicit authority. Surfaced finding: `adapters/github-copilot/overlay.yaml` `model_tiers` resolve to claude-sonnet-4/claude-haiku, not the DeepSeek model actually running — to be reconciled. |
| **Authorization** | Director accepted the immediately preceding revised tracer-bullet recommendation, chat 2026-08-25: "accept." |
| **Confidence** | medium — the runtime behavior (activation, capability mapping, degradation, output shape, no-write) is exactly what the tracer observes; no such execution has yet been recorded through the real VS Code Copilot + DeepSeek runtime. |
| **Revisit trigger** | If the execution surfaces a capability classified native that actually blocks, or degradation that does not pause as declared, the github-copilot adapter classifications are wrong and must be revised before any write-capability testing (Decision 10). Also revisit if the model-tier mismatch (DeepSeek vs claude-sonnet/haiku) materially affects which skills activate correctly. |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design) |
| **Superseded** | Director removed CopilotAgentAdapter from the plan. The tracer bullet was executed and verified (evidence in ledger) but the adapter path is no longer pursued. |

### Decision 15 — OpenCodeAgentAdapter tracer bullet: zero model-tier binding, opencode run --format json

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add `OpenCodeAgentAdapter` to `runtime/agents.py`, mirroring `CodexAgentAdapter`'s shape. Uses `opencode run --format json --auto` for non-interactive subprocess dispatch. Zero model-tier binding — model passed at invocation time via `--model`, never hardcoded (unlike `adapters/github-copilot/overlay.yaml`'s `model_tiers` which resolve to claude-sonnet/haiku). Replaces the previously-proposed DeepSeek adapter target (WO 2026-08-21-011) with OpenCode, which supports 75+ providers through Models.dev. Two real dispatches made: PONG test (status=completed) and nonexistent-file test (status=blocked via tool_use failure detection). |
| **Authorization** | Director accepted the tracer-bullet recommendation, chat 2026-08-25: "accept this bullet." |
| **Confidence** | high — two real dispatches verified the dispatch-and-parse path end-to-end. JSON event schema (`step_start`/`tool_use`/`text`/`step_finish`) differs from Codex's (`item.completed`/`agent_message`) but maps cleanly to `AgentResult`. Windows `.CMD` wrapper handled via `create_subprocess_shell`. |
| **Revisit trigger** | If `opencode run` requires interactive auth in a different environment, or if a future real dispatch needs capabilities beyond `retrieve`/`inspect_code`/`hypothesize`, the adapter needs revision. Also revisit if the `--auto` flag proves too permissive for governed dispatch (may need scoped `--permissions` via agent creation). |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design), alawas-engineering-implement-bounded-change (implementation) |

### Decision 16 — OpenCodeAgentAdapter write capability verified; closes Decision 10's open gap

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Test whether `opencode run --format json --auto` can write files through the OpenCodeAgentAdapter. One real dispatch: create `output.txt` in scratch directory containing `tracer-bullet-write-ok`. Independent verification: file exists with correct content. Regression check: PONG test still returns `status=completed`. This closes Decision 10's explicit gap ("skill migration stays blocked until some adapter demonstrates real write capability"). |
| **Authorization** | Director accepted the tracer-bullet recommendation, chat 2026-08-25: "accept this bullet." |
| **Confidence** | high — file independently verified with correct content. Unlike CodexAgentAdapter (Decision 6 failed due to Windows sandbox), OpenCode's `--auto` flag permits writes without sandbox restrictions. Regression check confirms read-only path unaffected. |
| **Revisit trigger** | If `--auto` proves too permissive for governed dispatch (allows unintended mutations), the adapter may need scoped `--permissions` via agent creation. Also revisit if a real skill migration surfaces write patterns that fail differently from this tracer. |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design), alawas-engineering-implement-bounded-change (implementation) |

### Decision 17 — Orchestrate agent promoted as default entry point across all three harnesses

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Promote the orchestrate agent as the default entry point for OpenCode, Claude Code, and Codex. Agent configs created at `.opencode/agents/orchestrate.md` (mode: primary), `.claude/agents/orchestrate.md` (tools: Read, Grep, Glob, Task, Skill), and `.codex/agents/orchestrate.toml` (sandbox_mode: read-only). All three share the same classification rules: Work Object references → conduct-work-object, direct skill requests → requested skill, general questions → inquire-system, ambiguous → ask one clarifying question. Three message types verified through real OpenCode dispatch: (1) WO reference — correct, (2) direct skill request — correct, (3) general question — correct. |
| **Authorization** | Director accepted, chat 2026-08-25: "promote now as default entry point for opencode, claude code and codex." |
| **Confidence** | high — three message types verified through real dispatch. Agent configs mirror the proven blender-operator pattern (canonical body transcribed to three harness formats). |
| **Revisit trigger** | If the orchestrate agent misroutes a real request, the classification rules need revision. Also revisit if a fourth harness is added (e.g., Copilot). |
| **Actor** | Director (accept), alawas-design-design-tracer-bullet (design), alawas-engineering-implement-bounded-change (implementation) |

### Decision 18 — Graph orchestration: deterministic routing, not LLM-based

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The graph dispatches to agents via deterministic code (read WO state → `AgentResolver.resolve()` → `adapter.run()`), not LLM-based classification. The orchestrate agent stays at the entry point (OpenCode/Claude Code/Codex) where ambiguity lives. The graph's job is execution, not classification. Extends Phase 6's existing `derive_proposal()` pattern — code already routes from WO state to skill names; this extends it to route from WO state to agent dispatch. |
| **Alternatives considered** | LLM-based orchestration (invoke orchestrate agent as subagent) — rejected: adds LLM cost/latency per dispatch, non-deterministic routing makes debugging harder, checkpoint integration for subagent calls untested. Hybrid (deterministic for clear cases, LLM for ambiguous) — rejected: over-engineering before proving one path works, violates tracer-bullet discipline. |
| **Authorization** | Director accepted, chat 2026-08-25: "accept branch a." |
| **Confidence** | medium-high — grounded in Phase 6's existing deterministic routing pattern. Untested with real agent dispatch through the graph (Decision 11's accepted cost of designing early). |
| **Revisit trigger** | If the graph ever needs to handle requests not cleanly derivable from WO state (e.g., "the WO says X but evidence suggests Y"), LLM-based classification may be needed mid-pipeline. Not this decision's scope. |
| **Actor** | Director (accept), alawas-thinking-pressure-test-decision (pressure test) |

### Decision 19 — execute_specialist node implemented in runtime/graph.py

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add `execute_specialist` node to Phase 6 graph. Reads `HandoffEnvelope` from dispatch, resolves adapter via `AgentResolver`, calls `adapter.run()`, stores `AgentResult` in state. Wired after dispatch, before branch_a/branch_b. Graph flow: dispatch → execute_specialist → branch_a/branch_b → join → direction_gate. Imports from `runtime.agents`: `AgentRequest`, `AgentResolver`, `CodexAgentAdapter`, `OpenCodeAgentAdapter`, `codex_available`, `opencode_available`. `Phase6State` extended with `agent_result: dict`. |
| **Authorization** | Director accepted, chat 2026-08-25: "(1) implement execute_specialist node in runtime/graph.py." |
| **Confidence** | high — node works when called directly (PONG test passed). Graph builds successfully with node wired in. Graph hangs at `direction_gate` interrupt (expected — waits for human approval). |
| **Revisit trigger** | If a real skill dispatch through the graph fails differently from direct adapter calls, the node needs revision. Also revisit if the `asyncio.run()` call inside the node causes issues in async contexts. |
| **Actor** | Director (accept), alawas-engineering-implement-bounded-change (implementation) |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | alawas-thinking-inquire-system session investigation, 2026-08-25 | Investigation via alawas-thinking-inquire-system (2026-08-25) established: no .claude/agents/ exists at project or user level; 8 of 45 alawas-* skills are execution-shaped with distinct restricted-tool-allowlist needs (candidates: implement-bounded-change, verify-release-evidence, deploy-with-recovery, diagnose-production-incident, production-operate-blender, apply-design-direction, plus research-produce-report and pressure-test-decision for subagent_spawn parallelism only). alawas-production-operate-blender identified as strongest pilot (single external system, GPU-slot isolation already designed, non-overlapping tool needs). Existing skill-adapter pattern (tools/generate-adapters.py -> adapters/{claude-code,codex,github-copilot}/) proven at skill level but not agent-type level; docs/design/platform-adapters-component-plan.md Decision 84 already flags subagent_spawn/subagent_isolation as asymmetric across platform overlays. Web research (dated 2026-08-25) confirmed three harnesses have convergent-but-distinct native subagent formats: Claude Code .claude/agents/*.md (YAML frontmatter + Markdown body), Codex CLI .codex/agents/*.toml (developer_instructions field), GitHub Copilot Markdown+YAML frontmatter with tools: allowlist and coordinator agents: field. LM Studio/Bionic checked and excluded -- no config-file subagent mechanism in official docs. |
| [system] | canonical/transcribed blender-operator agent files, verified in 2026-08-25 tracer | Canonical blender-operator agent-type body and three harness transcriptions were authored at user-level agent paths and the instruction bodies were diffed byte-identical after correcting the TOML transcription slip; this supports the first three checked success-evidence items but does not prove native harness dispatch. |
| [system] | Codex multi_agent_v1 subagent 01a03a14-0aa5-79f3-87f3-3df4ccdf6e18 plus queue files in %TEMP%\ws-blender-live-queue-_waetl3g | Live blender-operator dispatch ran as Codex subagent Pascal with the alawas-production-operate-blender contract supplied explicitly: headless Blender 5.2 launched via repository addon.py, command CMD-080dfc07-0001 executed op scene.get_objects through the bounded file queue, result status ok returned objects Camera, Cube, Light. No repo files edited; no render/import/texture, no mutation, no GPU claim needed. Caveat: this exercises the agent contract through the available Codex subagent runner, not native loading of C:/Users/Andre/.codex/agents/blender-operator.toml. |
| [system] | runtime/agents.py CodexAgentAdapter, two real codex exec calls made 2026-08-25 from this session against an isolated scratch directory (C:\Users\Andre\AppData\Local\Temp\claude\...\scratchpad\codex-tracer-bullet, not this repo) | Real `codex exec --json` dispatch verified end to end. Test 1 (task requiring file read): codex could not read the file because this environment's Windows sandbox helper (codex-windows-sandbox-setup.exe) is not found, so any `--sandbox read-only`-constrained shell command fails; codex returned an honest failure message, which the adapter mapped to status=completed (technically accurate -- the run finished -- but semantically misleading, since the underlying task was not achieved). Test 2 (task requiring no shell command, "reply PONG"): status=completed, summary="PONG" -- clean confirmation the dispatch-and-parse path works when not blocked by the sandbox gap. Parser required one fix: real codex exec --json emits `{"type":"item.completed","item":{"type":"agent_message","text":...}}`, not the `{"msg":{...}}` shape assumed from the reference proposal. |
| [gap] | AgentResult status vocabulary (completed/blocked/needs_approval/failed) | The fixed vocabulary cannot currently distinguish "the adapter's underlying process completed and returned an honest answer" from "the requested task was not actually accomplished." Test 1 above is a live example: technically completed, substantively unresolved. Needs resolving before any real (non-tracer-bullet) task is dispatched through CodexAgentAdapter. |
| [gap] | `--sandbox read-only` (codex exec flag) plus `node_repl` MCP server (enabled in this Codex installation's config) | `--sandbox read-only` constrains only model-generated shell commands, not MCP tool calls. An enabled, unsandboxed `node_repl` MCP server could let a dispatched Codex process execute arbitrary Node.js code and touch the filesystem outside the intended scratch-directory boundary, regardless of the sandbox flag. Investigated as a possible explanation for an unexpected Work Object write (see next entry) and ruled out as the actual cause this time, but the capability gap itself is real and unresolved for any future real dispatch. |
| [system] | Codex Desktop session 01a03a12-b197-79d1-b74b-e91b4ccb2cdc, rollout log C:\Users\Andre\.codex\sessions\2026\08\25\rollout-2026-08-25T10-58-18-01a03a12-b197-79d1-b74b-e91b4ccb2cdc.jsonl | A separate, independent Codex Desktop/VSCode session (originator: "Codex Desktop", source: "vscode", thread_source: "user", started 17:58:25 -- before this session's own codex exec tests) was running concurrently against this same Work Studio, with its own memory of the repo. It made the History entry timestamped 2026-08-25T18:06:01Z (actor "codex") via the sanctioned `uv run python -m tools.ws append-history` CLI path -- not an unauthorized bypass, and not caused by this session's tracer-bullet dispatch. Surfaces a genuine open question: this Work Object was concurrently edited by two independent sessions, which the studio's single-conductor session-boundary model (governance-conduct-work-object) does not yet account for. |
| [system] | Copilot read-only tracer bullet execution (Decision 14), actual VS Code Copilot + DeepSeek session, 2026-08-25 | Tracer executed: ran alawas-research-investigate-live-question read-only through the actual VS Code Copilot + DeepSeek session. Checkpoints: (a) activation held - skill framed a falsifiable question and routed honestly, not persuasively; (b) capability mappings held - file_read/content_search native and used, web_fetch native but not triggered (no known attributable URL pre-named), user_confirmation not needed, structured_output produced; (c) web_search manual-fallback degraded per the adapter - paused and requested one source or manual lookup rather than fabricating when external source discovery was needed; (d) output matched the skill's declared template; (e) zero .work-studio writes during the run. Findings: github-copilot model_tiers (claude-sonnet-4/claude-haiku) do not match the DeepSeek model running in this session; this mismatch is ALREADY KNOWN to WO 2026-08-21-011 (which recorded the hardcoded-claude finding and proposed a deepseek adapter target with zero model-tier binding like codex). Overlap surfaced: WO 2026-08-25-001 and WO 2026-08-21-011 both work the Copilot/DeepSeek adapter question and are not yet reconciled. |
| [system] | runtime/agents.py OpenCodeAgentAdapter, two real opencode run --format json calls made 2026-08-25 from this session against C:\Users\Andre\AppData\Local\Temp\opencode | Real `opencode run --format json --auto` dispatch verified end to end. Test 1 (PONG): status=completed, summary="PONG" — clean confirmation the dispatch-and-parse path works. Test 2 (nonexistent file read): status=blocked — tool_use event with state.status != completed correctly detected and mapped to blocked. JSON event schema differs from Codex: OpenCode emits `step_start`/`tool_use`/`text`/`step_finish` events (not `item.completed`/`agent_message`). Windows `.CMD` wrapper required `create_subprocess_shell` instead of `create_subprocess_exec`. Zero model-tier binding confirmed: model passed via `--model` flag at invocation time, never hardcoded. `opencode_available()` helper added alongside existing `codex_available()`. |
| [decision] | conductor, 2026-08-25 | WO 2026-08-21-011 closed. DeepSeek-specific adapter path superseded by this WO's Decision 15 (OpenCodeAgentAdapter). The broader MCP agency-mode question remains open as a potential successor inquiry. |
| [system] | runtime/agents.py OpenCodeAgentAdapter write-capability tracer (Decision 16), 2026-08-25 | Real `opencode run --format json --auto` write dispatch verified. Task: create output.txt containing "tracer-bullet-write-ok" in C:\Users\Andre\AppData\Local\Temp\opencode. Adapter returned status=completed. Independent verification: file exists with correct content. Regression check: PONG test still returns status=completed. Unlike CodexAgentAdapter (Decision 6 failed — Windows sandbox rejected writes), OpenCode's --auto flag permits writes without sandbox restrictions. Decision 10's open gap closed: an adapter now demonstrates real write capability. |
| [system] | Orchestrate agent promotion (Decision 17), 2026-08-25 | Three message types verified through real OpenCode dispatch: (1) WO reference "2026-08-25-001" — correctly read WO, reported status, offered routing options; (2) direct skill request "design a tracer bullet for the CopilotAgentAdapter" — correctly identified skill, loaded it, began reading WO; (3) general question "how does the work studio handle concurrent edits" — correctly loaded inquire-system, grounded answer in repository. Agent configs created at `.opencode/agents/orchestrate.md` (mode: primary), `.claude/agents/orchestrate.md` (tools: Read, Grep, Glob, Task, Skill), `.codex/agents/orchestrate.toml` (sandbox_mode: read-only). All three share identical classification rules. |
| [system] | execute_specialist node implementation (Decision 19), 2026-08-25 | Node added to runtime/graph.py. Reads HandoffEnvelope from dispatch, resolves adapter via AgentResolver, calls adapter.run(), stores AgentResult in state. Wired after dispatch, before branch_a/branch_b. Graph builds successfully with node wired in (verified: nodes = [__start__, dispatch, execute_specialist, branch_a, branch_b, join, direction_gate, __end__]). Node works when called directly (PONG test: status=completed, summary="PONG"). Graph hangs at direction_gate interrupt (expected — waits for human approval). Imports from runtime.agents: AgentRequest, AgentResolver, CodexAgentAdapter, OpenCodeAgentAdapter, codex_available, opencode_available. Phase6State extended with agent_result: dict. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Workflow Candidates

<!-- Proposed workflow rules with evidence. See alawas-governance-maintain-working-method. -->

### Candidate WFC-2026-08-25-001-A — Optimistic concurrency sufficiency for cross-harness concurrent Work Object writes

| Field | Value |
|-------|-------|
| **Identity** | WFC-2026-08-25-001-A |
| **Proposed rule** | The conductor's optimistic-concurrency check (`--expect-updated` on every `ws` mutation) is sufficient protection when two independent sessions/harnesses write to the same Work Object concurrently, without requiring an explicit lock, session registry, or coordination mechanism. |
| **Scope** | Work Object mutations via the sanctioned `tools.ws` CLI only; excludes any future direct-file-write path. Bears on `governance-conduct-work-object`'s Session-boundary rule, whose own text already names "genuinely concurrent editors on the same Work Object" as an unaddressed future case. |
| **Origin references** | Work Object `2026-08-25-001` History (entries 2026-08-25T17:50:06Z through 18:15:00Z) and evidence-ledger entry for Codex Desktop session `01a03a12-b197-79d1-b74b-e91b4ccb2cdc` (real concurrent write incident, no data loss). |
| **Evidence and lifecycle events** | 2026-08-25 — [system] Two independent sessions (this Claude Code session; a separate Codex Desktop/VSCode session) wrote to `2026-08-25-001` concurrently via `ws append-history`/`ws append-evidence`; both writes landed, no corruption, no lost update observed. [gap] No contrary-evidence review performed yet -- whether a near-miss or actual `--expect-updated` rejection has occurred elsewhere in this repo's history is unknown, not ruled out. |
| **Bounded test references** | None yet. Today's incident was observed, not a predeclared bounded test -- no hypothesis, scope, or signal was set in advance. Recommended next bounded test: deliberately run two concurrent `ws` mutations against a disposable test Work Object with a predeclared hypothesis (e.g. "the second writer's `--expect-updated` mismatch is caught and reported, never silently overwritten"). |
| **Timestamps** | Created: 2026-08-25T18:15:00Z (approx, at recording) |
| **Personal summary** | none |
| **Status** | active |
| **Relationships** | none |

## Next move

Deliverable 1: `.work-studio/deliverables/2026-08-25-001-agent-execution-current-state-reconstruction.md` — repository-grounded current-state reconstruction (Section A).

Deliverable 2: `.work-studio/deliverables/2026-08-25-001-agent-execution-architecture-plan.md` — the full B-M architecture plan, produced after a completed grilling session (Decisions 8-13) made enough of the underlying architecture decided that every section could be either synthesized from a cited Decision or explicitly marked as an open gap, never invented. Recommended next tracer per the plan: real Copilot read-only dispatch (Decision 13).

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T17:50:06Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director requested durable record of cross-harness agent-type investigation before proceeding to design-tracer-bullet; overlapping active WO 2026-08-24-014 (production-operate-blender skill build) already reached verify state and is the source of the pilot candidate -- this WO is scoped narrowly to the agent-TYPE adapter layer, not the skill itself.
### 2026-08-25T17:50:17Z — Transition explore -> design

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Riskiest assumption already identified during pre-WO investigation (does the skill-adapter generation pattern extend to agent-type definitions) and pilot candidate already selected (production-operate-blender). No further divergent exploration needed before design-tracer-bullet.
### 2026-08-25T17:53:30Z — Design accepted: hand-author canonical Blender-operator agent-type body + three format transcriptions

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted the tracer-bullet recommendation. Decision 1 recorded. Routing to alawas-engineering-implement-bounded-change to author the canonical body and three transcriptions per the recorded scope, authorization, non-goals, and rollback.
### 2026-08-25T17:55:57Z — Tracer bullet implemented and verified: canonical Blender-operator agent-type body reused verbatim across three harness formats

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Four files authored outside repo (~/.claude/agent-types/blender-operator.md canonical source; ~/.claude/agents/blender-operator.md, ~/.codex/agents/blender-operator.toml, ~/.copilot/agents/blender-operator.md transcriptions). Diff of instruction-body content across the three transcriptions found byte-identical match after correcting one authoring slip (dropped Markdown backticks/arrow character when first writing the TOML string -- not a real TOML syntax constraint). Riskiest assumption (Decision 1) confirmed: pass. Gap: none of the four files installed, registered, or test-dispatched through their real harness -- Codex and GitHub Copilot are not available in this environment, so 'valid native-format file' is the ceiling of what was verified, not confirmed live invocation. Unrelated pre-existing dirty working tree in andrelawas-work-studio (.work-studio/* modifications) preserved untouched -- no overlap with this change.
### 2026-08-25T18:00:42Z — Decision 2 recorded: build runtime AgentRequest/AgentAdapter/AgentResolver dispatch layer now (director override)

- **State:** design
- **Status:** active
- **Actor:** human
- **Rationale:** Director overrode the pressure test's medium-high-confidence recommendation to wait; chose to build the four-piece dispatch layer (AgentRequest, AgentResult, AgentAdapter protocol, AgentResolver) plus one CodexAgentAdapter plus one skill migration (engineering-implement-bounded-change) now, scoped per the original external proposal. Recorded as explicit override, not evidence-driven agreement -- revisit trigger names the dead-abstraction edge case explicitly.
### 2026-08-25T18:02:26Z — Design accepted: build runtime/agents.py (AgentRequest/AgentResult/AgentAdapter/AgentResolver/CodexAgentAdapter) + one real codex exec call as tracer bullet

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted. Decision 3 recorded. Routing to alawas-engineering-implement-bounded-change to write runtime/agents.py and make the real codex exec call per the recorded scope, authorization, non-goals, and rollback.
### 2026-08-25T18:06:01Z — Recorded live blender-operator dispatch evidence

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** Conductor recorded the just-run Codex subagent dispatch evidence for the blender-operator pilot and preserved the caveat that native .codex/agents TOML autoload remains unverified; next action remains the accepted runtime/agents.py tracer bullet.
### 2026-08-25T18:10:17Z — Decision 3 verified pass: runtime/agents.py CodexAgentAdapter dispatch-and-parse path confirmed real; two gaps and one concurrent-session finding recorded

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Two real codex exec calls made against an isolated scratch directory. Dispatch-and-parse path works (PONG test passed cleanly). Parser bug fixed (real event schema differs from reference proposal's assumed shape). Two gaps surfaced: (1) AgentResult's fixed status vocabulary cannot distinguish technical completion from task failure -- a file-read test failed honestly due to a missing Windows sandbox helper in this environment, but mapped to status=completed; (2) node_repl MCP server, enabled in this Codex install, is not constrained by --sandbox read-only, a real gap for future dispatch even though it was NOT the cause of an earlier concern. That earlier concern (an unexplained History write, actor codex, at 18:06:01) was investigated via Codex session rollout logs and resolved: it came from a separate, independent, concurrent Codex Desktop session already working the blender-operator pilot directly, using the sanctioned ws CLI write path -- not a breach. Surfaces a new governance finding: this WO was concurrently edited by two independent sessions, which the conductor's single-conductor session-boundary model does not yet account for.
### 2026-08-25T18:12:13Z — Decision 4 recorded and implemented: AgentResult status-vocabulary gap fixed by reusing 'blocked' for command_execution failures

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** runtime/agents.py CodexAgentAdapter.run() now checks for any command_execution item with status=failed and maps to status=blocked instead of completed when the underlying task was prevented from finishing. Verified against both real cases already on record: the file-read test (missing sandbox helper) now correctly returns blocked; the PONG test still correctly returns completed. No AgentResult schema change.
### 2026-08-25T18:15:00Z — Decision 5 recorded and implemented: node_repl/MCP sandboxing gap closed with -c mcp_servers={} after --ignore-user-config alone proved insufficient

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Tested --ignore-user-config alone first (per accepted design); verification step itself found it insufficient -- a live rmcp MCP connection attempt to mcp.cloudflare.com still occurred. Added explicit -c mcp_servers={} override; confirmed via direct codex exec and through the adapter that zero MCP connection attempts occur with both flags present. Comment added in runtime/agents.py explaining why both flags are needed. One unexplained adjacent observation recorded honestly: the same re-verification run's file-read test unexpectedly succeeded (previously failed due to a missing Windows sandbox helper) -- not claimed as caused by this fix, flagged as unconfirmed.
### 2026-08-25T18:17:02Z — Workflow Candidate WFC-2026-08-25-001-A recorded: optimistic-concurrency sufficiency for cross-harness concurrent Work Object writes

- **State:** design
- **Status:** active
- **Actor:** alawas-governance-maintain-working-method
- **Rationale:** Director accepted recording this candidate as retain, not promote -- today's real concurrent-write incident (this session plus an independent Codex Desktop session, both writing via the sanctioned ws CLI, no data loss) is real evidence but not a predeclared bounded test, so it cannot support promotion per this skill's own evidence rules. Candidate recorded with status=active, no bounded test yet, recommended next move is a deliberate predeclared concurrency test rather than waiting for another accidental real-world collision.
### 2026-08-25T18:19:25Z — Deliverable produced: current-state reconstruction (report-type, Section A only)

- **State:** design
- **Status:** active
- **Actor:** alawas-research-produce-report
- **Rationale:** Director requested a 17-section architecture review and implementation plan. Classified as mixing report-type (Section A, current-state reconstruction -- investigable, falsifiable) with plan-type authoring of unaccepted new architecture (Sections B-M -- new contracts, gaps, registry design, runtime integration, migration steps, testing plan, implementation sequence). Per this skill's own boundary, a plan-type deliverable may only synthesize already-accepted Decisions, never author new architecture. Produced Section A only, grounded entirely in this session's real file reads (runtime/graph.py grep, runtime/handoff.py, runtime/agents.py, skills/core structure, adapters/ generation mechanism, WORK-OBJECT.md, ADR 0025/0015) and this Work Object's own accepted Decisions 1-5. Declined Sections B-M explicitly rather than silently authoring speculative architecture as if decided.
### 2026-08-25T18:23:39Z — Design accepted: write+verify tracer bullet for CodexAgentAdapter (Decision 6)

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted. Decision 6 recorded. Routing to alawas-engineering-implement-bounded-change to switch CodexAgentAdapter to workspace-write sandbox mode scoped to the existing scratch directory, add modify_code capability, dispatch the trivial write task, and independently verify the result.
### 2026-08-25T18:27:53Z — Decision 6 FAILED: write-mode dispatch through CodexAgentAdapter does not work in this environment; second, narrower status-vocabulary gap found

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** runtime/agents.py updated: capabilities now includes modify_code, sandbox flag changed to workspace-write (both retained -- correct code, harmless). Real dispatch made: Codex's file-patch tool rejected the write as blocked by a read-only sandbox despite workspace-write being requested; independently verified output.txt was never created. Two findings: (1) environment -- this is the second distinct subsystem (after Decision 3's missing codex-windows-sandbox-setup.exe helper for shell commands) where Windows sandbox enforcement does not behave as requested; (2) adapter -- Decision 4's blocked-classification fix only inspects command_execution items; a rejected internal patch-tool call produces no such item (it surfaces as a Rust-level error log line instead), so this failure class still silently returns status=completed. Manual diagnostic codex exec calls outside the adapter (testing -c approval_policy="never") did not resolve it and separately, one of those manual calls regressed Decision 5's mcp_servers={} fix (a live MCP connection attempt reappeared) -- confirming this Codex install's config-loading behavior is fragile/inconsistent across invocations, not fully understood. No scope expansion: only the two authorized lines in runtime/agents.py were changed; no repository files touched; no approval_policy override was added to the adapter itself.
### 2026-08-25T18:29:35Z — Decision 7 recorded: CodexAgentAdapter reverted to read-only-only, blocked-classification broadened, sandbox investigation deferred

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Director accepted the pressure test's recommendation: (c) fix the classification gap unconditionally, (b) hold at read-only-only as the working assumption, (a) defer the Windows sandbox investigation as optional future work rather than deciding it today. Routing to alawas-engineering-implement-bounded-change to revert the write-mode code change from Decision 6 and implement the broadened blocked-classification fix.
### 2026-08-25T18:33:06Z — Decision 7 verified: CodexAgentAdapter reverted to read-only-only, blocked-classification broadened and confirmed against a real re-run of Decision 6's failing task

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** runtime/agents.py: capabilities reverted to {retrieve, inspect_code, hypothesize}; sandbox flag reverted to read-only; stderr_text now checked for 'error=patch rejected' and treated as a failed-command signal alongside the existing command_execution check. Re-ran Decision 6's exact task against the reverted adapter: reproduced the same real failure, independently confirmed output.txt still does not exist, and status now correctly returns blocked instead of completed. Regression-checked the clean PONG case -- unaffected. No repository files touched; only runtime/agents.py changed; pre-existing unrelated changes (handoff.py, tts_takes/) preserved untouched.
### 2026-08-25T18:34:06Z — Evidence correction: Copilot CLI is actually installed and callable, contradicting the earlier 'unavailable' claim

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director asked to pick up the Copilot-untested item. Direct check (which copilot, copilot --version, copilot --help) found copilot CLI 1.0.65 installed and callable, with a documented non-interactive -p mode and explicit --disable-builtin-mcps/--disable-mcp-server flags. This contradicts the 'unavailable in this environment' claim recorded in this WO's original evidence ledger entry (from the pre-WO alawas-thinking-inquire-system investigation) and in the success-evidence checklist. Corrected the checklist entry to state the correction plainly rather than silently updating the earlier claim.
### 2026-08-25T18:40:28Z — Decision 8 recorded: AgentDescriptor is in-code, no config file (grilling session, branch 1 of continuous plan-building session)

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Director accepted the recommendation as part of a continuous grilling session working toward the full B-M architecture plan. Consistent with Decision 2's existing bias toward the plainest mechanism.
### 2026-08-25T18:41:03Z — Decision 9 recorded: CopilotAgentAdapter gets a real tracer-bullet dispatch, not a paper design (grilling session, branch 2)

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Continuous grilling session toward the full B-M architecture plan. Directly consistent with Decisions 3-5's lesson: don't design an adapter's parser against an assumed event schema without a real dispatch.
### 2026-08-25T18:41:57Z — Decision 10 recorded: Copilot read-only proven first, write-capability separate, skill migration stays an open gap (grilling session, branch 3)

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Continuous grilling session. Mirrors the exact Decisions 3-5-6-7 sequence that already produced clean evidence once. engineering-implement-bounded-change's migration remains an honest gap, not invented steps.
### 2026-08-25T18:43:42Z — Decision 11 recorded: design runtime/graph.py wiring now, director override, queued for design-tracer-bullet (grilling session, branch 4)

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Director overrode the recommendation to wait for a real consumer, choosing to design the execute_specialist node now. Recorded as override, not evidence-driven agreement, mirroring Decision 2's pattern. Actual node spec deferred to alawas-design-design-tracer-bullet, not authored in this pressure test.
### 2026-08-25T18:45:07Z — Decision 12 recorded: write runtime/tests/test_agents.py using real captured output as fixtures (grilling session, branch 5)

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Continuous grilling session. Formalizes already-proven manual verification from Decisions 3-7/10 as durable tests, guarding against silent regression (already happened once, Decision 5). Fixture constraint: real captured output only, never hand-typed mocks.
### 2026-08-25T18:49:05Z — Decision 13 recorded: sequencing set (Copilot tracer bullet first), grilling session closed

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-pressure-test-decision
- **Rationale:** Continuous grilling session complete. Six branches walked and decided (Decisions 8-13): AgentDescriptor shape, second-adapter approach, skill-migration honesty, runtime-wiring override, test-suite approach, and final sequencing. The full B-M architecture plan can now be assembled honestly from Decisions 1-13 plus the current-state reconstruction deliverable, with every section either grounded in a real accepted Decision or explicitly marked as an open gap -- no invented architecture.
### 2026-08-25T18:51:20Z — Deliverable 2 produced: full B-M architecture plan, synthesized from Decisions 1-13

- **State:** design
- **Status:** active
- **Actor:** alawas-research-produce-report
- **Rationale:** Now legitimate synthesis rather than premature authoring: the completed grilling session (Decisions 8-13) plus pre-existing Decisions 1-7 and the Section A deliverable together cover Sections B, D, H, L fully; C and K partially (backward-looking honestly, forward speculation avoided); E, F, G, I, J, M each state their governing Decision precisely and name what remains unbuilt rather than inventing it. Read runtime/agents.py directly for Sections D and H so contract/adapter descriptions match the actual current code, not chat-remembered approximations.
### 2026-08-25T21:43:44Z — Routed to design: Copilot read-only tracer bullet design dispatched to alawas-design-design-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director instructed route to design. WO 2026-08-25-001 already in design state; executing the recorded next_action by dispatching the Copilot read-only tracer bullet design (Decisions 9, 10, 13) to alawas-design-design-tracer-bullet, mirroring Decisions 3-5 real-evidence-first discipline. Next action now names the design deliverable in the specialist's hands.
### 2026-08-25T21:47:44Z — Decision 14 recorded: revised Copilot read-only tracer bullet accepted - actual VS Code Copilot + DeepSeek session, not copilot CLI

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted the revised tracer-bullet recommendation (Decision 14). Riskiest assumption: a governed read-only skill executed through the actual VS Code Copilot + DeepSeek runtime behaves per the github-copilot adapter's declared capability mappings, including manual-fallback degradation and zero unauthorized writes. Smallest slice: run alawas-research-investigate-live-question read-only through this real session; observe activation, capability mapping, web_search degradation, output shape, no-write. Surfaced mismatch: github-copilot model_tiers resolve to claude-sonnet/haiku, not DeepSeek. Routing to alawas-engineering-implement-bounded-change to execute the tracer; this design does not implement it.
### 2026-08-25T21:51:45Z — Copilot read-only tracer bullet executed and verified through the actual VS Code Copilot + DeepSeek session (Decision 14)

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Dispatched the accepted read-only tracer through this actual session (not the copilot CLI). All five checkpoints held: activation, capability mappings, web_search manual-fallback degradation (paused and requested one source/manual lookup instead of fabricating), declared output shape, and zero .work-studio writes during the run. Riskiest assumption confirmed: a governed read-only skill executes through the real VS Code Copilot + DeepSeek runtime per the github-copilot adapter's declared mappings. Verified result routed to the conductor with implementation evidence. Findings for the director: (1) github-copilot model_tiers resolve to claude-sonnet-4/claude-haiku but the session runs DeepSeek - mismatch is ALREADY KNOWN to WO 2026-08-21-011, which proposed a deepseek adapter target with zero model-tier binding like codex; (2) write-capability testing remains an open gap (Decision 10).
### 2026-08-25T22:10:00Z — Decision 15 recorded: OpenCodeAgentAdapter tracer bullet accepted — replaces DeepSeek with OpenCode, zero model-tier binding

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director pivoted from the previously-proposed DeepSeek adapter target (WO 2026-08-21-011) to OpenCode as the adapter target. OpenCode supports 75+ providers through Models.dev with zero model-tier binding (model passed via --model at invocation time, never hardcoded). Tracer bullet designed: add OpenCodeAgentAdapter to runtime/agents.py mirroring CodexAgentAdapter's shape, using `opencode run --format json --auto` for subprocess dispatch.
### 2026-08-25T22:15:00Z — Decision 15 verified: OpenCodeAgentAdapter dispatch-and-parse path confirmed real; two dispatches passed

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Two real `opencode run --format json --auto` calls made against C:\Users\Andre\AppData\Local\Temp\opencode. Test 1 (PONG): status=completed, summary="PONG" — clean confirmation. Test 2 (nonexistent file read): status=blocked — tool_use failure correctly detected. JSON event schema differs from Codex (OpenCode uses step_start/tool_use/text/step_finish, not item.completed/agent_message). Windows .CMD wrapper required create_subprocess_shell. opencode_available() helper added. Zero model-tier binding confirmed: model passed via --model flag, never hardcoded. This reconciles the model_tiers mismatch by making the adapter model-agnostic.
### 2026-08-25T22:49:02Z — WO 2026-08-21-011 reconciled and closed

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** DeepSeek-specific adapter path superseded by Decision 15 (OpenCodeAgentAdapter). Evidence appended. Three paths remain: (1) write-capability decision (Decision 10); (2) route to verify-release-evidence; (3) CopilotAgentAdapter tracer bullet (Decision 9/13).
### 2026-08-25T22:52:14Z — Decision 16 verified: OpenCodeAgentAdapter write capability confirmed

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Real write dispatch through opencode run --format json --auto created output.txt with correct content in scratch directory. Independent verification confirmed. Regression check: PONG test unaffected. Unlike CodexAgentAdapter (Decision 6 failed due to Windows sandbox), OpenCode's --auto flag permits writes. Decision 10's open gap closed: an adapter now demonstrates real write capability, unblocking skill migration.
### 2026-08-25T23:09:55Z — CopilotAgentAdapter removed from plan

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director removed CopilotAgentAdapter from the plan. Decisions 9, 10, 13, 14 marked as superseded. OpenCodeAgentAdapter (Decision 15) provides the cross-harness adapter path instead. Decision 16 already closed the write-capability gap that Decision 10 deferred.
### 2026-08-25T23:16:02Z — Decision 17: Orchestrate agent promoted as default entry point across all three harnesses

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Three message types verified through real OpenCode dispatch: WO reference, direct skill request, general question. Agent configs created for OpenCode (.opencode/agents/orchestrate.md, mode: primary), Claude Code (.claude/agents/orchestrate.md), and Codex (.codex/agents/orchestrate.toml). All three share identical classification rules.
### 2026-08-25T23:21:01Z — Decision 18: Graph orchestration uses deterministic routing, not LLM-based

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted Branch A after pressure test. Graph dispatches via deterministic code (WO state → AgentResolver.resolve() → adapter.run()). Orchestrate agent stays at entry point where ambiguity lives. Extends Phase 6's existing derive_proposal() pattern.
### 2026-08-25T23:35:52Z — Decision 19: execute_specialist node implemented in runtime/graph.py

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Node reads HandoffEnvelope from dispatch, resolves adapter via AgentResolver, calls adapter.run(), stores AgentResult in state. Wired after dispatch, before branch_a/branch_b. Graph builds successfully. Node works when called directly (PONG test passed). Graph hangs at direction_gate interrupt (expected).
