---
schema_version: 1
id: 2026-08-22-003
title: Refine alawas-research-produce-report toward a Deep-Research-style dynamic workflow
type: inquiry
status: active
state: build
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T10:03:33Z
updated_at: 2026-08-22T11:14:27Z
next_action: Implement Decision 1 bounded iterative re-planning loop as a separate change










---
## Intent

Explore how `alawas-research-produce-report` (and/or the
`alawas-research-investigate-live-question` it composes) could be refined
toward something closer to Claude's Deep Research: a more dynamic, agentic
research workflow that searches the web iteratively, spawns subagents, and
adopts other Deep-Research-style capability, rather than today's fixed
decompose-once-then-invoke-once-per-sub-question pattern.

This is exploration only. No direction is selected yet; directions are
recorded below for the director to choose from.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] At least three materially distinct directions generated and presented
      -- four generated
- [x] Director has selected a direction (or explicitly declined to select)
      -- Direction 1 selected, Decision 1
- [x] Information gaps that would discriminate between directions are
      surfaced, not silently assumed -- infra-dependency gap resolved as a
      discoverable fact (Direction 2 eliminated, not a preference call);
      scope and budget-tolerance gaps remain open, carried forward below


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

### Decision 1 — Adopt Direction 1 (bounded iterative re-planning), reject Direction 2 outright

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Direction 2 (Workflow-tool orchestration) is rejected outright, not merely deprioritized -- confirmed non-portable, not a preference call (see Evidence ledger). Of the remaining three, Direction 1 is adopted: after the initial fixed sub-question decomposition and its `investigate-live-question` outcomes return, `produce-report` generates **at most one** additional round of new sub-questions drawn from gaps the initial outcomes reveal -- not the same sub-questions reworded. If the initial round's outcomes reveal no genuine gap, no second round runs at all. If a genuine gap exists, exactly one re-planning round runs, invoking `investigate-live-question` for the new sub-questions via `subagent_spawn` (already a portable, declared capability on all three generated adapters -- claude-code, codex, github-copilot). Hard cap: 2 rounds total (initial + at most 1 re-plan), regardless of findings -- never more, even if the second round also reveals gaps. |
| **Authorization** | Director: "Accept Direction 1" |
| **Confidence** | medium -- Direction 1 is the best fit to the stated intent ("dynamic workflow... release a subagent") and the only capability-adding option confirmed portable across all three adapters, but its key assumption (today's fixed one-shot decomposition actually misses real sub-questions) is untested against a real report run |
| **Actor** | director |
| **Revisit trigger** | Run Direction 1's own smallest test (one real broad request through `produce-report` in its current, unmodified form; check afterward whether a sub-question was missing that only became obvious once the first round's outcomes were in) before or shortly after implementation. If that check finds no missing sub-question, the key assumption is false and this decision should be revisited toward Direction 4 (transparency only, no capability increase) instead. Separately: if the 2-round hard cap is ever found insufficient in practice, that is a new decision, not a silent cap increase. |
| **Rationale** | Direction 2 is rejected because `subagent_spawn` maps to a single-subagent primitive (`Task` / `runSubagent`) on every generated adapter -- the declarative pipeline/parallel/verify `Workflow` tool Direction 2 depends on has no cross-platform equivalent, and adopting it would break this repo's own stated architecture (canonical core generating three portable adapters). Direction 1 is chosen over Direction 3 because it matches the director's stated intent ("dynamic workflow... release a subagent") more directly -- each re-planning round is additional `subagent_spawn` calls, a multi-agent pattern, versus Direction 3's single investigator searching deeper. Direction 1 is chosen over Direction 4 because Direction 4 solves a different problem (visibility into existing power) than the one asked for (more research power) -- recommending it instead would answer an unasked question. |

**Edge case noted:** an unbounded or poorly-gated re-planning round could thrash -- generating sub-questions that are cosmetically new but carry no new information. The "at most one round, only if a genuine gap exists" gate exists specifically to prevent this; the actual gap-detection heuristic (what counts as "genuine") is design work, not yet specified here.

**Assumption that could invalidate this:** that today's fixed one-shot decomposition genuinely misses real sub-questions often enough to justify the added cost and complexity. If the revisit-trigger test finds this false, the added round is pure cost with no benefit.

**Future friction:** even a 2-round hard cap materially increases token/time cost per report versus today's single pass. No mechanism yet decides *when* the cap itself should be reconsidered (e.g., after N report runs) -- that would be a future decision, not an automatic escalation.

### Decision 3 — Repair research-produce-report conformance gaps

| Field | Value |
|-------|-------|
| **Decision type** | authority |
| **Result** | pass |
| **Scope** | Add `research-produce-report` to the kernel manifest, add its missing Skill Grilling Profile and behavioral-fixture registration, add the exact high-consequence mutation gate required by generated-adapter tests, regenerate adapters/skill map, reinstall Codex, and verify. Excludes implementing Decision 1's iterative re-planning loop. |
| **Authorization** | Director: "fix the research-produce-report gaps" |
| **Confidence** | high — basis: each gap is directly reproduced by a deterministic kernel or test failure and has a narrow canonical owner. |
| **Actor** | director |
| **Revisit trigger** | A repair requires changing the accepted research workflow, deliverable contract, lifecycle schema, or two-round re-planning decision. |
| **Rationale** | Restore the existing skill to the same packaging, authority, grilling, and kernel contracts every other canonical skill must satisfy without expanding its behavior. |

### Decision 2 — Accept tracer bullet: test Direction 1's key assumption using a real question

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Run today's **unmodified** `alawas-research-produce-report` (no code or SKILL.md changes) on one real question: "How do I build the visual central command center for my Work Studio based on its current system?" -- decompose into sub-questions, invoke `alawas-research-investigate-live-question` once per sub-question, then manually inspect the outcomes for one thing only: does any outcome surface a materially new sub-question that wasn't in the original decomposition? Record a binary finding (gap found / not found / inconclusive) as a new Evidence entry on this Work Object. Does not implement the re-planning loop, the gap-detection heuristic, or the 2-round cap -- diagnostic only. |
| **Authorization** | Director supplied the real test question directly, accepting the tracer bullet design as proposed. |
| **Confidence** | high that this is a fair, real test (the question is genuinely unanswered and something the director actually wants answered, so the run has value regardless of outcome); medium on what the result will show |
| **Actor** | director |
| **Revisit trigger** | Same as Decision 1's revisit trigger -- this tracer bullet's result directly resolves it. Gap found -> proceed to implement Direction 1's loop. No gap found (and the run was not degraded) -> revisit Decision 1 toward Direction 4. Run too degraded to judge (e.g. most sub-questions came back unresolved) -> inconclusive, re-run with a different question rather than concluding either way. |
| **Rationale** | Cheapest possible way to falsify Direction 1's key assumption before investing in the loop, cap, and heuristic Decision 1 deferred as design work. Using a real, currently valuable question (rather than a synthetic one) means the run produces a useful deliverable regardless of what it reveals about the assumption. |

**Result: GAP FOUND.** Deliverable:
[.work-studio/deliverables/2026-08-22-003-visual-command-center.md](2026-08-22-003-visual-command-center.md).
Sub-question 3 (serving/rendering mechanism) organically surfaced a
materially new sub-question -- live-MCP-serve vs. static-generated-artifact
-- only visible after seeing that `mcp_server/`'s exposure scope is itself
still an open, undecided question elsewhere (WO `2026-08-21-010`). Direction
1's key assumption holds, at least once, unmanufactured.

**Gap-detection heuristic, specified from this concrete example** (closes
the design gap Decision 1 deferred): a second-round sub-question is
*genuine*, not cosmetic rephrasing, when an initial-round outcome reveals
that answering it depends on a **separate, unresolved decision or fork**
the original decomposition didn't anticipate -- not merely a related
detail or a narrower version of an existing sub-question. Here: the
serving-mechanism question turned out to hinge on another Work Object's
still-open authority question, which no rewording of the original
decomposition would have surfaced.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | alawas-research-investigate-live-question SKILL.md, Required capability mappings | investigate-live-question already declares web_fetch (native) and web_search (manual-fallback), but its Stage 3 ('Retrieve primary-source evidence') is single-shot per source -- it retrieves named/discovered sources once, it does not iterate: search, read, follow up, search again. Any 'deep research' refinement changes this iteration behavior, not the presence of search capability itself. |
| [system] | .work-studio/deliverables/2026-08-22-003-visual-command-center.md | Tracer bullet Decision 2 result: GAP FOUND. Running produce-report unmodified on 'how to build a visual command center' decomposed into 4 sub-questions; answering sub-question 3 (serving/rendering mechanism) organically surfaced a materially new sub-question -- live-MCP-serve vs. static-generated-artifact -- that was not in the original decomposition and only became visible after seeing that mcp_server/ exists but is minimal/deferred (WO 2026-08-21-010, verify state, exposure scope explicitly undecided). This is a real, unmanufactured instance of Decision 1's key assumption holding: fixed one-shot decomposition missed a sub-question that later outcomes revealed. |
| [system] | focused tests, kernel verifier, adapter drift check, and Codex project install | Decision 3 conformance repair verified: the three focused regressions passed; all kernel integrity checks passed; generated adapters matched with no drift; Codex installation verified the packaged research-produce-report skill contains the exact high-consequence mutation gate and its dedicated grilling profile. |
## Open questions

**Resolved by Decision 1:** infra dependency. Not a preference call after
all -- `subagent_spawn` maps to a single-subagent primitive on every
generated adapter; the `Workflow` tool Direction 2 needed has no
cross-platform equivalent. Direction 2 rejected outright on that basis.

Still open, not discoverable from the workspace -- need director input,
now scoped to Direction 1 specifically:

- **Scope of "deep research."** Direction 1 assumes external web research
  via `investigate-live-question`. Does "deep research" also cover
  recursive *internal* research (re-querying past Work Objects, evidence
  ledgers, deliverables)? Not designed for in Decision 1 -- would be a
  separate extension if wanted.
- **Budget tolerance.** Direction 1's 2-round hard cap still costs
  materially more tokens and wall-clock time per report than today's single
  pass. No stated budget constraint exists yet; relevant when
  design-tracer-bullet sizes the smallest test.

## Next move

Route to `alawas-engineering-implement-bounded-change` for Decision 3's narrow
conformance repair. Preserve Decision 1's iterative re-planning implementation
as separate unfinished scope after this repair.

### Direction 1: Iterative re-planning loop (adaptive decomposition)

- **Core idea**: Replace the fixed "decompose once, then invoke
  `investigate-live-question` once per sub-question" pattern with a loop:
  run the initial sub-question set, read back their outcomes, then generate
  *new* sub-questions the initial answers reveal as missing (mirroring how
  Claude's Deep Research re-plans after an initial research pass), repeating
  until a stop condition (diminishing new findings, or a turn/budget cap) is
  hit — only then synthesizing the final deliverable.
- **Distinctness claim**: The only direction that changes *when* questions
  are asked, not just how many run in parallel or how deep each one
  searches. It targets the decomposition step in `produce-report` itself.
- **Key assumption**: The current one-shot decomposition genuinely misses
  sub-questions that only become obvious after seeing initial answers — not
  yet tested.
- **Smallest test**: Run `produce-report` on one real broad research request
  in its current form; manually check afterward whether a sub-question was
  missing that only became obvious once the first-round outcomes were in.
  If none is found, this direction has no target problem yet.

### Direction 2: Workflow-tool orchestration (formal pipeline + verify)

- **Core idea**: Formalize `subagent_spawn` into an actual `Workflow` script
  — parallel fan-out of independent sub-question investigations, each
  optionally followed by an adversarial-verify stage (the same pattern this
  session's tooling already documents for code review), then a synthesis
  stage — instead of the current "sequential invocation is always valid,
  parallel via subagent_spawn when independent" wording.
- **Distinctness claim**: The only direction that changes the orchestration
  *mechanism* itself (ad hoc subagent calls -> a declared, resumable
  pipeline), rather than what each sub-question investigation does.
- **Key assumption**: The `Workflow` tool's fan-out/verify patterns add
  measurable quality or speed over today's sequential/optional-parallel
  invocation, without breaking `produce-report`'s existing boundary (it
  still only composes `investigate-live-question`, never bypasses its
  evidence discipline).
- **Smallest test**: Build one `Workflow` script that pipelines 3
  sub-questions with a verify stage; compare its output and wall-clock time
  against today's sequential invocation on the identical request.

### Direction 3: Deepen `investigate-live-question` itself (multi-hop search)

- **Core idea**: Leave `produce-report`'s orchestration untouched; instead
  give `investigate-live-question`'s own Stage 3 ("Retrieve primary-source
  evidence") a bounded multi-hop loop — search, read, follow up with a
  refined search, read again — up to a fixed depth, instead of today's
  single-shot retrieval per source.
- **Distinctness claim**: The only direction that locates the fix inside the
  sub-question investigator, not the report composer. `produce-report`'s
  decomposition and orchestration stay exactly as documented today.
- **Key assumption**: Most of the gap between today's output and
  "Deep-Research-quality" comes from shallow single-source retrieval per
  sub-question, not from how sub-questions are decomposed or orchestrated.
- **Smallest test**: Take one sub-question that previously came back
  `unresolved`; check whether one additional, refined follow-up search
  inside `investigate-live-question` would have resolved it.

### Direction 4: Transparent, interruptible research (no new search depth)

- **Core idea**: Add no new search or orchestration capability at all.
  Instead, make `produce-report` report each sub-question's outcome to the
  director as it completes (not just once at the end), so the director can
  redirect, add a sub-question, or stop early mid-research — mirroring
  Deep Research's visible "here's my plan, here's progress" UX rather than
  its raw search depth.
- **Distinctness claim**: The only direction that adds zero new search or
  compute capability — it is a transparency/control change, not a power
  change, and is the cheapest of the four by a wide margin.
- **Key assumption**: What actually feels missing versus Deep Research is
  visibility and mid-course control, not necessarily deeper search — not
  yet tested against the other three directions' assumption that raw
  capability is the gap.
- **Smallest test**: Run one report-type request today; afterward, ask
  whether seeing intermediate sub-question outcomes as they landed would
  have changed how the director wanted to steer the rest of the research.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T10:03:47Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director invoked alawas-thinking-develop-idea directly with a rough idea: refine alawas-research-produce-report into something closer to Claude's Deep Research -- a dynamic workflow that searches the web, spawns subagents, and adopts other Deep Research-style capability. No Work Object existed for this idea; created one to satisfy develop-idea's precondition (active Work Object in explore state, type inquiry) before generating directions.
### 2026-08-22T10:03:47Z — Activated for direction generation

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Type inquiry, explore state satisfies develop-idea's precondition. Proceeding directly to direction generation in the same turn per director's direct invocation.
### 2026-08-22T11:00:06Z — Decision recorded: adopt Direction 1 (bounded iterative re-planning), reject Direction 2 outright

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director confirmed Direction 1 over pressure-test-decision's recommendation. Direction 2 (Workflow-tool orchestration) eliminated on discoverable portability grounds -- subagent_spawn maps to a single-subagent primitive on every generated adapter, no cross-platform Workflow equivalent exists. Direction 1 adopted: at most one bounded re-planning round, gated on a genuine gap in the initial outcomes, hard-capped at 2 rounds total. Untested key assumption and the gap-detection heuristic are the open design question, routed to design-tracer-bullet.
### 2026-08-22T11:04:47Z — Tracer bullet accepted with real test question

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director supplied the test question directly: 'How do I build the visual central command center for my Work Studio based on its current system?' Tracer bullet design accepted as proposed -- run unmodified produce-report on this question, check outcomes for a decomposition gap.
### 2026-08-22T11:07:28Z — Tracer bullet result: gap found, assumption holds

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** produce-report ran unmodified on the real test question; sub-question 3 organically surfaced a materially new sub-question (live-MCP-serve vs static-generated-artifact) only visible after seeing the initial outcomes. Direction 1's key assumption holds, unmanufactured. Gap-detection heuristic specified from this concrete example, closing the design gap Decision 1 deferred. Deliverable: .work-studio/deliverables/2026-08-22-003-visual-command-center.md
### 2026-08-22T11:09:54Z — Accepted bounded conformance repair

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Director explicitly requested fixing the reproduced research-produce-report gaps; iterative re-planning remains outside this repair.
### 2026-08-22T11:14:27Z — Decision 3 conformance repair verified and installed

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Canonical skill registration, grilling coverage, authority language, generated adapters, and project Codex installation all passed their focused checks. The Work Object remains active because Decision 1's iterative re-planning loop is separate unfinished scope.
