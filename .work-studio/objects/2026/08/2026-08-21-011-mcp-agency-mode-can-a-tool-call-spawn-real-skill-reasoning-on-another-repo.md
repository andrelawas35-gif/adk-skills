---
schema_version: 1
id: 2026-08-21-011
title: MCP agency mode -- can a tool call spawn real skill reasoning on another repo
type: inquiry
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [architecture, research]
created_at: 2026-08-21T19:08:37Z
updated_at: 2026-08-25T22:48:17Z
next_action: Closed. DeepSeek adapter path superseded by WO 2026-08-25-001 Decision 15 (OpenCodeAgentAdapter). MCP agency-mode question remains open as successor inquiry.









---
## Intent

Director's framing: this Work Studio as "an agency that works on another
project" -- and confirmed the ambitious version: the agency does the
*thinking* (design, implementation, decisions), not just mechanical Work
Object CRUD, on a repo it doesn't live in. That means the `mcp_server/`
package built in `2026-08-21-010` (one tool, `ws_validate`, a plain CLI
wrapper) is the wrong shape for this -- calling it doesn't invoke any
`alawas-*` skill's reasoning, it just runs a deterministic command.

Falsifiable question: can an MCP tool function -- called from an external
Claude Code session working on a different repo -- itself invoke a real
Claude Code / Agent SDK session (with actual skill-invocation and
multi-turn reasoning capability) against that target repo, and return a
genuine result, not a canned one? `2026-08-21-006` named this exact
technical precondition (`does the Claude Agent SDK / Claude Code support
one process invoking a named skill/subagent programmatically`) and
explicitly did not research it, because the plan's own stated intent
foreclosed that direction for the in-repo runtime question. That
foreclosure does not apply here -- this is a different question (agency
serving another repo via MCP), not the local runtime/skill relationship
`2026-08-21-006` already answered.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Technical precondition researched with real primary sources: **it exists, but is Anthropic-only.** The Claude Agent SDK runs a real agent loop in-process and auto-loads `alawas-*` skills, but its `model` field only accepts Anthropic model aliases/IDs, with no custom endpoint or provider override -- confirmed an architectural constraint, not a configurable setting. The `claude -p` headless subprocess route is equally Anthropic-only (it IS the Claude Code CLI). **Neither mechanism supports a DeepSeek-powered agent.** Director's actual want (DeepSeek API + these skills) requires a third, unresearched path: a custom agent loop calling DeepSeek's API directly, manually loading the skill `.md` files as prompt content -- feasible in principle since skill content is plain Markdown, not SDK-internal, but not yet verified.
- [ ] Not yet run: the smallest reality check of an MCP tool function actually hosting/invoking either mechanism (process model, auth, session lifetime)
- [x] Honest answer given: **buildable, with real work, not free.** Both mechanisms are real. The SDK route requires a paid Anthropic API key (docs explicitly bar claude.ai-login-based auth for third-party agent products) -- a real operational cost this session's own subscription context doesn't cover. The subprocess route avoids that but shells out to the `claude` binary itself, with its own session/auth questions unverified.


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

### Decision 1 — DeepSeek adapter path superseded by OpenCodeAgentAdapter

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The proposed DeepSeek-specific adapter target (zero model-tier binding, like codex) is superseded by WO 2026-08-25-001 Decision 15, which built an OpenCodeAgentAdapter with zero model-tier binding supporting 75+ providers through Models.dev. A dedicated DeepSeek adapter is no longer necessary. |
| **Authorization** | Director accepted, chat 2026-08-25: "close it with that outcome." |
| **Confidence** | high — OpenCodeAgentAdapter verified with two real dispatches (PONG test and blocked-classification test); zero model-tier binding confirmed. |
| **Actor** | conductor |
| **Revisit trigger** | If OpenCode's provider model proves insufficient for a specific use case that DeepSeek's native API handles better, the dedicated adapter question may reopen. |
| **Rationale** | OpenCode already provides the model-agnostic dispatch layer this WO proposed building from scratch for DeepSeek. The broader MCP agency-mode question (can a tool call invoke real skill reasoning on another repo) remains open as a potential successor inquiry. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | WebFetch https://code.claude.com/docs/en/agent-sdk/overview (redirected from https://docs.claude.com/en/api/agent-sdk/overview) | Fetched https://code.claude.com/docs/en/agent-sdk/overview (official docs, redirect chain from docs.claude.com followed). Confirmed: the Claude Agent SDK is a real, official Python and TypeScript library that 'runs the agent loop in your own process' -- exactly one process programmatically starting a real agent session. Explicitly supports: Subagents ('spawn specialized agents for focused subtasks'), MCP, and critically 'Skills, commands, and memory -- Load automatically from your project's .claude/ and from ~/.claude/, same as Claude Code' -- meaning an SDK-driven session would auto-load the exact alawas-* skills already installed at ~/.claude/skills/ this session. Constraint found: 'Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login...Use the API key authentication methods' -- a real operational requirement (a paid Anthropic API key), not something this session's own claude.ai/subscription context provides for free. Alternative mechanism also documented: 'run the CLI as a subprocess with the -p flag and --output-format json' for headless invocation from any language -- this matches runtime/'s already-established subprocess pattern for reaching tools.ws, a second viable route with different tradeoffs (no SDK dependency, but shells out to the claude binary itself). |
| [system] | WebFetch https://code.claude.com/docs/en/agent-sdk/python | Fetched https://code.claude.com/docs/en/agent-sdk/python for model-provider configuration. Finding materially changes the earlier answer: the Claude Agent SDK's model field only accepts Anthropic model aliases (sonnet/opus/haiku/inherit) or full Anthropic model IDs -- no custom endpoint or provider override exists. The SDK wraps the Claude Code CLI subprocess, which talks to Anthropic's servers exclusively; this is described as an architectural constraint, not a configurable setting. This also eliminates the second mechanism named in this WO's earlier evidence (claude -p --output-format json headless subprocess) for a DeepSeek-based agent -- that subprocess IS the Claude Code CLI, equally Anthropic-only. Neither of the two previously-identified mechanisms supports a DeepSeek-powered agent. Skills-loading mechanism confirmed only partially: the SDK exposes a  option that adds a Skill tool to allowed_tools, but the docs available did not clarify whether skill content (the markdown files) is portable outside this SDK's own tool-loading mechanism -- this remains a real gap, not yet resolved either way. |
| [system] | this session, correcting a shell-parsing error in the prior append-evidence call | Correction to the immediately preceding evidence entry: a shell command-substitution error stripped a backticked code snippet from that entry, leaving a blank gap after 'the SDK exposes a'. The missing text was: skills: list[str] | Literal[all] | None = None -- a Python type-hinted option on ClaudeAgentOptions that adds a Skill tool to allowed_tools when set. The rest of that entry's content and conclusion are accurate and unaffected. |
| [system] | this session: Read adapters/codex/skills/alawas-research-investigate-live-question/SKILL.md and adapters/github-copilot/skills/alawas-research-investigate-live-question/SKILL.md Platform Adapter sections | Checked director's claim (skills are not Claude-specific, non-agent-biased) against real files rather than accepting it. Confirmed largely correct: this repo already has adapters/codex/ (OpenAI Codex CLI) and adapters/github-copilot/ alongside adapters/claude-code/, generated by tools/generate-adapters.py from a single provider-agnostic canonical core (skills/core/*/SKILL.md, no Platform Adapter section at all). Read adapters/codex/skills/research-investigate-live-question/SKILL.md's Platform Adapter tail: it has NO Model tier section and no hardcoded model reference at all -- only a Runtime pin resolution section and capability-name mappings to Codex-native tools (read_file, list_dir, grep_search). This is real, existing precedent for a skill target with zero fixed-model binding. Nuance found: the github-copilot adapter, by contrast, DOES still hardcode 'The platform overlay resolves this to claude-sonnet-4-20250514' in its Model tier section -- so not every existing adapter is model-agnostic, only codex's demonstrably is. Conclusion: the skills' substantive content (governing principle, boundaries, stage workflow, evidence rules) is genuine provider-agnostic Markdown; what would be new is a fourth adapter target (e.g. deepseek/custom-api) mirroring codex's zero-model-tier-binding pattern, paired with a custom agent loop that feeds that adapter's SKILL.md as a system prompt to DeepSeek's API. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T19:09:03Z — create-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director confirmed the agency-mode direction: the MCP server should let another repo's session commission real skill reasoning, not just mechanical ws CLI calls. This reopens the exact technical precondition 2026-08-21-006 explicitly left unresearched (whether one process can programmatically invoke a real Claude Code/Agent session), now for a genuine reason. Framed as its own Inquiry rather than folded into 2026-08-21-010, since it's a materially different question than that Work Object's already-closed-out mechanical MCP server scope.
### 2026-08-21T19:10:23Z — prototype-ready-two-viable-mechanisms

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Official docs (code.claude.com/docs/en/agent-sdk/overview) confirm the technical precondition holds: the Claude Agent SDK runs a real agent loop in-process and auto-loads the exact alawas-* skills already installed at ~/.claude/skills/; a headless claude -p --output-format json subprocess route also exists, matching runtime/'s established subprocess pattern. Neither has been reality-tested yet -- routing to design as prototype-ready, not answered outright, since Success evidence item 2 (an actual reality check) is still open. Real cost/auth constraint surfaced: the SDK route needs a paid Anthropic API key, not covered by this session's own subscription context.
### 2026-08-21T19:12:56Z — reframed-neither-anthropic-mechanism-covers-deepseek

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director revealed the real constraint: DeepSeek API, not Anthropic's. WebFetch of code.claude.com/docs/en/agent-sdk/python confirmed the Agent SDK's model field is Anthropic-only (aliases or full Anthropic model IDs), no custom endpoint/provider override, described as architectural not configurable. The headless claude -p subprocess route is equally Anthropic-only -- it IS the Claude Code CLI. Both previously-identified mechanisms are eliminated for this actual use case. Reframed back to explore: the real falsifiable question is now whether a custom agent loop calling DeepSeek's API directly can load and follow the alawas-* skill .md files as prompt content, since skills are plain Markdown, not an SDK-internal feature.
### 2026-08-21T19:15:33Z — confirmed-skill-content-provider-agnostic-route-to-design

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Checked director's claim (skills not Claude-specific) against real files: confirmed. skills/core/*/SKILL.md canonical content is genuinely provider-agnostic; adapters/codex/'s existing Platform Adapter tail has zero hardcoded model binding, real precedent for a fourth adapter target with the same shape. github-copilot's adapter, by contrast, still hardcodes a Claude model -- not every existing adapter is agnostic, only codex's demonstrably is. Path forward: a new deepseek adapter target mirroring codex's pattern, plus the smallest loop proving DeepSeek actually follows one skill. Routing to design-tracer-bullet.
### 2026-08-25T22:20:00Z — Decision 1 recorded: DeepSeek adapter path superseded by OpenCodeAgentAdapter

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** WO 2026-08-25-001 Decision 15 built an OpenCodeAgentAdapter with zero model-tier binding supporting 75+ providers through Models.dev — exactly what this WO proposed building from scratch for DeepSeek alone. Decision 1 recorded as pass. Closing with this outcome.
### 2026-08-25T22:20:00Z — closed

- **State:** close
- **Status:** closed
- **Actor:** conductor
- **Rationale:** DeepSeek-specific adapter path superseded by WO 2026-08-25-001 Decision 15 (OpenCodeAgentAdapter). MCP agency-mode question (can a tool call invoke real skill reasoning on another repo) remains open as a potential successor inquiry.
### 2026-08-25T22:48:17Z — Closed: DeepSeek-specific adapter path superseded by OpenCodeAgentAdapter (WO 2026-08-25-001 Decision 15). OpenCode supports 75+ providers with zero model-tier binding, making a dedicated DeepSeek adapter unnecessary. MCP agency-mode question remains open as a potential successor inquiry.

- **State:** close
- **Status:** closed
- **Actor:** conductor
- **Rationale:** DeepSeek-specific adapter path superseded by OpenCodeAgentAdapter (WO 2026-08-25-001 Decision 15). OpenCode supports 75+ providers with zero model-tier binding, making a dedicated DeepSeek adapter unnecessary. MCP agency-mode question remains open as a potential successor inquiry.
