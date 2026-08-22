# Report: giving this Work Studio its own MCP server
Work Object: `2026-08-21-010`. Report-type deliverable — decomposed into three
falsifiable sub-questions, each investigated against real evidence in this
repository and environment. Model-knowledge claims about the Model Context
Protocol's general shape (not fetched from a primary source this session) are
marked `[inference]`, not `[system]`.

## Sub-question 1: what does "having my own MCP" actually mean here?

**Answer: running an MCP *server* that exposes this studio's capabilities to
MCP clients — not consuming someone else's MCP server.** This studio already
has real, decided experience with the *opposite* direction.

- `[system]` `docs/design/claude-design-mcp-integration-plan.md` (238 lines,
  status "Decided — 25 human-accepted decisions", Work Objects
  `2026-07-27-004` through `-007`) records how this studio integrates
  *Claude Design's* MCP server as a *consumer*: an abstract capability
  (`claude_design`) reached via direct MCP, classified `native`/`manual-fallback`/
  `unsupported` per runtime in `adapters/*/overlay.yaml` (confirmed:
  `adapters/claude-code/overlay.yaml:56` declares `claude_design: native`).
- `[system]` grep across the repo for "mcp" (case-insensitive) finds this one
  precedent and nothing else — no existing code, config, or design record for
  this studio *hosting* an MCP server of its own.
- `[inference]` The director's phrasing ("having my own mcp") most naturally
  reads as the server direction — something other tools (Claude Desktop,
  Claude Code, or any MCP client) could connect to and get Work Studio
  capabilities from — which is the direction with zero existing precedent
  here, unlike consumption.

## Sub-question 2: what's the technical/dependency shape?

- `[system]` No `mcp` Python package is installed in this environment —
  confirmed via `import mcp` failing (`ModuleNotFoundError`) under both the
  system Python and the repo's `uv`-managed `.venv`. Building a server would
  need adding this as a new dependency.
- `[system]` This repo has two distinct, already-decided dependency postures:
  `tools/ws` is deliberately dependency-free stdlib (confirmed this session,
  `pyproject.toml` has no dependency for it; `WO 2026-08-21-003`'s evidence
  ledger records this as a deliberate design constraint), while `runtime/`
  already accepts real dependencies (`langgraph`, `pydantic`, `networkx`) for
  the LangGraph local runtime. An MCP server would need to pick one of these
  postures deliberately, not default into either by accident — adding `mcp`
  to `tools/ws` would break its stated dependency-free constraint; adding it
  as a `runtime/`-adjacent component would not.
- `[inference]` The official MCP SDK for Python is a real, actively maintained
  package (general knowledge, not fetched this session — flagged as
  `[inference]` rather than claimed as verified against the current spec).

## Sub-question 3: what would the server actually expose?

- `[system]` `tools/ws`'s own `--help` output (already surfaced earlier this
  session) lists 20+ subcommands — `create`, `transition`, `close`,
  `activate`, `append-evidence`, `append-history`, `validate`, `outcomes`,
  `backup`, `restore`, and more — each a natural candidate for one MCP tool,
  since they're already a stable, scriptable, deterministic CLI contract.
- `[system]` This very session's own tool list is a live, concrete example of
  what such an integration looks like from the client side: dozens of
  `mcp__<server>__<tool>` entries, each one operation exposed by some running
  MCP server. A Work-Studio-hosted server exposing `ws create`, `ws
  transition`, etc. as `mcp__work-studio__create`, `mcp__work-studio__transition`
  would follow the identical shape already visible in this environment.
- `[gap]` Whether every `ws` subcommand should be exposed, or only a curated
  subset, was not investigated — that's a design decision (authority
  boundaries, which commands are safe to expose to an external MCP client
  versus conductor-only), not a research question this report resolves.

## What this report does not resolve

This is a report, not a plan or an implementation. It establishes: the
director wants a server, not a client; no dependency for one exists yet and
adding it crosses an already-decided dependency-posture line that needs a
deliberate choice; and `tools/ws`'s existing CLI surface is the natural
mapping target. It does not decide which dependency posture to use, which
commands to expose, or how authority/consequence gating would work for an
external MCP client mutating Work Objects — those are design and decision
work, not research, and belong to `alawas-thinking-pressure-test-decision` and
`alawas-design-design-tracer-bullet` if the director wants to proceed.
