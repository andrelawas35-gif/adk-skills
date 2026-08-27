---
schema_version: 1
id: 2026-08-21-003
title: Full one-system-any-repo feature: package tools/ws, checkpoint-DB policy, multi-repo orchestration
type: project
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [architecture, engineering]
created_at: 2026-08-21T13:02:59Z
updated_at: 2026-08-21T19:18:35Z
next_action: Director decision: close this Work Object, or hold open pending anything further














---
## Intent

Build the full "one system, any repo" feature on top of the proven
`WS_REPO_ROOT` mechanism (WO `2026-08-21-001`, tracer bullet, merged
`c57f90e`): make `tools/ws` installable as a real package, decide where the
LangGraph checkpoint database should live long-term for cross-repo use, and
support orchestrating more than one target repo — rather than the tracer's
one-repo-per-invocation env var.

**Successor of**: `2026-08-21-001` (tracer bullet closed; these three items
were its explicit Non-goals, now brought into scope by director decision).

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Directions for the three components (packaging, checkpoint-DB policy, multi-repo orchestration) generated and selected — Direction 1 (minimal trio) selected
- [x] Packaging tracer bullet passed: console script runs standalone from an arbitrary directory (correct existing error behavior), `from tools.ws import schema` / `from tools.ws.sections import VALID_EVIDENCE_TAGS` resolve identically post-packaging, zero new runtime dependency
- [x] Selected direction(s) implemented and verified per their own bounded implementation cycle: packaging (`tools/pyproject.toml`, verified against the real `tools/ws/` via editable install -- console script standalone, `tools.ws.__file__` resolves to the real source, zero new dependency), computed checkpoint-DB default (`runtime/graph.py::_default_checkpoint_db()`, verified unset/set behavior directly), multi-repo left as-is (no code change -- verified by inspection, nothing to implement)


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

### Decision 1 — Selected Direction 1: minimal trio, three small independent patches

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Build all three components now, as separate, independently revertible patches: pip-installable `tools/ws`, a computed platform-appropriate checkpoint-DB default (no new dependency), and multi-repo orchestration left as one `WS_REPO_ROOT` per invocation (no registry) |
| **Authorization** | Director: "Direction 1, do all three now" |
| **Confidence** | high that one-repo-at-a-time is sufficient (director directly confirmed this, ruling out Direction 2's registry); medium on packaging's smallest test until it's actually run |
| **Actor** | director |
| **Revisit trigger** | If a real, current need for simultaneous multiple target repos emerges, revisit toward Direction 2 (registry) as a later successor rather than retrofitting these three patches |
| **Rationale** | Director confirmed one-repo-at-a-time is the real need, ruling out Direction 2; chose breadth (all three now) over Direction 3's sequential/deferred approach — each patch stays small and independently revertible, so bundling them doesn't add coupling risk |

### Decision 2 — Accept tracer bullet: packaging risk, scratch venv testing console-script + tools.ws import paths

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Of Direction 1's three patches, test only the packaging one via a tracer bullet (the other two -- checkpoint-DB default, multi-repo no-op -- are low-risk and proceed as direct small implementation, no tracer needed). Scratch copy of tools/ws + scratch pyproject.toml + disposable venv, testing (a) the console-script entry point runs standalone, (b) `from tools.ws import schema` / `from tools.ws.sections import VALID_EVIDENCE_TAGS` resolve identically post-packaging -- the exact imports runtime/envelope.py, runtime/mutation_protocol.py, and runtime/projection.py already depend on |
| **Authorization** | Director: "Yes, accept and run it" -- consequence is `meaningful`, ordinary confirmation sufficient |
| **Confidence** | high that the console script itself will work (mechanical); low-to-medium that packaging won't require restructuring the import path those three runtime/ files depend on -- that's the assumption this tracer bullet exists to test |
| **Actor** | director |
| **Revisit trigger** | Either the console script fails standalone, or either import path breaks/resolves to something other than the expected installed location |
| **Rationale** | Packaging is the one patch whose failure would invalidate the most downstream work -- runtime/'s three files already import `tools.ws` directly, so a packaging approach that changes that import path breaks existing code, not just the new packaging feature |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | grep/read across pyproject.toml, tools/ws/atomic.py, runtime/graph.py, .gitignore, this session | Codebase check: no packaging pattern exists anywhere in this repo -- pyproject.toml (for runtime/) explicitly declares [tool.uv] package = false, and tools/ws/atomic.py's own docstring states tools/ws stays dependency-free stdlib by design. No XDG/platformdirs usage anywhere for checkpoint-DB-style paths (grep across all .py files, zero hits outside .venv/site-packages). No pre-existing multi-repo registry concept (grep for registry/repos.yaml/repos.json across the repo, zero hits outside unrelated langsmith site-packages). All three components are genuinely greenfield -- nothing to extend, only new design. |
| [decision] | director, this session | Director: 'Just one repo at a time for now.' Resolves the multi-simultaneous-repo open question -- rules out Direction 2 (registry). Directions 1 (minimal trio) and 3 (package first, defer rest) remain live. |
| [system] | this session, scratch venv + pip install -e | Packaging tracer bullet run. Scratch copy of tools/ws under C:\Users\Andre\AppData\Local\Temp\ws-packaging-tracer\src\tools\ws, scratch pyproject.toml ([project.scripts] ws = tools.ws.__main__:main, dependencies=[], setuptools build backend), pip install -e into a disposable venv. Result: (a) installed ws console script ran standalone from an arbitrary directory with no repo checkout present, producing the correct existing error ('.work-studio/ not found ... Run ws init first') rather than crashing; (b) from tools.ws import schema and from tools.ws.sections import VALID_EVIDENCE_TAGS both resolved correctly to the installed package location (confirmed via __file__, not falling back to the real repo); (c) pip list --format=freeze showed only pip and the package itself -- zero new runtime dependency. Real repo's tools/ws and python -m tools.ws invocation were never touched (git status confirms only the two WO files changed). Scratch venv and copy deleted after the test. |
| [system] | this session, uv run --python 3.11 + disposable venv, implement-bounded-change | implement-bounded-change, all three patches: (1) Packaging: added tools/pyproject.toml (package-dir mapping tools.ws -> ws, no duplication/symlink -- single source of truth). Verified against the real repo (not scratch): pip install -e ./tools into a disposable venv; ws.exe validate ran standalone from an arbitrary directory with the correct existing error; tools.ws.__file__ resolved to the real tools/ws/__init__.py; pip list showed only pip + the package itself. Cleaned up a leftover *.egg-info build artifact and added it to .gitignore. (2) Checkpoint-DB default: added _default_checkpoint_db() to runtime/graph.py, threaded into all 8 argparse defaults. Verified directly: WS_REPO_ROOT unset returns the unchanged repo-relative default; set returns a platform-appropriate user-data directory (LOCALAPPDATA on this machine). Known, recorded gap: doesn't key by which repo WS_REPO_ROOT pointed at -- explicit --checkpoint-db avoids collision; left for a future revision. (3) Multi-repo: no code change, verified by inspection -- WS_REPO_ROOT already supports exactly one target per invocation as designed. runtime/tests (99 tests) and the full tools test suite (439 tests) both matched their established pre-existing baselines exactly (12 failures/32 errors; 2 failures/3 errors) -- zero regression. generate-adapters.py --check stayed clean (no drift from the new tools/pyproject.toml). No deviation from the accepted boundary. Not yet committed. |
| [system] | this session, independent verification against committed HEAD, two live sandbox repos | Release-evidence verification (independent re-run against committed ef1c4cc, not just the implementer's own check). Packaging: verified -- fresh venv, ws console script standalone, tools.ws.__file__ resolved to real source, zero new dependency. Checkpoint-DB default: verified both branches directly, plus a live end-to-end graph run (WS_REPO_ROOT set, no --checkpoint-db flag) that correctly created the checkpoint DB at the new computed default location -- proves the argparse wiring is real, not just the helper function in isolation. Multi-repo: not applicable, confirmed by inspection. Operational check beyond what implementation covered: ran the graph against two different sandbox repos in sequence -- both used the identical checkpoint/idempotency DB path, confirming the recorded 'known gap' (no per-repo keying) is real and observable, not theoretical. No error resulted (thread IDs differed) but idempotency-receipt state is shared across sequential targets. No privacy/security boundary applies -- everything local and disposable. No deployment or release claim made. |
## Open questions

- **Answered.** Director: "Just one repo at a time for now." Rules out
  Direction 2 (registry) — no multi-simultaneous-repo need exists right now.
  Directions 1 and 3 remain live; both already assumed one-repo-at-a-time.
- **Resolved.** Packaging `tools/ws` does not conflict with "dependency-free
  stdlib": the tracer bullet's `pip list --format=freeze` showed only the
  package itself installed, no new runtime dependency. Confirmed, not just
  inferred.

## Next move

All three patches implemented, independently verified against committed
`ef1c4cc`, and committed. Release-evidence verification found no failed
criteria; the one confirmed gap (checkpoint/idempotency DB shared across
sequential targets, no per-repo keying) was already an accepted non-fix, now
observed rather than theoretical. Awaiting director decision to close.

### Direction 1: Minimal trio — three small, independent patches

- **Core idea**: Give `tools/ws` a lightweight `pyproject.toml` + console-script
  entry point (pip-installable); default the checkpoint DB to a
  platform-appropriate user-data directory when `WS_REPO_ROOT` is set (no new
  dependency, just a computed default); leave multi-repo orchestration as-is
  — one `WS_REPO_ROOT` per invocation, no new registry or switcher.
- **Distinctness claim**: Smallest possible version of "all three in scope" —
  each piece is a standalone, independently revertible patch with no shared
  design surface between them.
- **Key assumption**: One-repo-at-a-time is actually sufficient for real use;
  a registry/orchestrator would be solving a problem that doesn't exist yet.
- **Smallest test**: Package `tools/ws`, `pip install -e` it in a throwaway
  venv, run `ws --help` from an arbitrary directory with no repo checkout
  present.

### Direction 2: Repo registry as the unifying primitive

- **Core idea**: Design a single `.work-studio/repos.yaml`-style registry
  listing named target repos, each with its `.work-studio` path and preferred
  checkpoint-DB location. `tools/ws` and `runtime/graph.py` both read this
  registry instead of one-off env vars; packaging becomes a secondary,
  easier win once the registry format is stable.
- **Distinctness claim**: The only direction that actually solves *multi*-repo
  (more than one target at a time) rather than one-repo-at-a-time; the other
  two components become consequences of this one design decision instead of
  separate patches.
- **Key assumption**: Multiple simultaneous target repos is a real, current
  need — not speculative future-proofing (see Open questions).
- **Smallest test**: Hand-write a two-entry `repos.yaml` pointing at two
  throwaway sandboxes, and get `_resolve_repo_root()` to read the registry by
  name instead of `WS_REPO_ROOT`, for one of the two.

### Direction 3: Package first, defer the rest

- **Core idea**: Ship pip-installable `tools/ws` now as its own bounded
  Work Object — the most independently valuable and lowest-risk piece (usable
  from any project without cloning this repo). Explicitly defer checkpoint-DB
  policy and multi-repo orchestration to future successor Work Objects,
  opened only if real cross-repo usage actually materializes.
- **Distinctness claim**: Sequential, not parallel — unlike Direction 1
  (all three now, separately) this does only one thing now and treats the
  other two as *not yet justified*, not just *separately scoped*.
- **Key assumption**: Packaging is valuable on its own merits regardless of
  whether checkpoint-DB policy or multi-repo orchestration ever get built.
- **Smallest test**: Same as Direction 1's packaging test, but stop there —
  no checkpoint-DB or registry work follows regardless of outcome.

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T13:03:19Z — create-successor-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director expanded scope past WO 2026-08-21-001's tracer-bullet non-goals (packaging, checkpoint-DB policy, multi-repo orchestration) after the tracer merged. Created as a successor project rather than reopening the closed/merged tracer object; three interrelated architectural pieces warrant divergent exploration before committing to an approach.
### 2026-08-21T13:12:00Z — direction-1-selected

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected Direction 1 (minimal trio: pip-installable tools/ws, computed checkpoint-DB default, multi-repo orchestration left as-is) over Direction 3 (package-first, defer rest). Direction 2 already ruled out by the one-repo-at-a-time answer.
### 2026-08-21T13:15:06Z — accepted-packaging-tracer-bullet

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the packaging tracer bullet (Decision 2): scratch venv testing console-script entry point and the tools.ws import paths runtime/ already depends on. Running it now.
### 2026-08-21T13:17:13Z — packaging-tracer-bullet-passed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Packaging tracer bullet passed all three checks: console script standalone, tools.ws import paths identical post-packaging, zero new runtime dependency. Routing to implement-bounded-change for packaging plus the other two low-risk patches.
### 2026-08-21T13:23:54Z — implement-bounded-change-completed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** All three of Direction 1's patches implemented and verified: tools/pyproject.toml (packaging), runtime/graph.py computed checkpoint-DB default, multi-repo left as-is (no code change needed). Zero regression: runtime/tests and the full tools test suite both matched their established pre-existing baselines exactly. No deviation from the accepted boundary. Not yet committed.
### 2026-08-21T13:25:33Z — committed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Director committed all three patches (ef1c4cc).
- **Commit:** ef1c4cc
### 2026-08-21T13:28:27Z — release-evidence-verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Independent release-evidence verification against committed ef1c4cc: all three accepted criteria verified (packaging, checkpoint-DB default, multi-repo no-op). No release/deployment claim. One confirmed operational gap: checkpoint/idempotency DB shared across sequential target repos -- already an accepted non-fix, now observed directly rather than theoretical.
### 2026-08-21T13:29:14Z — Closed: All three patches (packaging, computed checkpoint-DB default, multi-repo no-op) implemented, independently verified against committed ef1c4cc, and committed (ef1c4cc). One confirmed, accepted-as-non-fix gap: checkpoint/idempotency DB is shared across sequential target repos (no per-repo keying) -- observed directly during verification, not just theorized. No deployment/release involved; this was local dev tooling.

- **State:** close
- **Status:** closed
- **Actor:** director
- **Rationale:** All three patches (packaging, computed checkpoint-DB default, multi-repo no-op) implemented, independently verified against committed ef1c4cc, and committed (ef1c4cc). One confirmed, accepted-as-non-fix gap: checkpoint/idempotency DB is shared across sequential target repos (no per-repo keying) -- observed directly during verification, not just theorized. No deployment/release involved; this was local dev tooling.
### 2026-08-21T19:18:35Z — Reconciled pyproject.toml with the working editable install

- **State:** close
- **Status:** closed
- **Actor:** claude-code
- **Rationale:** Post-close follow-up: the packaging patch's working install (tools.ws / work-studio-ws, work-studio-mcp) was editable-installed out-of-band and not captured by uv.lock -- a uv sync would have silently dropped the ws console script. Declared a uv workspace (root pyproject.toml: [tool.uv.workspace] members = ["tools", "mcp_server"]; mcp_server/pyproject.toml switched its work-studio-ws source from a raw path to {workspace = true}), regenerated uv.lock, and verified: uv sync reproduces the install, ws --version resolves from an unrelated cwd, uv run ws works via the workspace entrypoint, and the opt-in test group (hypothesis, mcp) still resolves on demand. Not committed.
