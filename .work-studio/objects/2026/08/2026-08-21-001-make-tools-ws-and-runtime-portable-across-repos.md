---
schema_version: 1
id: 2026-08-21-001
title: Make tools/ws and runtime/ portable across repos
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T08:28:24Z
updated_at: 2026-08-21T13:00:12Z
next_action: Director decision: commit/merge tracer/repo-root-portability as-is, or decide separately on the fuller feature (packaging, checkpoint-DB policy, multi-repo orchestration remain non-goals)





---
## Intent

Make `tools/ws` and `runtime/` (LangGraph engine — `envelope.py`, `graph.py`,
`projection.py`) work against a `.work-studio/objects/` tree that lives in a
different repository from this one, so the studio can eventually operate as
"one system, any repo" rather than being pinned to this codebase.

## Success evidence

- [x] A disposable sandbox repo outside this repo has its own `.work-studio/objects/` (`%TEMP%\ws-portability-sandbox`, `git init`'d, uncommitted)
- [x] `tools/ws create` + `tools/ws validate`, run from inside that sandbox, read/write only the sandbox's tree (Leg A) — via a directory junction (no admin rights needed for a true symlink on this machine), `ws create` and `ws validate` both operated only on the sandbox; confirmed absent from this repo's own `.work-studio/objects/`
- [x] `envelope.py`/`graph.py`/`projection.py` accept an optional `repo_root` override — **fully confirmed; gap closed by implement-bounded-change**. Only `graph.py` needed a change: `envelope.py`/`projection.py`'s `_REPO_ROOT` use is sys.path bootstrap only (code location, correctly stays fixed) or an explicit `objects_dir` parameter already threaded by the caller (already portable by design). `_resolve_repo_root()` in `graph.py` consults `WS_REPO_ROOT` env var, defaulting to unchanged behavior when unset. `graph run` against the sandbox found and read the sandbox's Work Object correctly, and both `tracer.sqlite` and `idempotency.sqlite` landed only in the sandbox. The `dashboard-signals` leak (node 2's `tools.ws validate` subprocess running with `cwd=_REPO_ROOT` instead of the resolved root, so `tools/ws`'s CWD-based `_find_work_studio_root()` scanned this repo's objects instead of the sandbox's) is now closed: `cwd` is the resolved root, with `PYTHONPATH` set explicitly back to this repo so the `tools.ws` import still resolves regardless of `cwd`. Verified directly: `_find_work_studio_root()` returns the sandbox path when `cwd=sandbox`, and re-running the exact node-2 subprocess invocation against the sandbox produces no cross-repo warnings.
- [x] `runtime/tests/` stays green on the edited branch, before and after — 99 tests, identical 12 failures/32 errors before and after (diffed the exact failing-test-name sets; byte-for-byte identical), pre-existing and unrelated to this change
- [x] This repo's own `.work-studio/objects/` and `runtime/checkpoints/tracer.sqlite` are untouched by the sandbox run — `runtime/checkpoints/` doesn't even exist in this repo (never created); no new file for the sandbox's WO id appeared under this repo's `.work-studio/objects/`

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
| **Result** | pass |
| **Scope** | Whether to run the two-leg tracer bullet described in Intent/Success evidence as the next bounded step toward runtime/ portability |
| **Authorization** | Director: "Yes, accept and run the tracer bullet" — consequence is `meaningful`, ordinary confirmation is sufficient (no high-consequence ritual) |
| **Confidence** | high that Leg A works as-is (tools/ws already uses Path.cwd()); low-to-medium that Leg B cleanly redirects the LangGraph runtime end-to-end — that is the riskiest assumption this tracer bullet exists to test |
| **Actor** | director |
| **Revisit trigger** | Either leg fails to redirect cleanly (writes/reads still land in this repo), or `runtime/tests/` breaks on the edited branch |
| **Rationale** | `runtime/`'s three files hardcode their root to their own file location and are the actual blocker for cross-repo use; `tools/ws`'s portability is comparatively low-risk since `persistence.py`/`mutation_protocol.py` already prove the override pattern works in this codebase — bundling both legs into one sandbox test is cheaper than testing them separately |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | codebase inspection | tools/ws already reads Path.cwd(), so it should follow into any directory once physically present there; runtime/envelope.py:30, graph.py:51, projection.py:44 hardcode their root to their own file location; persistence.py:149 and mutation_protocol.py:199 already take an optional override, proving the pattern inside this codebase |
| [system] | this session, uv run --python 3.11 | Tracer bullet run. Leg A: sandbox at C:\Users\Andre\AppData\Local\Temp\ws-portability-sandbox, tools/ws junction-linked in (mklink /J, no admin needed), ws create + ws validate operated only on the sandbox tree, confirmed absent from this repo's own .work-studio/objects/. Leg B: added graph.py::_resolve_repo_root() consulting WS_REPO_ROOT env var (defaults unchanged); graph run against the sandbox correctly found/read the sandbox's Work Object, and tracer.sqlite/idempotency.sqlite landed only in the sandbox -- this repo's runtime/checkpoints/ was never created. runtime/tests: 99 tests, identical 12 failures/32 errors before and after (diffed failing-test-name sets byte-for-byte), pre-existing and unrelated. |
| [system] | this session, uv run --python 3.11, implement-bounded-change | implement-bounded-change: closed the dashboard-signals leak in runtime/graph.py node2_validate. Changed node 2's subprocess to cwd=resolved_root (was cwd=_REPO_ROOT always) with PYTHONPATH explicitly set back to this repo so python -m tools.ws still imports regardless of cwd. Verified: _find_work_studio_root() returns the sandbox path when invoked with cwd=sandbox (previously always returned this repo's path); replaying the exact node-2 subprocess call against the sandbox produced only the sandbox file's own file-integrity warning, no cross-repo dashboard-signals output. runtime/tests: 99 tests, byte-for-byte identical failing set (12 failures/32 errors) before and after this edit -- zero regression. No deviation from the accepted tracer-bullet boundary: change stayed inside runtime/graph.py, no tools/ws edits, no checkpoint-db default changes (those were already independently overridable via --checkpoint-db, outside the documented gap). Not yet committed -- lives on branch tracer/repo-root-portability. |
## Open questions

- **Fully resolved.** Redirecting via `WS_REPO_ROOT` lets the LangGraph
  runtime find, read, and checkpoint against a different repo's tree
  end-to-end, without falling back to this repo's data. The `dashboard-signals`
  leak (node 2's `tools.ws validate` subprocess consulting this repo's
  `objects_dir` instead of the resolved root) is closed: node 2's subprocess
  now runs with `cwd=` the resolved root and an explicit `PYTHONPATH` back to
  this repo so the `tools.ws` import still works. Verified directly against
  the sandbox, with zero regression in `runtime/tests`.

## Next move

Implementation complete and verified on branch `tracer/repo-root-portability`;
not yet committed or merged. Awaiting director decision: commit/merge as-is,
or treat this as sufficient proof-of-concept and decide separately whether/when
to build the fuller feature (packaging, checkpoint-DB location policy,
multi-repo orchestration remain explicit non-goals, not addressed here).

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T08:30:09Z — record-tracer-bullet-design

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Two-leg tracer bullet drafted for runtime/ portability (repo_root override) with tools/ws riding along; awaiting director acceptance of Decision 1
### 2026-08-21T09:25:56Z — accepted-tracer-bullet-running-legs

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted Decision 1 as scoped; running Leg A (sandbox + symlinked tools/ws) and Leg B (short-lived branch, defaulted repo_root override in runtime/) together against one throwaway sandbox repo
### 2026-08-21T09:34:33Z — tracer-bullet-passed-with-documented-gap

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Both legs of the tracer bullet ran. Leg A (tools/ws in a sandbox) fully passed. Leg B (repo_root override in graph.py via WS_REPO_ROOT) passed for the core find/read/checkpoint path with zero regression in runtime/tests, but exposed a real, narrow, non-blocking gap: node 2's validate subprocess still leaks this repo's own objects_dir into one advisory check (dashboard-signals) because tools/ws's root discovery is CWD-based. Routing to implement-bounded-change to build the real feature and close that gap.
### 2026-08-21T13:00:12Z — implement-bounded-change-completed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Implemented the accepted tracer-bullet feature in runtime/graph.py: WS_REPO_ROOT override plus the dashboard-signals leak fix (node 2's subprocess cwd now resolves correctly, with PYTHONPATH set explicitly for import resolution). Verified directly against the sandbox with zero regression in runtime/tests. No deviation from the accepted boundary. Not yet committed -- awaiting director decision on branch tracer/repo-root-portability.
