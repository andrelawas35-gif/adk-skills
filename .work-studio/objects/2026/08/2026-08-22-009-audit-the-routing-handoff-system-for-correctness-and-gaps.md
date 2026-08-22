---
schema_version: 1
id: 2026-08-22-009
title: Audit the routing/handoff system for correctness and gaps
type: inquiry
status: active
state: build
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T11:26:51Z
updated_at: 2026-08-22T11:40:12Z
next_action: All four gaps (G1-G4) fixed and verified. Ready to close, or director may want to commit these changes first.















---
## Intent

Audit the routing/handoff system for correctness and gaps. Report-type
research request; grounded in the real code, not a synthesis of prior
decisions.

**Deliverable:** [.work-studio/deliverables/2026-08-22-009-routing-handoff-audit.md](../../../deliverables/2026-08-22-009-routing-handoff-audit.md)

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Both routing layers (skill-level, runtime) mapped and their logic
      checked against real code
- [x] Sync between runtime table and conductor table verified (in sync,
      guarded by a passing test)
- [x] Gaps surfaced and fixed: G1 (inert to_skill placeholder, Decision 1),
      G2 (advisory routing-consistency check, Decision 1), G3 (stale
      drift-guard comment, Decision 2), G4 (hardcoded alawas- prefix in 6
      core files, reframed and fixed, Decision 2)


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

### Decision 1 — Fix G1 (inert to_skill placeholder) and G2 (no routing-consistency check)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Fix both substantive gaps from the routing audit as smallest reversible changes: G1 -- derive `phase6_dispatch`'s `to_skill` from `derive_proposal(state)` instead of the hardcoded `"specialist"` placeholder. G2 -- add an advisory-only `routing-consistency` validator check (excluded from `DEFAULT_CHECKS`) cross-referencing `next_action` against the conductor's state-keyed route. G3 (comment fix) and G4 (naming) explicitly deferred, not in scope of this decision. |
| **Authorization** | Director: "Fix G1 and G2" |
| **Confidence** | high -- both fixes verified directly: G1 against all 8 states + empty/unknown via `derive_proposal`, with no test pinning the old placeholder value; G2 run against the real workspace (fires correctly as warnings, never blocks, exit 0), and its own high false-positive rate on real data confirms the audit's prediction that it must stay advisory |
| **Actor** | director |
| **Revisit trigger** | G2's advisory warnings fire on most active Work Objects today (next_action is usually more specific than the bare canonical skill name) -- if this proves too noisy to be useful in practice, narrow the match logic or retire the check, rather than promoting it to a hard gate to force compliance. |
| **Rationale** | The routing audit (this Work Object's own report) found the routing logic sound overall but identified two substantive, low-risk gaps with clear, small fixes already specified in the deliverable. Director authorized fixing both directly rather than routing through a separate pressure-test-decision pass, given the fixes were already precisely scoped by the audit itself. |

### Decision 2 — Fix G3 (stale comment) and G4 (naming), reframed on inspection

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | G3: reworded the `_STATE_ROUTING_TABLE` comment in `runtime/handoff.py` to name the actual drift-detection test instead of only saying no sync exists. G4: the original audit framing ("mixed alawas-prefixed and bare naming, low consequence") was wrong on inspection -- `adapter_skill_name()` confirms bare names are canonical in `skills/core/`, with the `alawas-` prefix applied only at generation time. The real issue was 6 core files hardcoding the prefix in their own source (business-assess-financial-decision, business-improve-operating-process, business-manage-commercial-pipeline, business-plan-workforce-accountability, research-produce-report, thinking-resume-work), bypassing the generator. Normalized all 17 occurrences to bare names. |
| **Authorization** | Director: "route: alawas-governance-conduct-work-object -- G3/G4" |
| **Confidence** | high -- verified `generate-adapters.py --check` reports no drift after the change (generated adapter output is byte-identical), and the full 26-test generator contract suite passes |
| **Actor** | director |
| **Revisit trigger** | If any future core skill file is authored with a hardcoded `alawas-` prefix again, that repeats this same drift -- worth a lint check in the generator itself if it recurs, though none exists today. |
| **Rationale** | G3 was a one-line, zero-risk documentation accuracy fix. G4's original framing undersold the real risk (silent drift if the prefixing convention ever changes) and its true scope only became clear by reading `adapter_skill_name()` directly rather than trusting the audit's own "low consequence" label -- worth recording as a correction to the prior report, not just an implementation note. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/handoff.py:46-60, skills/core/governance-conduct-work-object/SKILL.md '### 6. Route to specialist' | Two routing layers exist. Skill-level: the conductor's 8-row state->skill table is the canonical routing authority, executed by a human/agent. Runtime: _STATE_ROUTING_TABLE is a manually-synced copy. Compared row-by-row: identical today (notice->turn-signal-into-work, explore->develop-idea, design->design-tracer-bullet, build->implement-bounded-change, verify->verify-release-evidence, release->deploy-with-recovery, observe/close->review-outcome-and-adapt). |
| [system] | runtime/tests/test_handoff_graph.py:515-548, executed | test_state_routing_table_stays_in_sync_with_conductor parses the conductor SKILL.md table and asserts the runtime copy matches. Ran it: PASS. So the drift risk the handoff.py comment warns about ('no automatic sync exists') is auto-DETECTED (failing test), even though it is not auto-SYNCED. The comment undersells the existing guard. |
| [system] | runtime/graph.py phase6_dispatch (~658), runtime/handoff.py derive_proposal | phase6_dispatch hardcodes to_skill='specialist' on the HandoffEnvelope -- an inert placeholder (previously confirmed by WO 2026-08-21-006). The real routing signal is derive_proposal(state), computed on each branch's HandoffReceipt, not on the dispatch envelope. The envelope's to_skill field therefore carries no routing meaning. |
| [system] | runtime/handoff.py:63-75, 114-130; test_handoff_graph.py derive_proposal/merge tests PASS | Routing logic is correct where it exists: derive_proposal defaults unknown/empty state to 'await-director' (safe deferral, not a wrong route); merge_proposals dedups and sorts deterministically; explore->develop-idea (never directly ->investigate-live-question) is consistent between runtime and the conductor's documented downstream-only note. |
| [gap] | tools/ws/validate.py (no next_action<->state routing check), grep across tools/ws and runtime | No validation cross-checks a Work Object's free-text next_action against its state's routing target. The conductor SKILL.md says routing is 'Based on current state and next_action' but the table is state-keyed and next_action is unconstrained free text -- nothing detects a next_action that contradicts the state's canonical route. (An incident-routing successor-linkage check exists, but nothing general.) |
| [gap] | skills/core/*/SKILL.md routing refs; tools/generate-adapters.py namespace_skill_references:626-637 | Core SKILL.md files mix alawas-prefixed and bare skill references (e.g. both 'alawas-governance-conduct-work-object' and 'conduct-work-object'). The generator normalizes BACKTICKED references of either form via aliases, so adapters are consistent -- but non-backticked prose references are not normalized and would ship as bare names. Low consequence (readability, not routing logic). |
| [system] | runtime/graph.py phase6_dispatch, tools/ws/validate.py check_routing_consistency -- implemented and verified | G1 fixed: phase6_dispatch now derives to_skill via derive_proposal(frontmatter.get('state',''), role='dispatch') instead of the hardcoded 'specialist' placeholder. Verified against all 8 states + empty/unknown -- correct real skill name or 'await-director' in every case. No test asserted the old literal value; routing-sync and derive_proposal tests still pass; the 11 pre-existing test errors in that file are a baseline fixture issue (confirmed identical on git-stashed original graph.py, unrelated to this change). G2 fixed: new advisory 'routing-consistency' check added to tools/ws/validate.py (excluded from DEFAULT_CHECKS, run via 'ws validate routing-consistency'), cross-referencing next_action against the conductor's state-keyed route, skipping closed objects. Ran against the real workspace: fires as a warning (not a failure, exit 0) on most active objects, because next_action is legitimately almost always MORE specific than the bare canonical skill name -- confirms the audit's own prediction that this must stay advisory, never a hard gate. Fixed one caused regression: tests/test_ws_cli.py's test_all_checks_registered hardcodes the full CHECK_REGISTRY key set and needed the new name added -- now passes. Full tools test suite: 253 tests, 1 pre-existing unrelated failure (a path-separator string match in evidence-relations, confirmed present before these changes). |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [gap] | ws transition audit (build) | A decision record with result: pass exists but none has a populated rationale. Claim sidecar expected to document contradiction and freshness exposure in the rationale field. |
| [system] | runtime/handoff.py comment; skills/core/*/SKILL.md; tools/generate-adapters.py adapter_skill_name() | G3 fixed: the drift-guard comment now names the actual detection test (test_state_routing_table_stays_in_sync_with_conductor) instead of only saying 'no automatic sync exists'. G4 reframed and fixed: confirmed via adapter_skill_name() that the canonical convention is bare names in core/, alawas- prefix added only at generation time. The real inconsistency (not 'mixed naming is arbitrary' as originally audited) was 6 core files hardcoding the adapter-facing prefixed name in their own source, bypassing the generator: business-assess-financial-decision, business-improve-operating-process, business-manage-commercial-pipeline, business-plan-workforce-accountability (1 occurrence each, self-referencing their own Grilling Profile line), research-produce-report (11 occurrences), thinking-resume-work (2 occurrences). All 17 occurrences were backtick-wrapped, matching the generator's expected pattern exactly. Normalized all 6 files to bare names. Verified: generate-adapters.py --check reports no drift -- the generator's own aliasing correctly re-adds the alawas- prefix at generation time, so generated adapter output is byte-identical to before. Full generator contract suite (26 tests) passes. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:27:13Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director invoked alawas-research-produce-report to audit the routing/handoff system for correctness and gaps. Report-type: decomposed into sub-questions grounded in real code (runtime/handoff.py, graph.py Phase 6, conductor SKILL.md routing table, tools/ws/validate.py).
### 2026-08-22T11:27:13Z — Investigated and producing report

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Grounded audit of both routing layers complete; authoring deliverable.
### 2026-08-22T11:28:38Z — Deliverable produced: routing/handoff audit

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Report authored at .work-studio/deliverables/2026-08-22-009-routing-handoff-audit.md. Both routing layers audited against real code; routing logic sound and tables in sync (guarded by a passing test); four gaps surfaced (G1 inert to_skill placeholder, G2 no next_action/state consistency check, G3 stale drift-guard comment, G4 mixed skill-reference naming). No architecture authored -- gaps surfaced for separate decisions.
### 2026-08-22T11:34:28Z — G1 and G2 implemented and verified

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director instructed: fix G1 and G2. Both implemented as smallest reversible changes: G1 one-line derivation fix in phase6_dispatch; G2 a new advisory-only validator check, matching the audit's own recommendation not to make it a hard gate. Verified against real code and the real workspace; fixed a regression the change itself caused (test_all_checks_registered); confirmed the one remaining test failure predates these changes.
### 2026-08-22T11:34:58Z — G1 and G2 implemented and verified

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 1 recorded. Both fixes implemented as smallest reversible changes and verified against real code and the real workspace. Fixed a regression the change itself caused (test_all_checks_registered); confirmed the one remaining test failure predates these changes.
### 2026-08-22T11:35:23Z — Decision record corrected

- **State:** build
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Removed duplicate placeholder rows left by an earlier edit and populated the Rationale field the audit gate flagged as missing.
### 2026-08-22T11:40:12Z — G3 and G4 implemented and verified

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 2 recorded. G3 fixed (comment accuracy). G4 reframed on inspection -- the original audit label undersold a real drift risk, corrected in Decision 2's rationale. All four gaps from the routing audit are now fixed.
