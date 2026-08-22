---
schema_version: 1
id: 2026-08-21-010
title: Give this Work Studio its own MCP server -- feasibility and shape
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T18:45:47Z
updated_at: 2026-08-21T19:02:11Z
next_action: Director decision needed: close this Work Object now (mcp_server/ stands as a minimal, deliberately single-tool proof, with the exposure-scope/authority decision explicitly deferred), or continue design work on which further ws commands to expose and how authority gating should work for a mutating one














---
## Intent

Director's signal: "include mcp integration into my work studio by having
my own mcp." Most natural reading: run an MCP (Model Context Protocol)
*server* that exposes this Work Studio's capabilities -- the Work Object
model, `tools/ws` operations -- to MCP clients (Claude Desktop, Claude
Code, or any other MCP-speaking tool), rather than this studio consuming
someone else's MCP server.

Report-type deliverable (per `alawas-research-produce-report`'s classification step): no
existing Work Object holds a decided trail about MCP integration to
synthesize from -- this is genuinely new ground, so it decomposes into
falsifiable sub-questions for `alawas-research-investigate-live-question`, not a plan
synthesis.

**Deliverable:** `.work-studio/deliverables/2026-08-21-010-mcp-server-report.md`

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Three sub-questions decomposed and investigated with real evidence: found existing MCP-consumption precedent (`docs/design/claude-design-mcp-integration-plan.md`), confirmed no `mcp` package installed, confirmed `tools/ws`'s CLI surface as the natural mapping target
- [x] One standalone deliverable document produced at `.work-studio/deliverables/2026-08-21-010-mcp-server-report.md`, linked from this Work Object's Intent
- [x] Real `mcp_server/` package built per Decision 1's accepted design, installed, and verified end-to-end (`ws_validate` tool, `exit_code=0`), exposing only the one already-proven safe operation -- exposure of any mutating `ws` command left as the explicitly named, still-unresolved decision
- [x] One genuine gap reported honestly, not resolved: which `ws` subcommands should be exposed, and how authority/consequence gating would work for an external MCP client -- explicitly named as design/decision work this report does not do


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

### Decision 1 — MCP server lives in a new sibling package (`mcp_server/`), not inside `tools/ws` or `runtime/`

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A future MCP server component gets its own package (working location: `mcp_server/`, own `pyproject.toml`), depending on `tools.ws` as an ordinary library dependency (already pip-installable per `2026-08-21-003`'s proven tracer bullet) plus `mcp` as its only new dependency. It does not live inside `tools/ws` (would break `tools/pyproject.toml`'s `dependencies = []` contract, built and tested this session) and is not folded into `runtime/` (wrong conceptual surface -- this Work Object's own report found `tools/ws`'s CLI subcommands, not `runtime/`'s LangGraph graphs, are the natural mapping target for MCP tools). |
| **Authorization** | Director: "Yes, do recommended" -- consequence is `meaningful`, generic acceptance is sufficient authority at this level |
| **Confidence** | medium-high -- grounded in real packaging evidence (`tools/pyproject.toml`'s enforced `dependencies = []`, `tools/ws`'s already-proven pip-installability), not just architectural preference. Not higher because whether `runtime/` execution capabilities (`run_phase6`, checkpoints) should also be exposed via MCP was not tested -- if so, this package would additionally depend on `runtime/`, which this branch already accommodates without contradiction. |
| **Actor** | director |
| **Revisit trigger** | If the actual want turns out to be exposing LangGraph execution (checkpoints, interrupts) rather than Work Object CRUD, revisit toward folding into `runtime/` instead (rejected Branch A) |
| **Rationale** | `tools/ws`'s `dependencies = []` is not just a stated intent but an enforced, already-tested packaging contract -- adding `mcp` inside it would directly violate work this same session already shipped. A new sibling package mirrors the exact independently-packaged-component pattern `2026-08-21-003` proved, keeps `runtime/`'s dependency graph untouched, and matches this Work Object's own report finding about which surface (`tools/ws`, not `runtime/`) actually needs wrapping. |

**Edge case noted:** `mcp_server/` importing `tools.ws` requires it actually be installed (`pip install -e` or equivalent) in the working dev environment, not just proven installable in an isolated scratch venv (`2026-08-21-003`'s tracer bullet used a disposable venv, not the main dev workflow) -- this needs confirming before real implementation, not assumed to already work.

**Assumption that would invalidate this choice if wrong:** that MCP tools map cleanly 1:1 onto `tools/ws` CLI subcommands, rather than needing a different, more MCP-native interface shape (the MCP spec distinguishes tools from resources, for instance) -- untested, `[inference]` only.

**Future friction noted:** `tools/pyproject.toml` requires Python `>=3.9`, the root `pyproject.toml` requires `>=3.11` -- if `mcp_server/` ever needs both `tools.ws` and `runtime/` as dependencies, it inherits the stricter `>=3.11` constraint, which is fine today but is a real, already-visible seam, not a hypothetical one.

### Decision 2 — Accepted tracer bullet, narrowed: confirm `tools.ws` installs/imports in the real dev `.venv` only

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Split from the originally proposed two-part tracer bullet. This slice tests only the first uncertainty: `uv pip install -e tools/` into the repo's real `.venv` (not a disposable scratch one), then confirm `tools.ws` is importable from a location outside its own directory. Defining an MCP tool wrapping a `ws` operation is deferred to a second slice, not attempted here. |
| **Authorization** | Director: "Yes, do the smaller slice first" |
| **Confidence** | high that the install itself will succeed (the packaging contract was already proven installable in a scratch venv, `2026-08-21-003`); the open question is only about the real-venv environment specifically, not the packaging mechanics |
| **Actor** | director |
| **Revisit trigger** | If the editable install fails or `tools.ws` is not importable from outside its directory even after installing, this blocks Decision 1 entirely -- revisit the sibling-package approach before any MCP tool work proceeds |
| **Rationale** | Smaller, cheaper slice than testing both uncertainties at once. Isolates whether the real-dev-venv install works at all before spending effort defining an MCP tool against an import that might not succeed. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | this session: grep -rln -i mcp across repo; Read docs/design/claude-design-mcp-integration-plan.md; grep claude_design adapters/claude-code/overlay.yaml; python3.13 -c import mcp / uv run python -c import mcp | Report produced. Key finding: docs/design/claude-design-mcp-integration-plan.md (238 lines, Decided, 25 accepted decisions, WOs 2026-07-27-004..007) already documents this studio consuming an external MCP server (Claude Design) via the abstract-capability system (claude_design in adapters/*/overlay.yaml, confirmed adapters/claude-code/overlay.yaml:56 declares claude_design: native). No existing precedent for this studio hosting its own MCP server -- grep for mcp across the repo finds only this consumption-direction precedent. mcp Python package not installed under system Python or the repo's uv .venv (ModuleNotFoundError both). tools/ws has 20+ subcommands, a natural mapping target for MCP tools, matching the mcp__<server>__<tool> shape already visible in this session's own tool list. |
| [system] | this session: Read runtime/graph.py:415-451 in full (node2_validate + its subprocess call and comment) | Decision 1 revisited on director's direct question ('would it be better to fold it into runtime'). Investigated the exact reason runtime/graph.py uses subprocess to reach tools.ws (runtime/graph.py:434-439, direct read): it exists solely to decouple the runtime process's own cwd from tools.ws's CWD-based root discovery (_find_work_studio_root) for cross-repo support (WO 2026-08-21-001) -- a narrow workaround for one coupling problem, not a general 'reach tools.ws via subprocess, not import' principle. A library import would face the same cwd-discovery issue and would need its own fix (an explicit root parameter), regardless of which package hosts it -- so this evidence does not actually favor runtime/ over a new sibling package. Decision 1's original grounding (tools/pyproject.toml's enforced dependencies=[], the report's finding that tools/ws's CLI is the real target surface) was re-examined and confirmed to still hold. Director: stick with Decision 1. |
| [system] | this session: uv pip install -e tools/; cd /tmp && python -c import tools.ws / schema / VALID_EVIDENCE_TAGS; cd /tmp && ws --version / --help | Decision 2 implemented and verified. uv pip install -e tools/ into the real dev .venv (not a scratch one) succeeded: Installed 1 package, work-studio-ws==0.1.0 (from file:///.../tools). Confirmed importability from outside the repo entirely: running from /tmp (cd /tmp && .venv/Scripts/python.exe -c ...), tools.ws, tools.ws.schema, and tools.ws.sections.VALID_EVIDENCE_TAGS all import correctly, resolving to the real repo source (tools.ws.__file__ = .../tools/ws/__init__.py) -- the exact imports runtime/graph.py's subprocess mechanism already depends on, now proven to also work via direct import, not just via subprocess+PYTHONPATH. The installed ws console script also runs standalone from /tmp (ws --version -> 1.0.0, ws --help lists all subcommands). Both halves of Decision 1's edge case now confirmed in the real dev environment, not a disposable scratch venv. |
| [system] | this session: uv add --group test mcp; uv run --group test python -c inspect of mcp.server submodules and importlib.metadata; scratch script mcp_tool_poc.py (written, run twice, deleted) | Second tracer-bullet slice executed. Added mcp>=2.0.0 to the test dependency group (uv add --group test mcp; pulled mcp 2.0.0 plus transitive deps -- click, starlette, uvicorn, jsonschema, etc). Correction to an earlier [inference]: the installed SDK's high-level API is mcp.server.mcpserver.MCPServer, not mcp.server.fastmcp.FastMCP as assumed from general knowledge -- confirmed via importlib.metadata this is the genuine official 'Model Context Protocol SDK' (LF Projects), just a newer major version (2.0) with a restructured API than what was assumed. Wrote a scratch script (deleted after the test) defining one MCP tool (ws_validate) wrapping the real tools.ws validate command against this Work Object itself. First run hit a real bug in the scratch script, not the assumption: tools.ws.__main__.main() takes no argv parameter, reads sys.argv directly -- fixed by patching sys.argv around the call. Second run succeeded end-to-end: server.list_tools() showed the tool registered; server.call_tool('ws_validate', {'work_object_id': '2026-08-21-010'}) returned exit_code=0, 'All default validation checks passed.' -- a correct, real result from the actual tools.ws validate command, invoked through a real MCP tool wrapper, in-process. Both of Decision 1's open uncertainties (real-venv install, tool/CLI-subcommand mapping) are now confirmed with positive evidence, not assumed. |
| [system] | this session: Write mcp_server/pyproject.toml, __init__.py, server.py; uv pip install -e mcp_server/; python -c import mcp_server.server, list_tools/call_tool; ls .venv/Scripts/ for work-studio-mcp.exe; work-studio-mcp.exe --help exit code | Real mcp_server/ package built per Decision 1's exact accepted design: mcp_server/pyproject.toml (name work-studio-mcp, dependencies mcp>=2.0.0 + work-studio-ws via [tool.uv.sources] path=../tools editable=true), mcp_server/src/mcp_server/__init__.py, mcp_server/src/mcp_server/server.py. Exposes exactly one tool, ws_validate -- the proven read-only pattern from both tracer bullets -- with an explicit module-docstring guard against silently adding a mutating tool (create/transition/close/append-*) without first resolving the named authority/exposure-scope gap. uv pip install -e mcp_server/ succeeded (Installed 1 package, work-studio-mcp==0.1.0). Verified via the real installed package (not the scratch script): from mcp_server.server import server; server.list_tools() shows ['ws_validate']; server.call_tool('ws_validate', {'work_object_id': '2026-08-21-010'}) returns exit_code=0, 'All default validation checks passed.' -- identical correct result to the tracer bullet. Console script work-studio-mcp.exe exists in .venv/Scripts/ and runs without error (exit 0); full client-server handshake was an explicit non-goal, not attempted. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T18:46:11Z — create-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director asked to give this Work Studio its own MCP server. Classified as report-type per alawas-research-produce-report: no existing decided trail exists to synthesize, so this decomposes into falsifiable sub-questions for investigate-live-question rather than a plan synthesis.
### 2026-08-21T18:48:08Z — deliverable-produced

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** alawas-research-produce-report classified this as report-type (no decided trail to synthesize), decomposed into three falsifiable sub-questions, investigated each with real evidence, and produced .work-studio/deliverables/2026-08-21-010-mcp-server-report.md. Key finding: this studio already has decided precedent for consuming an MCP server (Claude Design, docs/design/claude-design-mcp-integration-plan.md), but none for hosting one -- the director's ask is the unprecedented direction. One genuine gap named, not resolved: which ws subcommands to expose and how authority gating works for an external client.
### 2026-08-21T18:50:48Z — dependency-posture-decision-recorded

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Pressure-tested the dependency-posture question blocking progress. Decided (Decision 1): MCP server lives in a new sibling package (mcp_server/), depending on tools.ws as a library plus mcp as its only new dependency -- not inside tools/ws (breaks its dependencies=[] contract) and not folded into runtime/ (wrong conceptual surface per this WO's own report). Director: do recommended. Transitioning explore -> design now that the blocking decision is resolved.
### 2026-08-21T18:53:26Z — decision-1-reexamined-confirmed

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director asked directly whether runtime/ would be better than the sibling-package Decision 1. Investigated runtime/'s subprocess-based tools.ws integration in full; found it's a narrow cwd-decoupling workaround (WO 2026-08-21-001 cross-repo support), not a general boundary-crossing pattern -- does not transfer to the packaging-location question. Decision 1 re-examined and confirmed unchanged: MCP server stays in a new sibling package (mcp_server/).
### 2026-08-21T18:54:50Z — accepted-narrowed-tracer-bullet-route-to-implement

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted a narrower first slice of the tracer bullet (Decision 2): confirm tools.ws installs/imports in the real dev .venv only, deferring the MCP tool definition to a second slice. Routing to implement-bounded-change.
### 2026-08-21T18:55:48Z — real-venv-install-verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 2's narrowed tracer bullet confirmed: tools.ws installs editable and imports cleanly in the real dev .venv from outside the repo entirely, including the exact imports runtime/graph.py already depends on via subprocess. The ws console script also runs standalone. This uncertainty is fully resolved.
### 2026-08-21T18:56:14Z — second-tracer-bullet-slice-route-to-implement

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted running the deferred second slice: add mcp as a dependency, define one MCP tool wrapping a safe read-only ws operation, confirm in-process invocation.
### 2026-08-21T18:58:28Z — second-slice-verified-both-uncertainties-resolved

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Second tracer-bullet slice succeeded end-to-end: a real MCP tool (mcp.server.mcpserver.MCPServer, official SDK 2.0.0) wrapping tools.ws's real validate command executed correctly in-process against this Work Object, returning exit_code=0. Both of Decision 1's open uncertainties -- real-venv install, and CLI-subcommand-to-MCP-tool mapping -- are now confirmed with positive, executed evidence. Corrected one earlier [inference]: the SDK's actual API is mcp.server.mcpserver.MCPServer, not the mcp.server.fastmcp.FastMCP assumed from general knowledge. New implementation-relevant fact for later: tools.ws.__main__.main() takes no argv parameter and reads sys.argv directly, requiring the wrapper to patch sys.argv per call.
### 2026-08-21T19:02:11Z — real-package-built-and-verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** mcp_server/ built exactly per Decision 1's accepted design: separate package, tools.ws as a library dependency via uv path source, mcp as its only other dependency, exposing one proven safe tool (ws_validate). Installed and verified via the real package (not the scratch script) -- identical correct result. Console script resolves and runs. This Work Object's core question is now answered with working code, not just a report and tracer bullets.
