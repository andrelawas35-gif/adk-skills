# Agent execution current-state reconstruction

**Work Object:** `2026-08-25-001` — Cross-harness agent-type adapter for execution-shaped skills
**Deliverable type:** report (Section A of a larger director-requested architecture review; Sections B–M are explicitly out of scope for this deliverable — see note at the end)
**Produced:** 2026-08-25

This document answers one question only: *what does this repository's agent/skill/runtime architecture actually contain today, as opposed to what a proposal describes or implies?* Every claim below is `[system]` (a direct file/code observation) or `[decision]` (an accepted Work Object Decision), attributed to its source. Synthesis connecting these facts is marked `[inference]`.

---

## 1. Skills layer

`[system]` Skills live as plain `SKILL.md` files under `~/.claude/skills/` (installed/generated form) with a canonical source at `skills/core/<skill>/SKILL.md` in this repository. 45 skills use the `alawas-*` namespace, spanning business, design, engineering, governance, operations, production, research, and thinking domains.

`[system]` Every `SKILL.md` declares, in frontmatter: `name`, `description`, `default_tier`, `platform`. In body: Governing principle, Boundaries and non-goals, Inputs and preconditions, **Required capabilities** (a named list like `file_read`, `web_fetch`, `subagent_spawn`), Consequence and authority rules, Grilling entry/profile, Stage workflow, Evidence rules, Work Object updates, Routing and termination, Output template. Each also carries a generated "Platform Adapter" section with a **Required capability mappings** table (abstract capability → concrete platform tool → classification: native/manual-fallback/unsupported).

`[system]` `capabilities` here means *abstract tool-access primitives* (`file_read`, `terminal_run`, `subagent_spawn`, `web_search`, etc.) — not cognitive primitives (retrieve/perceive/compare/infer). A prior Work Object (`2026-08-22-002`, state `explore`, not yet decided) explicitly flagged this exact term collision between "tool-primitive capability" (load-bearing, used everywhere) and a proposed "cognitive-primitive capability" taxonomy — unresolved, not settled either way.

`[inference]` Of the 45 skills, this session's earlier investigation (via a dedicated Explore subagent reading all 45 `SKILL.md` bodies) classified ~37 as pure reasoning-lens skills (no distinct execution toolset) and named 8 as execution-shaped with a genuinely restricted, non-overlapping tool need: `engineering-implement-bounded-change`, `engineering-verify-release-evidence`, `operations-deploy-with-recovery`, `operations-diagnose-production-incident`, `production-operate-blender`, `design-apply-design-direction` (six with a distinct restricted allowlist), plus `research-produce-report` and `thinking-pressure-test-decision` (two using `subagent_spawn` for parallelism only, not a distinct persona).

## 2. Skill portability layer (exists, skill-level only)

`[system]` `tools/generate-adapters.py` generates `adapters/{codex,claude-code,github-copilot}/skills/<skill>/SKILL.md` from one canonical `skills/core/<skill>/SKILL.md`. Per the script (lines 1–21, 89–105 read this session): it copies each skill's **body byte-for-byte unchanged** and only (a) replaces YAML frontmatter with platform-specific metadata, (b) appends a Platform Adapter section with capability mappings and declared limitations, (c) produces byte-identical output on regeneration. `adapters/<platform>/overlay.yaml` holds `capability_mappings` (abstract → concrete tool name) and `capabilities` (native/manual-fallback/unsupported classification) per platform.

`[system]` `docs/design/platform-adapters-component-plan.md` (Grilling Session 11, Decisions 82–91) is the authoritative design record for this layer. Decision 84 (read this session) already flags `subagent_spawn`/`subagent_isolation` as **asymmetric across platform overlays** — classified natively only on Claude Code (via a `Task`-equivalent tool), missing from the Codex and GitHub Copilot overlays as of that decision.

`[inference]` This mechanism proves the "one canonical source, N generated platform outputs" pattern works — but only for skill *prose*, where the body content itself never varies. It does not touch runtime execution or model dispatch.

## 3. Agent-type portability layer (exists, built this session, one pilot)

`[system]` No `.claude/agents/`-equivalent directory existed anywhere in the repo or user home before this session (confirmed via directory search, twice). This session (`2026-08-25-001` Decision 1, accepted, Result: pass) hand-authored one canonical agent-type persona (`~/.claude/agent-types/blender-operator.md`) and transcribed its instruction body verbatim into three real harness-native formats: `~/.claude/agents/blender-operator.md` (Claude Code — YAML frontmatter + Markdown body), `~/.codex/agents/blender-operator.toml` (Codex CLI — TOML fields, body in `developer_instructions`), `~/.copilot/agents/blender-operator.md` (GitHub Copilot — Markdown + YAML frontmatter). Diffed byte-identical after one authoring correction.

`[system]` The Codex transcription is confirmed **broken against real Codex parsing** (`2026-08-25-001`, evidence ledger): `"invalid type: sequence, expected a map"` for `mcp_servers`. Independently corroborated twice — once by real `codex exec` output in this session, once by a separate, concurrent Codex Desktop session's own evidence entry on the same Work Object, which dispatched the blender-operator contract successfully through its own subagent runner but explicitly noted this does not prove native `.toml` autoloading.

`[inference]` One pilot is not evidence that hand-transcription scales to the other 7 execution-shaped skill candidates — it demonstrates the wrapper-shape claim (body reusable verbatim, only wrapper syntax varies) holds for one case.

## 4. Runtime / graph layer

`[system]` `runtime/` (Python, `pyproject.toml` name `work-studio-runtime`, isolated `.venv`, Python ≥3.11, strict Pydantic dependency) contains `graph.py` (1860 lines), `handoff.py` (162 lines), `envelope.py` (75 lines), plus `business.py`, `engineering.py`, `research.py`, `mutation_protocol.py`, `persistence.py`, `projection.py` (not read this session).

`[system]` `graph.py` defines real `langgraph.graph.StateGraph` graphs, checkpointed to SQLite (`SqliteSaver`): a minimal 2-node tracer (`load_envelope` → `validate`), a **Phase 6 graph** (`build_phase6_graph`: `dispatch → {branch_a, branch_b} → join → direction_gate`, `PHASE6_MAX_CONCURRENCY = 2`, crash/resume recovery via `_phase6_crash_hook`, `interrupt()`-based human approval gates via `authority_gate`), and a **research graph** (`propose_fetch → gate_fetch → fetch_source → record_note`, gated by `interrupt()` before any live fetch).

`[system]` A grep of `graph.py` for any model/subprocess invocation (`anthropic|openai|codex|subprocess\.run|requests\.(post|get)|httpx|api_key|model_client`) found **exactly one** hit — an unrelated `subprocess.run` at line 448, part of checkpoint-DB recovery tooling, not agent dispatch. `phase6_dispatch`/`branch_a`/`branch_b` (lines 845–962) build `HandoffEnvelope` **proposal payloads** via `_phase6_business_dispatch_payload`/`_phase6_engineering_dispatch_payload` and never invoke a model. This is by explicit design: ADR 0025 ("single-writer rule") states the graph is "a non-writer of canonical state by construction... it reads `.work-studio/` and writes only to its own gitignored marker file."

`[inference]` The graph today is a **dispatch-proposal and state-transition engine**, not an execution engine. It has never called out to any model or coding harness. Any claim that agent execution needs to be woven "into" the graph's existing nodes is not supported by what the graph currently does — there is no existing execution call-site to nest into or conflict with.

## 5. Handoff / routing contract

`[system]` `runtime/handoff.py` defines `HandoffEnvelope` (dispatch record: `from_role`, `to_skill`, `component_kind`, `governance_domain`, `task`, `input_refs`, `expected_output`, `authority_scope`) and `HandoffReceipt` (completion record: `status`, `output_refs`, `verification_gaps`, `proposed_next_skill`, `started_at`, `completed_at`). Both are strict Pydantic models (`extra="forbid"`).

`[system]` `_STATE_ROUTING_TABLE` (lines 83–92) maps the 8 canonical Work Object states to skill names (`notice→turn-signal-into-work`, `explore→develop-idea`, `design→design-tracer-bullet`, `build→implement-bounded-change`, `verify→verify-release-evidence`, `release→deploy-with-recovery`, `observe|close→review-outcome-and-adapt`). This is a **manually-synced mirror** of the same table in `governance-conduct-work-object/SKILL.md` — a test (`test_state_routing_table_stays_in_sync_with_conductor`) fails on drift.

`[system]` `HandoffEnvelope`'s `ComponentKind`/`GovernanceDomain` Literal types are cross-validated at import time against `tools/ws/component_governance.py`'s `VALID_COMPONENT_KINDS`/`VALID_GOVERNANCE_DOMAINS` — a `RuntimeError` on drift, not a silent divergence.

`[inference]` This is a skill-to-skill routing contract, keyed purely on Work Object state. It has no field for "which model/provider should execute this" — that concept does not exist anywhere in `handoff.py` today.

## 6. Deterministic layer / canonical persistence

`[system]` `references/WORK-OBJECT.md` (canonical schema doc) defines the 8-state lifecycle (`notice|explore|design|build|verify|release|observe|close`, ADR 0015, "8-state permissive model with evidence gates") plus `status` (active/waiting/paused/closed), `consequence` (low/meaningful/high), `sensitivity` (ordinary/private/restricted), and the body's canonical sections including **Workflow Candidates** ("Proposed workflow rules with evidence" — not present by default in every generated template; added directly to `2026-08-25-001` this session per `alawas-governance-maintain-working-method`'s contract).

`[system]` All `.work-studio/` mutations route through `python3 -m tools.ws` (the deterministic CLI), enforcing immutable ID allocation, lifecycle transition rules, optimistic concurrency (`--expect-updated` required on every mutating command except `create`/`init`), frontmatter schema validation, and append-only invariants on `Evidence ledger` and `History`. `tools/ws/component_governance.py` and `runtime/envelope.py`'s `WorkObjectEnvelope` (strict Pydantic, raises `ValidationError` on frontmatter drift) both validate against this same canonical model.

`[system]` `ws` supports 30+ subcommands (`create`, `start`, `transition`, `close`, `append-evidence`, `append-history`, `append-artifact`, `graph`, `domain`, `validate`, `outcomes`, `command-center`, `backup`, `restore`, etc. — confirmed via `ws --help` this session).

## 7. Runtime dispatch layer (built this session, one pilot, not yet a general system)

`[system]` `runtime/agents.py` (new file, created this session, `2026-08-25-001` Decisions 2–5) contains: `AuthorityEnvelope` (3 booleans: `inspect`/`modify_code`/`deploy` — simplified from an originating proposal's unspecified type), `AgentRequest` (Pydantic, fields: `task`, `role`, `skill`, `work_object_id`, `context_refs`, `artifact_refs`, `required_capabilities`, `constraints`, `protected`, `authority`, `expected_output`, `consequence`), `AgentResult` (Pydantic, `status: Literal["completed","blocked","needs_approval","failed"]`, `summary`, `outputs`, `evidence_candidates`, `proposed_actions`, `artifacts`, `unresolved_questions`, `tool_trace_ref` — all list-of-string fields, simplified from the proposal's unspecified `ObjectRef`/`EvidenceCandidate`/etc. types), `AgentAdapter` (`runtime_checkable` Protocol: `name: str`, `async def run(request) -> AgentResult`), `CodexAgentAdapter` (concrete implementation), `AgentResolver` (linear-scan registry match on `type` + `capabilities` subset, no scoring).

`[system]` `CodexAgentAdapter.run()` shells out to `codex exec --json --sandbox read-only --skip-git-repo-check --ignore-user-config -c mcp_servers={} <task>` and parses the resulting JSONL stream for `{"type":"item.completed","item":{"type":"agent_message","text":...}}` events. Two real dispatch calls were made against an isolated scratch directory this session; one succeeded cleanly (`status=completed`), one initially exposed a real gap (an honest task failure was misclassified as `completed`) that was found, fixed (map to `blocked` when any `command_execution` item reports `status=failed`), and re-verified. The `mcp_servers={}` override was added after discovering `--ignore-user-config` alone did not prevent a live MCP connection attempt (`rmcp` worker to `mcp.cloudflare.com`) during verification.

`[system]` `runtime/agents.py` sits **beside** `runtime/graph.py`, not inside it or wired into `_STATE_ROUTING_TABLE`, `HandoffEnvelope`, or any graph node. It is not registered, imported by, or called from any other file in the repository.

`[decision]` `2026-08-25-001` Decision 2 recorded this build as a **director override** of a pressure-test's medium-high-confidence recommendation to wait for a second real dispatch case before building — recorded explicitly as an override, not as evidence-driven agreement, with a named revisit trigger: if `CodexAgentAdapter` sits unused after this one pilot with no second adapter or second skill routed through it, that is itself the "dead abstraction" signal.

## 8. What exists vs. what is implied vs. what is a gap

| | Status |
|---|---|
| Skill-level canonical→N-platform generation | **Exists**, proven, in production use (`tools/generate-adapters.py`) |
| Agent-type canonical→N-harness config-file portability | **Exists for one pilot**, one file confirmed broken against real parsing |
| Runtime graph that proposes skill handoffs | **Exists**, never executes anything itself (by design, ADR 0025) |
| Runtime dispatch to an actual model/harness | **Exists for one adapter (Codex), one skill never yet routed through it** |
| A second, structurally different adapter (e.g. multimodal) | **Does not exist** |
| Any skill migrated to be invoked *through* `AgentResolver`/`AgentAdapter` rather than by the calling harness directly | **Does not exist** — `engineering-implement-bounded-change`, named in Decision 2's scope as the first migration target, has not been touched; its `SKILL.md` is unmodified |
| A registry/config file declaring available agents declaratively (vs. hardcoded in Python) | **Does not exist** |
| Wiring between `runtime/agents.py` and `runtime/graph.py`/`handoff.py` | **Does not exist** — deliberately, per Decision 3's scope, pending the "does this sit beside or inside the graph" question, which the grep evidence above answers (beside) but which has not been *implemented* as an actual integration |
| A concurrent-Work-Object-write concurrency model beyond optimistic locking | **Untested by design** — `2026-08-25-001` recorded this as Workflow Candidate `WFC-2026-08-25-001-A`, status `active`, no bounded test run |

---

## Note on scope

This document answers only "what exists." It deliberately does not contain Sections B–M of the director's original request (gaps requiring new work, proposed architecture, core contracts beyond what's built, registry design, runtime integration changes, skill migration steps, a second adapter design, a testing plan, an implementation sequence, or a final recommended tracer) — those require new decisions this studio's own working method (one bounded, evidence-gated, director-accepted decision at a time, via `alawas-design-design-tracer-bullet` / `alawas-thinking-pressure-test-decision`) has not yet made. Authoring them here would present unaccepted architecture as if it were settled, which is the exact failure mode `alawas-research-produce-report` is built to prevent for plan-type deliverables.

The natural next bounded decision, grounded in this document's own findings: whether to migrate `engineering-implement-bounded-change` (already named in Decision 2's scope) through `AgentResolver`/`CodexAgentAdapter` as the second real case — the same evidence-first path `2026-08-25-001` has followed since Decision 1.
