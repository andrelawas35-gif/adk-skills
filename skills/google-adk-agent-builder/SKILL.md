---
name: google-adk-agent-builder
description: >
  Build and iterate on local Google ADK agents in Python.
  Use when: scaffolding a new ADK app; creating or editing `agent.py`,
  `__init__.py`, `.env`, or local tests; adding tools or multi-agent flows;
  wiring session, artifact, or memory services; running `adk create`,
  `adk run`, `adk web`, or `adk api_server`; turning a workflow (tutoring,
  paper reading, retrieval, planning, research) into an ADK agent
  architecture. Always refresh against official ADK docs before
  implementing SDK details — the framework changes quickly.
---

# Google ADK Agent Builder

## Overview

Build Google ADK agents locally first. Grow into larger systems only after the
local loop works. Prefer official ADK docs and the installed CLI over memory
when SDK behavior, file layout, or command flags matter.

## Don't Use When

- Building non-ADK Python agents (LangChain, AutoGen, custom).
- Deploying to production cloud infrastructure without first validating locally.
- The user only needs a one-shot script, not an agent with a conversation loop.
- Writing ADK evals or optimization pipelines — those are separate concerns.

## Workflow

### Step 1 — Verify the toolchain

Run `pip show google-adk` and `adk --help`. If `adk` is not on `PATH`, use
the full path to `adk.exe` from the user's Python Scripts directory.

**Check**: `pip show google-adk` returns a version and `adk --help` prints
usage before you proceed.

### Step 2 — Refresh from official docs

Read [references/adk-patterns.md](references/adk-patterns.md) for the current
CLI shape, scaffold layout, and documented patterns. Then browse the linked
official doc pages for any feature the user's request touches. ADK evolves
quickly — never assume a method signature or config key from memory.

**Check**: You've confirmed the ADK version and scanned the relevant doc page
for breaking changes since the last skill update.

### Step 3 — Choose the architecture

Walk this decision tree:

```
User needs one conversational flow?
  └─ Yes → Single root agent (stop here unless more is needed)

Agent must read files, search, call APIs, or transform data?
  └─ Yes → Add Python tools to the root agent

Multiple roles with genuinely different instructions?
  └─ Yes → Add sub-agents (tutor, examiner, reader, planner, etc.)

Need continuity across runs (memory, sessions, artifacts)?
  └─ Yes → Wire session/artifact/memory services
```

**Rule of thumb**: one agent first, tools second, multi-agent last. If one
agent can do the job cleanly, keep one agent.

**Check**: You can explain why you chose N agents and M tools in one sentence.

### Step 4 — Scaffold the project

If no ADK project exists: `adk create <app_name>` from the target parent
directory. Inspect the generated files before editing. Expect a minimal
scaffold: `agent.py`, `__init__.py`, `.env`, `.gitignore`.

If a project already exists: edit in place. Don't re-scaffold.

**Check**: `agent.py` exists and imports `Agent` from
`google.adk.agents.llm_agent`.

### Step 5 — Map the request to ADK primitives

| User need | ADK primitive |
|-----------|---------------|
| Main chat behavior | Root agent `instruction` |
| Deterministic side-effect (file I/O, API call) | Python tool |
| Distinct conversational role | Sub-agent |
| Long-running or replayable steps | Session state or external storage |
| Cross-run continuity | Artifact or memory service |

Keep `instruction` concise and behavioral. Put process into tools and code,
not giant prompts.

**Check**: Every user requirement maps to exactly one ADK primitive.

### Step 6 — Implement the thinnest working slice

Start with:
- One agent
- One tool
- One prompt path
- One testable user outcome

Avoid deployment, hosted memory, or evaluation infrastructure until local
runs produce useful output.

**Check**: You can run the agent locally and get a meaningful response to a
single test prompt.

### Step 7 — Run and validate

| Goal | Command |
|------|---------|
| Fastest feedback | `adk run <agent_path>` |
| Interactive local UI | `adk web <agents_dir>` |
| HTTP API for another app | `adk api_server <agents_dir>` |

Fix any import errors, missing env vars, or tool exceptions before moving on.

**Check**: The agent responds correctly to at least one happy-path prompt and
one edge-case prompt.

### Step 8 — Ground the outputs

For research, learning, or tutoring agents:
- Cite the source passage for each factual claim.
- Distinguish direct extraction from model inference.
- State when a conclusion is uncertain.
- Prefer short explanations followed by recall questions.

**Check**: A user can trace any factual claim back to a source or see a clear
"this is inferred" marker.

## Learning-System Specialization

When the user is building a tutor, paper reader, or self-study system, apply
these extra rules on top of the core workflow:

### Separate the concerns

Split behavior into distinct roles. Each can be a tool or sub-agent:

| Role | Responsibility |
|------|----------------|
| Source reader | Extract concepts, claims, methods, vocabulary from sources |
| Curriculum builder | Map dependencies, order topics, decide what to learn next |
| Tutor | Explain concepts, adapt to learner level, ask recall questions |
| Examiner | Generate quizzes, grade responses, track misconceptions |

### Store state outside the prompt

When the system needs continuity across sessions, keep these outside the
agent prompt:

- Source metadata (title, author, page markers)
- Concept cards and glossary entries
- Misconceptions and error patterns
- Quiz history and scores
- Review schedule (spaced repetition)

Use ADK session state, artifact service, or plain files/SQLite — whichever
fits the user's complexity tolerance.

### Require citations

Every claim drawn from a source must reference the source. The tutor must
distinguish "the paper says X" from "I infer Y from the paper."

### Favor recall over explanation

The tutor should ask questions that force active recall, not just deliver
explanations. Summaries are intermediate artifacts — the real product is the
learner's recall, questions, and review history.

## Design Rules (Quick Reference)

1. **Local first**: No cloud deployment unless explicitly requested.
2. **Concise instructions**: Behavior lives in tools and code, not mega-prompts.
3. **Plain Python tools**: For PDF parsing, note extraction, metadata cleanup,
   quiz generation, and other deterministic work.
4. **Separate ingestion from tutoring**: A paper reader and a tutor share
   storage, not the same prompt.
5. **Artifacts over chat**: Store summaries and extracted data as artifacts.
   The chat is for interaction, not persistence.

## References

Read [references/adk-patterns.md](references/adk-patterns.md) for:

- Current ADK CLI commands and local dev flow
- Starter project layout from the installed `google-adk` scaffold
- Recommended agent patterns for tutoring and research workflows
- Current official documentation links to refresh before implementation
