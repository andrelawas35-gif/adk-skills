---
schema_version: 1
id: 2026-08-21-006
title: Utilize the runtime with the alawas skills -- does the runtime invoke skills, or is HandoffEnvelope.to_skill only a proposal?
type: inquiry
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T13:46:44Z
updated_at: 2026-08-21T14:41:30Z
next_action: None required -- Inquiry remains answered. The two noted gaps (missing --approve-direction CLI flag; Git Bash /tmp path-translation pitfall) are operational notes, not blocking findings; either could become its own small Work Object if the director wants them fixed, but neither is implied by this Inquiry's scope.





---
## Intent

Director's signal: "I want to utilize the runtime using my skills." Answer
the falsifiable question this implies: does the LangGraph local runtime
(`runtime/graph.py` and friends) actually invoke the `alawas-*` skills as
part of its execution today, and -- separately -- what would it take, and
would it be a good idea, for it to do so, versus the alternative of skills
using the runtime's mechanisms (checkpointing, effect journal, authority
gates) as their execution substrate without the graph itself calling out to
an LLM.

Starting evidence from an informal, ungoverned read this session (not yet
an Inquiry evidence-ledger entry -- restated here to be re-verified, not
assumed): `HandoffEnvelope`/`HandoffReceipt`'s `to_skill` field
(`runtime/handoff.py`, written at `runtime/graph.py:640-643`) looked like a
data record only -- Phase 6 writes `to_skill="specialist"`, a hardcoded
placeholder, not a real skill name -- and the three `subprocess` calls found
in `runtime/` (`graph.py:427`, `mutation_protocol.py:243`,
`persistence.py:199`) all shell out to `tools.ws`, none to Claude/an
agent/a skill. This Inquiry exists to verify that reading properly (with
evidence attribution) rather than act on it as settled.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Confirmed: no code path in `runtime/` invokes a skill, an LLM, or a Claude Code/Agent SDK session -- the informal reading stands as verified, attributed evidence (see Evidence ledger)
- [x] Build plan's stated intent checked: explicitly neither (a) nor (b) as originally framed -- the plan's own section title is "One first graph, not 22 autonomous agents," and its architecture diagram shows skill contracts feeding the runtime only as definitions, specialist nodes producing only typed proposals, with no path back into skill/agent execution
- [ ] **Not pursued -- moot given the finding.** Technical precondition for direction (a) (Agent SDK/Claude Code programmatic skill invocation) was not researched; the plan's explicit design intent already forecloses direction (a) regardless of technical feasibility, so this became unnecessary to answer this Inquiry
- [x] Recommendation given: neither direction -- the plan's actual intended pattern is a third option, already what's built: the runtime stays deterministic-only (dispatch, checkpoint, retry, gate, persist), skills run in a separate session/turn reading the `HandoffEnvelope` proposal, and results flow back only through the persistence node's governed write. No pressure-test-decision needed -- this isn't a live choice between competing options, it's confirming the existing design already matches its own stated intent


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

### Decision 1 — <summary>

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority / delegation |
| **Result** | pass / fail / pending |
| **Scope** | <!-- what this decision applies to --> |
| **Authorization** | <!-- who or what authorized this --> |
| **Confidence** | <!-- high / medium / low, plus basis. Scope-qualify when the decision's parts differ: 'high for <X>; low for <Y> — basis: <why>' --> |
| **Actor** | <!-- who made the decision --> |
| **Revisit trigger** | <!-- condition that would cause reconsideration --> |
| **Rationale** | <!-- why this decision was made --> |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | this session, Read references/architecture/langgraph-local-runtime-integrated-build-plan.md lines 1-110, 210-260 | references/architecture/langgraph-local-runtime-integrated-build-plan.md, section title itself: '6. One first graph, not 22 autonomous agents' -- explicit rejection of the graph autonomously dispatching to skills as agents. The architecture diagram (lines 24-47) shows SK (22 canonical skill contracts) feeding into RT (runtime) only as 'Skill definitions and routing obligations' (per the Truth and ownership boundaries table, line 103: owner Work Studio, recovery rule 'Regenerate and verify') -- contracts/definitions, not live invocation. AG (Specialist nodes/subgraphs) sits inside the Runtime plane and connects to RT via 'typed proposal/receipt' only; RT connects onward via 'one serialized persistence node' to CLI -- no arrow anywhere from RT back into SK or into any external agent/skill-execution process. The plan's stated non-capabilities (line 81) explicitly list 'no...agent-provider adapter' as of the inspected baseline. The plan's central operating principle (line 47): 'LangGraph may decide when execution proceeds. It must not decide what counts as canonical truth, adequate evidence, granted authority, or an accepted governing change.' Section 6's node mapping (lines 231-236) confirms current code matches this: 'semantic nodes/subgraphs' (inquiry, develop idea, pressure test, research, design direction, etc.) are named as a category, but the actual implemented Phase 6 branches (phase6_branch_a/branch_b, runtime/graph.py) are documented read-only, deriving proposals mechanically (derive_proposal) rather than invoking an LLM or skill. |
| [system] | this session: uv run python -m runtime.graph run-phase6/inspect-phase6 against 2026-08-21-006; uv run python -c run_phase6(...) direct calls; uv run python -c Path('/tmp/...').resolve() showing C:\tmp\...; find / for actual file locations | Demonstration run of run_phase6 against this Work Object (2026-08-21-006), confirming the answered finding operationally: uv run python -m runtime.graph run-phase6 2026-08-21-006 <thread> --checkpoint-db <path> dispatched, ran both read-only specialist branches, joined (both proposed develop-idea from the WO's explore state), and paused at direction_gate's interrupt -- a proposal, not a canonical write, exactly as the architecture doc describes. Separate-process inspect-phase6 and a separate-process approve_direction=True call both correctly read/resumed the durable SQLite checkpoint, completing with direction_approved: true. Gap noted: main()'s run-phase6 CLI subcommand does not expose --approve-direction; answering the direction_gate interrupt currently requires a direct Python call to run_phase6(..., approve_direction=...), not a pure CLI-only workflow. Platform note for future runs from Git Bash on Windows: a bare /tmp/... path is translated differently depending on how it reaches Python -- Git Bash auto-converts /tmp/... to %LOCALAPPDATA%/Temp/... only when passed as a literal CLI argument to a Windows exe, but a /tmp/... string embedded inside a python -c script resolves via Python's own path handling to C:\tmp\... instead. Mixing the two styles across separate invocations against 'the same' checkpoint path silently touches two different physical files, producing a misleading appearance of broken cross-process checkpoint resume (reproduced twice this session before the cause was found). Always resolve one explicit, unambiguous absolute path once and reuse it verbatim across every invocation touching a given checkpoint db. |
## Open questions

- **Answered.** The build plan states an intended relationship, explicitly: section 6's title ("One first graph, not 22 autonomous agents") and diagram show the runtime is meant to stay deterministic-only, with skill execution deliberately kept outside the graph. The current `to_skill` proposal-only pattern is the stated design, not an unfinished gap.
- **Not pursued, moot.** Whether the Agent SDK/Claude Code supports programmatic skill invocation was not researched -- the plan's stated intent already forecloses building toward that regardless of technical feasibility.
- **Not pursued, moot for the same reason.** Compatibility with ADR 0025/0026 was not separately checked, since direction (a) is not the design's stated direction to begin with.

## Next move

Answered; no further routing needed. Practical takeaway: skills and the LangGraph runtime are already usable together today, exactly as designed -- a skill (like `conduct-work-object`, in use this session) reads/writes Work Objects via `tools.ws`, and separately a bounded deterministic pass (`run_phase6`, `run_research`) can run through the LangGraph runtime for retry/checkpoint/journal/gate behavior on mechanical sub-steps. No build or design work follows unless the director wants a concrete demonstration run, which would be a routine operational request, not new Inquiry or design work.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T13:47:17Z — create-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director's signal 'I want to utilize the runtime using my skills' framed as an Inquiry after an informal (ungoverned) read this session suggested the runtime's to_skill field is a proposal, not an invocation. Activated directly to explore rather than left in notice, since the question is already concrete and falsifiable, not a vague signal needing turn-signal-into-work classification.
### 2026-08-21T13:49:07Z — answered-neither-direction-runtime-stays-deterministic

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Answered from primary-source evidence in this repo's own architecture doc, no reality contact or external research needed. references/architecture/langgraph-local-runtime-integrated-build-plan.md section 6 is titled 'One first graph, not 22 autonomous agents' and its diagram shows skill contracts feeding the runtime only as definitions/routing obligations (not live invocation), specialist nodes producing only typed proposals/receipts, and no path from the runtime back into skill/agent execution. The plan's central principle: 'LangGraph may decide when execution proceeds. It must not decide what counts as canonical truth, adequate evidence, granted authority, or an accepted governing change.' Neither candidate direction (a: graph autonomously invokes skills: b: skills use runtime mechanisms as their execution substrate) matches the stated intent -- the actual designed pattern is a third option, already what exists: runtime stays deterministic-only, skills run in a separate session reading the HandoffEnvelope proposal, results return only through the governed persistence node. This confirms the current to_skill-is-proposal-only code matches its own design intent rather than being an unfinished gap.
### 2026-08-21T14:41:30Z — demonstrated-run-phase6-against-this-wo

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director asked for a concrete demonstration of run_phase6 against a real Work Object (this one). Ran dispatch/branches/join/direction_gate across three separate processes with a durable SQLite checkpoint, confirming the answered finding operationally: proposal only (develop-idea), paused for approval, no canonical write until governed persistence. Recorded two operational gaps found along the way: the run-phase6 CLI subcommand does not expose --approve-direction (a direct Python call is currently required), and a platform-specific path-translation pitfall when scripting from Git Bash on Windows that twice produced a misleading appearance of broken cross-process checkpoint resume before the actual (mundane) cause was found.
