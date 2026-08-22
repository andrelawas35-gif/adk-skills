---
schema_version: 1
id: 2026-08-21-005
title: Multi-repo registry: Direction 2 successor to 2026-08-21-003
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T13:31:29Z
updated_at: 2026-08-21T13:56:23Z
next_action: Director decision: commit the full registry (read-path + write-path) as-is, extend further (fork/backup/restore), or investigate the 11-vs-12 test-count discrepancy first














---
## Intent

Build the repo registry design (Direction 2) that WO `2026-08-21-003` deferred:
a `.work-studio/repos.yaml`-style registry listing named target repos, each
with its `.work-studio` path and preferred checkpoint-DB location, so
`tools/ws` and `runtime/graph.py` can target more than one repo instead of one
`WS_REPO_ROOT` per invocation. This also closes the one confirmed operational
gap `2026-08-21-003` left open and accepted: the checkpoint/idempotency DB is
currently shared across sequential target repos (no per-repo keying).

**Successor of**: `2026-08-21-003` (closed; its recorded revisit trigger —
"if a real, current need for simultaneous multiple target repos emerges,
revisit toward Direction 2" — is why this object exists). Director selected
"Build the registry (Direction 2)" over the smaller "fix DB keying only"
option when this successor was created.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Registry design explored and a direction selected (develop-idea: Direction 2 selected) — design-tracer-bullet ran both the read-path and write-path assumption tests
- [x] Registry format lets `_resolve_repo_root()`'s effective input be read from the registry instead of requiring `WS_REPO_ROOT` pre-set — `run`/`resume` now accept `--repo NAME`, which sets `WS_REPO_ROOT` from `.work-studio/repos.json` for that invocation. `fork`/`backup`/`restore` and `--repo-all` on `run`/`resume` remain out of scope (the latter deliberately: untested semantics for running one `work_object_id` against multiple repos' distinct namespaces)
- [x] Checkpoint-DB path is keyed per registry entry — both for `inspect` and now `run`/`resume` (`--repo` resolves `checkpoint_db` from the registry entry when not given explicitly)
- [x] Selected direction implemented and independently verified, read path and write path: `inspect --repo`/`--repo-all` and `run`/`resume --repo` added to `runtime/graph.py`; `.work-studio/repos.json` registry format; 102-test baseline (11F/32E, one fewer failure than the 12F/32E baseline both `2026-08-21-003` and this WO's own read-path pass recorded — flagged as unexplained by this diff, plausibly test flakiness, not claimed as a fix); manual CLI smoke tests against real throwaway target repos confirmed correct per-entry isolation, error handling, and unchanged default behavior on both paths


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

### Decision 1 — Selected Direction 2: session-scoped multi-target registry, the graph iterates the registry itself

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Of the three directions generated (Direction 1: env-var-compatible name-alias registry; Direction 2: registry that the graph itself iterates across multiple targets in one invocation; Direction 3: decentralized self-declaring target repos), select Direction 2. Registry becomes a first-class input to `runtime/graph.py`'s orchestration: one invocation can accept a list of registry entries (or "all") and run the graph against each target repo, each with its own checkpoint DB and its own resolved repo root per iteration rather than per process. |
| **Authorization** | Director, this session, in response to a direct discriminating question ("What's the actual friction driving this successor?") |
| **Confidence** | high on the selection itself (director directly named the trigger, resolving the fork); low-to-medium on the design details (per-iteration checkpoint isolation, concurrent-vs-sequential execution) until a tracer bullet tests them |
| **Actor** | director |
| **Revisit trigger** | If simultaneous-target usage turns out to be rare in practice and the real day-to-day need is just naming/avoiding retyped paths, revisit toward Direction 1 (the smaller, env-var-compatible alias layer) as a fallback |
| **Rationale** | Director confirmed the actual friction is running one command against multiple target repos in a single invocation, not just avoiding retyped `WS_REPO_ROOT` paths -- Direction 1 doesn't address that at all. Direction 3 was ruled out separately on filesystem evidence: `C:\Users\Andre\Documents\Work_Studio\` currently contains no sibling target repos, so there is nothing for a self-declaring/scanning mechanism to discover yet. |

### Decision 2 — Accept tracer bullet: per-iteration checkpoint isolation, unmodified `inspect_thread` against two disposable sandbox DBs

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Test the riskiest assumption of Decision 1 (Direction 2) before designing any registry format or CLI flag: does calling the existing, unmodified `inspect_thread(thread_id, checkpoint_db)` (`runtime/graph.py:446`) against two disposable sandbox checkpoint DBs, back-to-back in one Python process, produce two independent, uncontaminated results? Read-path only (`inspect_thread`); write-path (`run`/`resume`) iteration explicitly deferred. No registry file, no `--repo` flag, no change to `_resolve_repo_root()` or `_default_checkpoint_db()`. |
| **Authorization** | Director: "accept the tracer bullet as scoped" -- consequence is `meaningful`, ordinary confirmation sufficient |
| **Confidence** | high that `inspect_thread` itself is safe to call twice (it's already a pure function taking an explicit path, per its signature); low-to-medium on SQLite connection lifecycle and any module-level state across iterations -- that's the assumption this tracer bullet exists to test |
| **Actor** | director |
| **Revisit trigger** | If either sandbox result contains the other's data, an exception occurs only on the second iteration, or the checkpoint-db path resolves incorrectly on either call, the per-process iteration model fails and Decision 1 needs revisiting toward a per-target subprocess boundary instead |
| **Rationale** | `inspect_thread` is the cheapest possible falsifier of "does anything leak across iterations" -- it already takes `checkpoint_db` as an explicit argument, so if leakage happens here it would happen anywhere in the graph. Testing the write path (`run`/`resume`) was considered and deferred: higher cost, and this read-path result gates whether that's even worth building next. |

### Decision 3 — Accept tracer bullet: write-path per-iteration isolation, mutating `WS_REPO_ROOT` between two real throwaway target repos in one process

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Test the write-path assumption deferred by Decision 2: does mutating `os.environ["WS_REPO_ROOT"]` between iterations of one Python process, then calling `run()` (which touches `_find_work_object`, writes a marker file, claims an idempotency receipt, and spawns a real `tools.ws validate` subprocess via `node2_validate`), correctly isolate each iteration -- no cross-repo marker-file writes, no idempotency-key collisions, no stale subprocess `cwd`. Two real throwaway target repos (each with one dummy Work Object satisfying `WorkObjectEnvelope`), sequential (not concurrent) iteration, distinct `checkpoint_db`/`idempotency_db`/`marker_file` per iteration. Not in scope: the `--repo`/`--repo-all` CLI surface on `run`/`resume` itself, genuine concurrency, `resume`/`fork` semantics, registry schema changes. |
| **Authorization** | Director: "accept the tracer bullet as scoped" -- consequence is `meaningful`, ordinary confirmation sufficient |
| **Confidence** | medium that per-call env-var mutation is safe -- both `_find_work_object`'s `_resolve_repo_root()` call and `node2_validate`'s are per-invocation reads, not cached at import time (grounded in reading the source directly), but this exact sequential-mutation pattern has never been exercised; every existing caller sets `WS_REPO_ROOT` once, outside the process, before launch |
| **Actor** | director |
| **Revisit trigger** | If either repo's marker file contains the other's Work Object ID, `node2`'s subprocess validates against the wrong repo, or the idempotency DB rejects a legitimate second claim due to a cross-target key collision, the in-process env-var-mutation model fails and Decision 1 needs revisiting toward a per-target subprocess boundary (spawn a fresh `runtime.graph run --repo <name>` process per target) instead |
| **Rationale** | Real throwaway repos, not fakes, because `node1`/`node2` need a real envelope to validate against and a real `tools.ws validate` subprocess call -- the read-path bullet could fake state via `graph.update_state`, but the write path's riskiest surface is exactly the parts that can't be faked without losing the risk being tested. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | grep across runtime/graph.py and tools/ws/*.py, this session | `WS_REPO_ROOT` is consumed in exactly one place, `_resolve_repo_root()` in `runtime/graph.py`. `tools/ws` has zero references to `WS_REPO_ROOT` -- it resolves its own workspace root independently. No existing registry, YAML/JSON repo list, or multi-target abstraction exists anywhere in the repo. |
| [system] | directory listing of `C:\Users\Andre\Documents\Work_Studio\`, this session | Only `andrelawas-work-studio` exists at that path -- no sibling target repos present. Rules out Direction 3's key assumption (target repos discoverable by shared-parent-directory scan) as currently unsupported by any real instance. |
| [decision] | director, this session | Director: "Simultaneous multi-repo runs (Direction 2)" -- resolves the discriminating gap between Direction 1 (name-alias for one-repo-at-a-time) and Direction 2 (one invocation touching multiple targets). |
| [system] | this session, uv run --python 3.11, scratch script under scratchpad | Tracer bullet run (Decision 2). Seeded two disposable sandbox checkpoint DBs (sandbox-a.sqlite, sandbox-b.sqlite) via graph.update_state (no full node1/node2 run -- avoids _find_work_object/_resolve_repo_root, out of scope). Called the existing, unmodified inspect_thread(thread_id, checkpoint_db) against each in one Python process, back-to-back. Result: sandbox-a-thread returned only MARKER_A_ONLY and its own thread_id; sandbox-b-thread returned only MARKER_B_ONLY and its own thread_id -- no cross-contamination, no exception on either call. Real repo untouched: git status after cleanup showed only the pre-existing WO-005/003 edits and pre-existing uncommitted phase7/hypothesis work (unrelated, from WO 2026-08-21-004); uv run triggered a routine lockfile sync of pyproject.tomls pre-existing dependency-groups entry, no new dependency added by this tracer bullet itself. Scratch script and both sandbox DBs deleted after the run. |
| [system] | this session, runtime/graph.py implementation + verification | Bounded implementation: added _repo_registry_path/_load_repo_registry/_resolve_registry_checkpoint_db to runtime/graph.py, and --repo/--repo-all (mutually exclusive with --checkpoint-db) to the inspect subcommand only -- read path, matching the tracer bullet's tested scope. Registry format: .work-studio/repos.json (JSON not YAML: zero new dependency, stdlib json, consistent with the codebase's dependency-free-by-design posture). Write-path (run/resume/fork/backup/restore) left untouched -- explicit non-goal per the tracer bullet. Verification: runtime/tests via unittest discover, 102 tests, 12 failures/32 errors -- matches WO 2026-08-21-003's recorded baseline exactly (99 tests same 12F/32E; +3 tests is the pre-existing, unrelated test_phase7_hypothesis.py from WO 2026-08-21-004), zero regression. Manual CLI smoke test against two disposable sandbox checkpoint DBs (same sandbox-a/sandbox-b pattern as the tracer bullet): --repo sandbox-a and --repo sandbox-b each returned only their own thread's marker value; --repo-all iterated both, correctly returning an empty values dict (not an error) for the thread that only exists in the other sandbox; --repo with an unknown name raised a clear KeyError; --repo combined with --checkpoint-db was rejected by argparse; no-flags behavior unchanged (still resolves to the original default checkpoint-db path). Real repo's .work-studio/repos.json was created temporarily for this smoke test and deleted afterward -- git status confirms no trace remains. Not yet committed. |
| [system] | this session, uv run --python 3.11, scratch script under scratchpad | Write-path tracer bullet run (Decision 3). Two real throwaway target repos (repo-a, repo-b), each with one minimal but schema-valid dummy Work Object (2026-08-21-901, 2026-08-21-902) satisfying WorkObjectEnvelope and tools.ws validate's full body-section requirements. Sequentially mutated os.environ[WS_REPO_ROOT] to each repo in turn, called the existing, unmodified run() with distinct checkpoint_db/idempotency_db/marker_file per iteration. First attempt failed node2 (tools.ws validate exit 1) because the initial dummy WO bodies were missing required sections (Success Evidence, Constraints, Decisions, Evidence Ledger, Open Questions, Next Move, History) and used a non-conforming ID format -- a fixture defect, not a mechanism defect; node1's marker-file isolation was already clean on that first attempt. Fixed fixtures to full schema-valid WOs and re-ran: both repos completed node1_completed=True and node2_completed=True, each marker file contained only its own repo's WO ID, no cross-contamination. Confirms node2_validate's per-call _resolve_repo_root() read and subprocess cwd genuinely follow WS_REPO_ROOT mutated mid-process, not a stale value from process start. Real repo untouched: git status after cleanup showed only pre-existing WO-005/003 edits, an unrelated new WO-006 file, and active.md (both from other in-progress director activity). Scratch script, both throwaway repos, and all generated checkpoint/idempotency/marker files deleted after the run. |
| [system] | this session, runtime/graph.py implementation + verification | Bounded implementation, write-path extension: added _resolve_registry_entry/_resolve_registry_repo_root to runtime/graph.py; --repo (mutually exclusive with --checkpoint-db) added to run and resume subparsers and to _legacy_main's shared parser. Deliberately did NOT add --repo-all to run/resume: unlike inspect (read-only, safe to loop one thread_id across every registry entry), --repo-all on run/resume would silently execute one work_object_id against multiple target repos' distinct Work Object namespaces -- untested by the tracer bullet (which used two different, per-repo work_object_ids) and not obviously correct semantics. Flagging as a deliberate non-implementation, not a silent gap. Verification: runtime/tests via unittest discover, 102 tests, 11 failures/32 errors -- one fewer failure than the 12F/32E baseline recorded by both 2026-08-21-003 and this WO's own earlier read-path pass; noting the discrepancy honestly rather than either claiming a fix or an exact match -- plausibly test-order/timing flakiness in the kill/resume regression tests, not something this change's diff (three new functions, --repo flag wiring, zero change to existing default-path behavior) would plausibly explain. Manual CLI smoke test against a real throwaway target repo + repos.json registry entry: run --repo and resume --repo both resolved WS_REPO_ROOT correctly and completed both nodes; unknown --repo name raised a clear KeyError; --repo combined with --checkpoint-db rejected by argparse; no-flags default behavior unchanged (correctly failed to find the throwaway WO in the real repo, proving WS_REPO_ROOT was not leaked from the --repo runs). Real repo's .work-studio/repos.json and any generated marker/idempotency files were created temporarily and deleted afterward -- git status confirms no trace remains. Not yet committed. |
## Open questions

- **Answered.** Per-iteration checkpoint isolation for the read path
  (`inspect_thread`) holds: the tracer bullet showed two disposable sandbox
  DBs, inspected back-to-back in one process, produced independent,
  uncontaminated results.
- **Answered.** Write-path (`run`/`resume`) per-iteration isolation holds:
  the write-path tracer bullet showed `os.environ["WS_REPO_ROOT"]` mutated
  between sequential `run()` calls against two real throwaway target repos
  produced independent, uncontaminated results (marker files, idempotency
  claims, and the real `tools.ws validate` subprocess all correctly followed
  the mutated value).
- **Answered.** Registry file format: `.work-studio/repos.json` (JSON, not
  literal YAML) -- zero new dependency, stdlib `json`, consistent with the
  codebase's dependency-free-by-design posture. `--repo`/`--repo-all` CLI
  surface: `inspect` has both; `run`/`resume` have `--repo` only --
  `--repo-all` deliberately not extended to the write path (untested,
  ambiguous semantics for one `work_object_id` across multiple repos'
  distinct namespaces).
- `fork`/`backup`/`restore` still require `WS_REPO_ROOT`/`--checkpoint-db`
  unchanged -- not extended, genuinely out of scope, not yet designed.
- Unexplained: the second full-suite run showed 11 failures/32 errors, one
  fewer failure than the 12F/32E baseline this WO's own read-path pass and
  `2026-08-21-003` both recorded. Flagged in the Evidence ledger as likely
  test-order/timing flakiness in the kill/resume regression tests, not
  attributed to this change.

## Next move

Read-path and write-path implementation both complete and verified: registry
(`.work-studio/repos.json`), `--repo`/`--repo-all` on `inspect`, `--repo` on
`run`/`resume`. Not yet committed. Awaiting director decision: commit as-is,
or extend further (`fork`/`backup`/`restore`, or investigate the 11-vs-12
test-count discrepancy) before committing.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T13:31:51Z — create-successor-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director created this as successor to closed WO 2026-08-21-003, selecting Direction 2 (repo registry) over the smaller per-repo-DB-keying-only option, to pursue 003's recorded revisit trigger: a real need for simultaneous multiple target repos.
### 2026-08-21T13:32:07Z — activate-explore

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Correcting frontmatter state to match the create-successor-and-activate history entry: divergent exploration of registry format and per-repo checkpoint-DB keying.
### 2026-08-21T13:34:57Z — direction-2-selected

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected Direction 2 (session-scoped multi-target registry, graph iterates the registry) over Direction 1 (name-alias for one-repo-at-a-time), after confirming the real friction is simultaneous multi-repo runs, not repeated path-typing. Direction 3 (decentralized self-declaring repos) ruled out separately: no sibling target repos exist yet to discover.
### 2026-08-21T13:38:05Z — accepted-tracer-bullet

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the per-iteration checkpoint-isolation tracer bullet (Decision 2): unmodified inspect_thread against two disposable sandbox checkpoint DBs, read-path only. Running it now.
### 2026-08-21T13:40:04Z — tracer-bullet-passed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Tracer bullet passed: two disposable sandbox checkpoint DBs, inspected back-to-back via unmodified inspect_thread in one process, produced independent uncontaminated results (no cross-contamination, no exception). Per-iteration checkpoint isolation confirmed for the read path. Write-path (run/resume) iteration and registry format/CLI surface remain undesigned. Routing to implement-bounded-change.
### 2026-08-21T13:45:43Z — implement-bounded-change-completed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Implemented the registry (.work-studio/repos.json) and --repo/--repo-all on the inspect subcommand only, matching the tracer bullet's tested read-path scope. Write-path (run/resume/fork) left untouched as an explicit non-goal. Zero regression: runtime/tests (102 tests) matched WO 2026-08-21-003's recorded baseline exactly. Manual CLI smoke test against two disposable sandbox DBs confirmed correct per-entry isolation, error handling, and unchanged default behavior. Not yet committed.
### 2026-08-21T13:46:42Z — resume-for-write-path-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Read-path implementation left uncommitted pending director decision. Director now wants a tracer bullet designed for the write path (run/resume/fork iteration over the registry) -- the piece explicitly deferred by Decision 2. Returning to design state for design-tracer-bullet.
### 2026-08-21T13:47:53Z — accepted-write-path-tracer-bullet

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the write-path tracer bullet (Decision 3): mutate WS_REPO_ROOT between iterations against two real throwaway target repos, testing run()'s marker-file/idempotency/subprocess-cwd isolation. Running it now.
### 2026-08-21T13:49:58Z — write-path-tracer-bullet-passed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Write-path tracer bullet passed: two real throwaway target repos, WS_REPO_ROOT mutated between sequential run() calls in one process, produced independent uncontaminated results (marker files, idempotency claims, node2 tools.ws validate subprocess all correctly followed the mutated WS_REPO_ROOT with no cross-repo leakage). Both read-path and write-path per-iteration isolation now confirmed. Routing to implement-bounded-change to extend the registry/--repo/--repo-all surface onto run/resume.
### 2026-08-21T13:56:23Z — write-path-implement-bounded-change-completed

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Extended --repo onto run and resume (mutually exclusive with --checkpoint-db), plus the shared legacy-CLI path. Deliberately did not add --repo-all to run/resume -- untested, ambiguous semantics for one work_object_id across multiple repos. Manual CLI smoke test against a real throwaway target repo confirmed correct WS_REPO_ROOT resolution, error handling, and unchanged default behavior on both run and resume. Full test suite: 11 failures/32 errors, one fewer failure than the 12F/32E baseline -- flagged as likely flakiness, not claimed as caused by this change. Not yet committed.
