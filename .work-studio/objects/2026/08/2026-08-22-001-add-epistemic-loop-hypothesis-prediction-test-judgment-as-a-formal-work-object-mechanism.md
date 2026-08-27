---
schema_version: 1
id: 2026-08-22-001
title: Add epistemic loop (Hypothesis/Prediction/Test/Judgment) as a formal Work Object mechanism
type: inquiry
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [governance, architecture]
created_at: 2026-08-22T09:45:45Z
updated_at: 2026-08-22T09:54:08Z
next_action: None -- closed. Cross-reference doc at references/EPISTEMIC-LOOP-MAPPING.md; revisit only if a concrete need to query/group Work Objects by loop-stage arises (Decision 1 revisit trigger).








---
## Intent

Test whether the studio's epistemic model needs a new formal loop —
`Evidence -> Hypothesis -> Prediction -> Test -> New Evidence -> Judgment ->
Decision -> Action -> Outcome -> Revision` — as a tracked mechanism sitting
alongside the existing Evidence Ledger / Decisions / History split, or
whether that split plus the existing Decision revisit-trigger and outcome-
review cycle already covers the same ground informally, making a new
mechanism redundant ceremony.

Originated from a request to `alawas-research-produce-report` to "create a
plan" for a recapped "epistemic architecture." That skill found the request
mixed already-accepted material, one superseded taxonomy stated as current,
and this genuinely new, undecided loop — and stopped rather than author
architecture no one had accepted. Director chose to route the loop as a
decision to pressure-test rather than drop it.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Pressure-test-decision has adversarially tested whether the loop
      catches a real recurring failure the current Decision + revisit-
      trigger + outcome-review cycle misses -- it does not (four
      independent citations, Decision 1)
- [x] A recorded decision: adopt the loop as a formal mechanism, reject it
      as redundant, or adopt a narrower/different version -- Decision 1,
      Branch C (non-binding cross-reference doc, no schema change)


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

### Decision 1 — Reject formal loop mechanism; author a non-binding cross-reference doc instead

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Whether to add `Evidence -> Hypothesis -> Prediction -> Test -> New Evidence -> Judgment -> Decision -> Action -> Outcome -> Revision` as a new formal, schema-tracked Work Object mechanism (Branch B), reject it outright with no artifact (Branch A), or author one short, non-binding reference document mapping each loop-stage name to its existing owning skill/field, with zero Work Object frontmatter, template, or validator changes (Branch C — chosen) |
| **Authorization** | Director: "Accept C, no missed-catch case" |
| **Confidence** | high that the loop is not a missing mechanism — four independent citations confirm each stage already exists under a different name (`pressure-test-decision`'s Branch-chosen/alternatives = Hypothesis, its step 6 "Test the confirmed choice" = Prediction, `design-tracer-bullet`'s "observable exit evidence" for a "falsifiable assumption" = Test, the Decision record's Rationale/Confidence = Judgment, `review-outcome-and-adapt`'s "Compare the hypothesis with what was actually shipped and what was actually observed" = Outcome, the Decision record's Revisit trigger = Revision); medium on whether even the lightweight doc is worth authoring versus recording this finding and closing with no artifact at all |
| **Actor** | director |
| **Revisit trigger** | If a concrete need arises to query, group, filter, or automate over Work Objects by loop-stage (a dashboard, a report, a validator rule) — not merely a preference for the loop's naming to feel more explicit — revisit toward Branch B (formal schema-tracked mechanism). Director explicitly confirmed no missed-catch case exists today. |
| **Rationale** | Branch A leaves the actual finding (the mapping across skills is real but undiscoverable without cross-referencing four separate files) unaddressed. Branch B would formalize schema-tracked duplication of fields that already exist under other names — the studio's own anti-patterns (`conduct-work-object`'s "stage theater," this skill's "premature ADRs" and "vague recording") already warn against ceremony that doesn't add new capability. Branch C is the smallest reversible artifact that matches the real gap (discoverability of an existing distributed mechanism), not the imagined gap (a missing mechanism). |

**Edge case noted:** the cross-reference doc has no enforcement — if a referenced skill's step or field is later renamed or removed, nothing flags the doc as stale, and a stale mapping asserting a false equivalence is worse than no mapping at all.

**Assumption that could invalidate this:** that plain-English documentation is sufficient. If it turns out someone wants to query or filter Work Objects *by* loop-stage (not just read about the mapping), this doc provides no machine-readable anchor for that — Branch B would need reconsidering at that point, per the revisit trigger above.

**Future friction:** any later reporting/dashboard tooling that wants to group Work Objects by epistemic-loop stage gets nothing structural from this doc; it would need its own schema work regardless of whether this decision stands.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | references/EVIDENCE-MODEL.md:16-20 | The Evidence-ledger-vs-History split ('Evidence records what is known and where it came from; History records what happened') and the laundering guard (never present inference as system fact) are already accepted and unchanged. Any new loop must not duplicate or contradict this. |
| [system] | fixtures/conflict-epistemic-tag-contract.md | The five-tag taxonomy in the original framing ([lived], [source], [system], [inference], [decision]) is superseded. WO 2026-07-27-012 reconciled it to the current six tags ([system], [decision], [inference], [gap], [testimony], [memory]): [lived] -> [testimony], [source] -> [system]. Any new mechanism must use the current six-tag set, not the retired one. |
| [gap] | grep across references/AGREEMENT-LOOP.md and docs/adr/* | No trace anywhere in the repo of a formal Evidence -> Hypothesis -> Prediction -> Test -> New Evidence -> Judgment -> Decision -> Action -> Outcome -> Revision loop. This is not a forgotten decision being recovered -- it is a genuinely new proposal with zero prior acceptance. |
## Open questions

**All three resolved by Decision 1** (director confirmed no missed-catch
case exists):
- Real recurring failure mode missed by the current cycle? No — the loop's
  stages already exist distributed across `pressure-test-decision`,
  `design-tracer-bullet`, and `review-outcome-and-adapt`.
- Own tracked section vs. existing sections? Neither — Branch C adds a
  non-binding reference doc only, no schema change either way.
- Does Prediction/Judgment add anything Confidence/Revisit-trigger don't
  already capture? No — they're the same fields under different names.

## Next move

Route to `alawas-engineering-implement-bounded-change`: author one short,
non-binding reference doc (e.g. `references/EPISTEMIC-LOOP-MAPPING.md`)
containing the loop-stage -> owning-skill/field table from Decision 1. No
Work Object frontmatter, template, or validator changes anywhere in the
repo — this is documentation only.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T09:46:04Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Signal originated from a request to alawas-research-produce-report (asking it to author a plan for a described 'epistemic architecture'). produce-report checked the claims against the repo: the History/Evidence split and laundering guard are already accepted (references/EVIDENCE-MODEL.md), the five-tag taxonomy cited was superseded by WO 2026-07-27-012, and the proposed Hypothesis/Prediction/Test/Judgment loop has no prior decision anywhere in the repo. Per its own boundary (never author new architecture as a plan-type deliverable), it stopped and routed to conduct-work-object to open this as a decision to pressure-test, per director confirmation ("Option 2, route it to pressure-test-decision").
### 2026-08-22T09:47:15Z — Classified and staged for pressure-test

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Intent, Success evidence, Open questions, Next move, and three Evidence ledger entries recorded directly per director instruction. Ready to route to pressure-test-decision -- the unresolved decision is whether the proposed epistemic loop catches a real gap or duplicates existing mechanism.
### 2026-08-22T09:50:39Z — Decision recorded: reject formal loop mechanism, author non-binding cross-reference doc

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director confirmed Branch C (Accept C, no missed-catch case) over pressure-test-decision's recommendation. The proposed Evidence->Hypothesis->...->Revision loop is not a missing mechanism -- all ten stages already exist distributed across pressure-test-decision, design-tracer-bullet, and review-outcome-and-adapt under different names. Rejected Branch B (new schema-tracked mechanism) as redundant ceremony; rejected Branch A (no artifact) because the mapping is real but currently undiscoverable without cross-referencing four separate skill files.
### 2026-08-22T09:53:54Z — Closed: Decision 1 recorded and implemented: the proposed epistemic loop is not a missing mechanism -- all ten stages already exist distributed across pressure-test-decision, design-tracer-bullet, and review-outcome-and-adapt. Non-binding cross-reference doc authored at references/EPISTEMIC-LOOP-MAPPING.md, zero schema/template/validator changes, verified via generate-adapters.py --check (no drift) and git status (single new untracked file, no overlap with pre-existing uncommitted work). Both Success evidence checkboxes met.

- **State:** close
- **Status:** closed
- **Actor:** director
- **Rationale:** Decision 1 recorded and implemented: the proposed epistemic loop is not a missing mechanism -- all ten stages already exist distributed across pressure-test-decision, design-tracer-bullet, and review-outcome-and-adapt. Non-binding cross-reference doc authored at references/EPISTEMIC-LOOP-MAPPING.md, zero schema/template/validator changes, verified via generate-adapters.py --check (no drift) and git status (single new untracked file, no overlap with pre-existing uncommitted work). Both Success evidence checkboxes met.
### 2026-08-22T09:54:08Z — Closure hygiene: clear stale next_action

- **State:** close
- **Status:** closed
- **Actor:** claude-code
- **Rationale:** next_action still held the pre-close routing instruction (implement-bounded-change), which was already completed and superseded by closure. Setting it to reflect no further action.
