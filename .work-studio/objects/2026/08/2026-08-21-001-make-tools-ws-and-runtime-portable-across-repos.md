---
schema_version: 1
id: 2026-08-21-001
title: Make tools/ws and runtime/ portable across repos
type: project
status: active
state: design
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T08:28:24Z
updated_at: 2026-08-21T08:30:09Z
next_action: Awaiting director acceptance of Decision 1 (tracer bullet as scoped)
---
## Intent

Make `tools/ws` and `runtime/` (LangGraph engine — `envelope.py`, `graph.py`,
`projection.py`) work against a `.work-studio/objects/` tree that lives in a
different repository from this one, so the studio can eventually operate as
"one system, any repo" rather than being pinned to this codebase.

## Success evidence

- [ ] A disposable sandbox repo outside this repo has its own `.work-studio/objects/`
- [ ] `tools/ws create` + `tools/ws validate`, run from inside that sandbox, read/write only the sandbox's tree (Leg A)
- [ ] `envelope.py`/`graph.py`/`projection.py` accept an optional `repo_root` override that, when set, redirects both Work Object reads/writes and checkpoint state to the sandbox — with no observable change to existing callers when unset (Leg B)
- [ ] `runtime/tests/` stays green on the edited branch, before and after
- [ ] This repo's own `.work-studio/objects/` and `runtime/checkpoints/tracer.sqlite` are untouched by the sandbox run

## Constraints and non-goals

**Constraints:**
- Sandbox is local, throwaway, uncommitted — no network, no push, no production repo, no other person's data
- `runtime/` edit lives on a short-lived local git branch only
- `repo_root` override must default to today's `Path(__file__)`-derived value when unset — zero behavior change for existing callers

**Non-goals:**
- Packaging `tools/ws` (no `pip install`, no console-script entry point)
- Deciding where the checkpoint DB lives long-term
- Any multi-repo orchestration framework

## Decisions and revisit triggers

### Decision 1 — Accept tracer bullet: sandbox repo (Leg A, tools/ws) + defaulted repo_root override (Leg B, runtime/)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pending |
| **Scope** | Whether to run the two-leg tracer bullet described in Intent/Success evidence as the next bounded step toward runtime/ portability |
| **Authorization** | Awaiting director confirmation — consequence is `meaningful`, so ordinary confirmation is sufficient (no high-consequence ritual) |
| **Confidence** | high that Leg A works as-is (tools/ws already uses Path.cwd()); low-to-medium that Leg B cleanly redirects the LangGraph runtime end-to-end — that is the riskiest assumption this tracer bullet exists to test |
| **Actor** | director (pending), proposed by conductor |
| **Revisit trigger** | Either leg fails to redirect cleanly (writes/reads still land in this repo), or `runtime/tests/` breaks on the edited branch |
| **Rationale** | `runtime/`'s three files hardcode their root to their own file location and are the actual blocker for cross-repo use; `tools/ws`'s portability is comparatively low-risk since `persistence.py`/`mutation_protocol.py` already prove the override pattern works in this codebase — bundling both legs into one sandbox test is cheaper than testing them separately |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | codebase inspection | tools/ws already reads Path.cwd(), so it should follow into any directory once physically present there; runtime/envelope.py:30, graph.py:51, projection.py:44 hardcode their root to their own file location; persistence.py:149 and mutation_protocol.py:199 already take an optional override, proving the pattern inside this codebase |

## Open questions

- Does redirecting `envelope.py`/`graph.py`/`projection.py` via `repo_root` actually let the LangGraph runtime read/write a different repo's `.work-studio/objects/` tree end-to-end, including checkpoint state, without silently falling back to this repo's own data? (the tracer bullet's riskiest assumption, unresolved until run)

## Next move

Awaiting director acceptance of Decision 1 (tracer bullet as scoped). On accept:
run Leg A (sandbox + symlinked `tools/ws`) and Leg B (short-lived branch, defaulted
`repo_root` override in the three `runtime/` files) together against one throwaway
sandbox repo, per Success evidence. Pass → route to `alawas-engineering-implement-bounded-change`
to make `repo_root` a real committed feature. Fail → return to Open questions with
the specific failure point recorded.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T08:30:09Z — record-tracer-bullet-design

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Two-leg tracer bullet drafted for runtime/ portability (repo_root override) with tools/ws riding along; awaiting director acceptance of Decision 1
