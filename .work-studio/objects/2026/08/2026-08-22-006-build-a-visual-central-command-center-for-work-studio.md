---
schema_version: 1
id: 2026-08-22-006
title: Build a visual central command center for Work Studio
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [engineering, design]
created_at: 2026-08-22T11:08:08Z
updated_at: 2026-08-22T11:22:09Z
next_action: Director decision: commit these changes, or continue working uncommitted. Work Object is otherwise complete -- both success-evidence criteria met, plus the CLI-wiring deviation.












---
## Intent

Build a visual central command center over Work Studio's current state --
Work Objects, their state/status/consequence, the attention register
(`active.md`), and decisions -- so the director can see the whole system at
a glance instead of reading individual Work Object files or running `ws`
CLI commands one at a time.

Grounded in `.work-studio/deliverables/2026-08-22-003-visual-command-center.md`
(produced by `alawas-research-produce-report`, carried forward as accepted
source material -- see Evidence ledger). That deliverable already answered
most of the research question: the studio's read-only-projection rule
requires this to be read-only, two partial computed-projection precedents
already exist (`ws outcomes`, `ws skill-map`), and the smallest real slice
is a static, regenerated-on-demand HTML view -- not a live service via the
still-authority-undecided MCP server.

Not yet resolved: exact visual layout and information architecture (which
fields matter most at a glance) -- a genuine design question, not answered
by the prior research pass.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] A bounded tracer bullet tests the smallest real slice (static HTML
      generated from `.work-studio/objects/**` + `active.md`) end to end
- [ ] The command center renders real current Work Object state without
      writing to `.work-studio/` anywhere
- [ ] Regeneration is a deliberate, explicit action (a command to run), not
      an automatic or live-watching process, consistent with the studio's
      single-session operating model


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

### Decision 1 — Accept tracer bullet: verify real-file parsing before any rendering

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A read-only script walks `.work-studio/objects/**/*.md` and `active.md`, extracts frontmatter fields (`id`, `title`, `type`, `state`, `status`, `consequence`, `next_action`) and the Primary/Supporting split, and prints a tally: total files, parsed cleanly / with a warning / failed, with path and reason for anything short of clean. No HTML, styling, or rendering. No file written anywhere. |
| **Authorization** | Director: "Accept, verify parsing first" |
| **Confidence** | high that this is the correct first slice -- irregular frontmatter/body formatting has been directly observed across real files this session, making parsing (not rendering) the actual riskiest unknown |
| **Actor** | director |
| **Revisit trigger** | Result of running the script against the real `.work-studio/objects/` tree. Clean (or near-clean) parse -> proceed to a rendering tracer bullet using this same parser. Meaningful failures -> stop and choose: harden the parser, normalize source files, or ship a best-effort view that flags unparsed Work Objects rather than hiding them. |
| **Rationale** | Building a renderer on unverified parsing risks a command center that silently misrepresents real Work Object state -- worse than not having one. Testing extraction alone, against real files, is the cheapest way to know before investing in layout/rendering work. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | .work-studio/deliverables/2026-08-22-003-visual-command-center.md | references/EVIDENCE-MODEL.md states directly: any view over Work Objects -- a report, summary, graph, or dashboard -- is a read-only projection, never a source; writing to it is not a way to change what the record says. A command center must be read-only; any interaction it offers must route back through the ws CLI, never write .work-studio/ directly. |
| [system] | .work-studio/deliverables/2026-08-22-003-visual-command-center.md | Two existing read-only computed projections already exist: 'ws outcomes' (reviewed vs unreviewed Work Objects) and 'ws skill-map build' (skill responsibility/non-goals/capabilities index, though it is not scoped to only this repo's alawas-* skills). tools/ws/dashboard_signals.py exists but is scoped narrowly to epistemic-pressure claims/conflicts, not general Work Object state or attention. |
| [gap] | WO 2026-08-21-010 (MCP server), verify state | The Work Studio MCP server exists but exposes exactly one tool (ws_validate) and its own Work Object has an explicitly open, undecided question: which further ws commands to expose and how authority gating should work for a mutating one. Extending it to serve a live command center would inherit that unresolved authority question rather than resolve it. Recommended smallest slice (deliverable's answer to sub-question 4): a script reading .work-studio/objects/** + active.md that renders one static HTML view, regenerated on demand -- no running service, no new authority-gating question, no new capability declarations anywhere in the skill system. |
| [system] | scratchpad/tracer_parse_check.py, executed against real .work-studio/objects/**/*.md and active.md | Tracer bullet result: 17/17 real Work Object files parsed cleanly for id/title/type/state/status/consequence/sensitivity/next_action -- 0 failures, 0 missing fields. Every single file has irregular blank-line padding before the closing frontmatter '---' (3 to 24 blank lines observed), confirming the suspected risk was real -- but a tolerant parser (find closing '---' anywhere after position 3, regex per remaining line) handled all of it without breaking. Assumption holds: parsing real files is not the blocker. Separately discovered: active.md currently has 0 Primary and 7 Supporting Work Objects -- no Primary is set at all, a real UI-design case the command center must handle. |
| [system] | scratchpad/command_center.py, executed against real .work-studio/objects/**/*.md and active.md, output: scratchpad/command_center.html | Rendering tracer bullet executed successfully. Real output matches the accepted layout exactly: 11 active Work Objects shown, 7 closed hidden by default behind a toggle, 0 parse failures, staleness column computed from real updated_at timestamps, 'no primary set' banner correctly shown (0 primary, 7 supporting). Standalone script, read-only, zero writes to .work-studio/. Static HTML file, regenerated on demand. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [decision] | director: 'add a ws subcommand' | Authorized deviation from the accepted tracer bullet's non-goals (which explicitly excluded ws CLI wrapping). Implemented: moved the generator into tools/ws/command_center.py (matching where dashboard_signals.py and other CLI-backed readers already live) instead of a standalone tools/ script, because the standalone version hardcoded paths to this specific repo checkout -- wiring it as a real ws subcommand required using the same _find_work_studio_root() resolution every other command uses, or it would defeat WO 2026-08-21-003's whole point (ws runs from any directory). Registered 'ws command-center' in tools/ws/__main__.py. tools/command_center.py kept as a thin non-duplicating wrapper (subprocess call to 'python -m tools.ws command-center') rather than deleted, to avoid a destructive operation on a just-created file without separately asked authority. |
## Open questions

- **Visual layout / information architecture.** Which fields matter most
  at a glance -- state/status/consequence per Work Object, the
  Primary/Supporting attention split, decision timelines, staleness
  (`updated_at` age)? Not investigated; a design question for
  design-tracer-bullet, not research.
- **Rendering technology.** A generated static HTML file is the smallest
  slice per the prior research, but the exact mechanism (plain
  Python string templates vs. a small static-site generator vs. an
  Artifact-style self-contained page) is still open.
- **Regeneration trigger.** On-demand only (director runs a command), or
  should there be a lightweight "regenerate and open" convenience step?
  Either is consistent with the read-only rule; this is a UX preference,
  not a constraint.

## Next move

Route to `alawas-design-design-tracer-bullet`: design the smallest
end-to-end slice -- a script reading real `.work-studio/objects/**` +
`active.md` and rendering one static HTML view of current state,
status, consequence, and attention across all Work Objects. The three
Evidence ledger entries above (read-only-projection rule, existing
partial precedents, and the recommended static-artifact approach) should
carry forward as given context, not be re-derived.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:08:21Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director confirmed opening a Work Object for the visual command center, surfaced as a byproduct of WO 2026-08-22-003's tracer bullet: produce-report answered the real question 'how do I build a visual command center' and its deliverable (.work-studio/deliverables/2026-08-22-003-visual-command-center.md) already resolved most of the research question with a concrete recommended smallest slice. This project carries that deliverable forward as accepted source material rather than re-deriving it.
### 2026-08-22T11:09:24Z — Classified and staged for design-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Intent, Success evidence, Open questions, Next move, and three carried-forward Evidence entries recorded. Skipping explore/decide-direction -- the prior research pass (WO 2026-08-22-003's deliverable) already resolved the architectural approach (static, regenerated-on-demand HTML, read-only). Remaining open questions (layout, exact rendering tech, regeneration UX) are design-tracer-bullet's remit, not divergent-direction generation.
### 2026-08-22T11:11:11Z — Tracer bullet accepted, running parsing verification

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted: verify real-file frontmatter parsing before any rendering work.
### 2026-08-22T11:12:04Z — Parsing tracer bullet passed -- proceeding to rendering design

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** 17/17 real files parsed cleanly with a tolerant parser despite universal blank-line padding. Per Decision 1's exit criteria, routing to a second tracer bullet: actually render the static HTML view using this same parser. Also surfaced: active.md has 0 Primary Work Objects currently -- a real case the layout must handle.
### 2026-08-22T11:16:28Z — Rendering tracer bullet passed -- both success-evidence criteria met

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Real static HTML generated from real .work-studio/ data, matching the accepted layout (active/closed split with toggle, staleness, no-primary banner). Zero parse failures, zero writes to .work-studio/. Both bounded tracer bullets (parsing, rendering) now passed.
### 2026-08-22T11:22:09Z — ws command-center subcommand wired and verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Director authorized adding a ws subcommand. Generator moved into tools/ws/command_center.py (portable, uses _find_work_studio_root() like every other command). Verified identical output across three invocation paths: python -m tools.ws command-center, the installed ws console script, and the thin tools/command_center.py wrapper -- including a real cross-directory portability check (correctly errors outside the workspace, correctly resolves from a subdirectory inside it). Changed files: tools/ws/__main__.py (modified), tools/ws/command_center.py (new), tools/command_center.py (rewritten as thin wrapper), .work-studio/command-center.html (generated output). Nothing else touched -- confirmed against substantial pre-existing unrelated dirty work in this repo. Not committed.
