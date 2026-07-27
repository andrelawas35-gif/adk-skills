---
name: verify-design-implementation
default_tier: medium
description: "Use when design implementation needs verification; checks that the agent's code changes match what the user confirmed — browser rendering matches the confirmed proposal; does not fix issues, only reports them."
---

# Verify Design Implementation

## Governing principle

Verification must be honest about what it checks and what it defers.
The primary check is: does what the browser renders match what the user
confirmed? For Path A (code-first execution), the reference is the confirmed
proposal from `apply-design-direction`. For Path B (Claude Design execution),
the reference is the implementation brief. Both paths verify against the
browser — Claude Design visual comparison is optional and must never
substitute for browser evidence.

Structural and visual verification against the confirmed proposal or brief
are the focus. Behavioral, full-stack, and accessibility dimensions are
explicitly deferred with status reporting, not silently omitted.

## Boundaries and non-goals

This skill does:

- Verify that the agent's implementation matches the confirmed proposal
  or implementation brief from `apply-design-direction`.
- Check structural correctness: does the implementation contain the
  specified changes?
- Check visual correctness: does the browser rendering reflect the
  confirmed changes or brief at specified viewports?
- Optionally, compare the browser rendering against a Claude Design visual
  reference (when available) for additional visual fidelity checking.
- Produce a `[system:verification-report]` Evidence Ledger entry with
  per-change pass/fail status.
- Degrade gracefully when browser automation is unavailable, with
  explicit capability gap reporting.

This skill does not:

- Fix implementation issues — it reports them.
- Check behavioral correctness (interactions, state transitions, API calls).
- Check full-stack correctness (backend rendering, data loading, auth flows).
- Check accessibility (WCAG compliance, screen reader behavior, keyboard nav).
- Modify any code or design artifacts.

## Inputs and preconditions

**Required input:** a readable Work Object in the `verify` state with:
- A `[system:design-direction]` evidence entry from `apply-design-direction`
  (confirmed proposal for Path A, or implementation brief for Path B).
- Access to the running application in a browser (or manual-fallback).
- For Path B, optionally a Claude Design visual reference for additional
  visual comparison (when available and user has authenticated).

**Preconditions:** the confirmed changes have been implemented. The target
project dev server is running and accessible.

## Required capabilities

- `file_read` — read confirmed proposal, target project code.
- `structured_output` — produce the verification report.
- `browser_automation` — inspect the running application (manual-fallback
  acceptable).

## Consequence and authority rules

- This skill performs only reads and observations — **low consequence**.
- No code or design artifacts are modified.
- The verification report is written to the Evidence Ledger through the
  conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

The verification lens asks:

1. Are the checked changes sufficient for the confirmed proposal's risk level?
2. Are unchecked aspects honestly reported?
3. Could a structural match hide a visual mismatch (or vice versa)?

## Skill Grilling Profile

Apply the `verify-design-implementation` profile and continuous Grilling
Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Load confirmed proposal or brief

Read the `[system:design-direction]` evidence entry from
`apply-design-direction`. Extract the confirmed interpretation (Path A)
or the implementation brief (Path B): what was supposed to change, what
was supposed to be preserved, and what was out of scope.

If a Claude Design visual reference is available, load it as an optional
comparison aid. The browser rendering is always the canonical reference.

### 2. Check implementation (structural)

Inspect the target project code. Verify: are the confirmed changes present
in the code? Are preserved elements still intact? Are there unintended
changes outside the confirmed scope?

### 3. Check implementation (visual)

Inspect the running application (via browser automation or manual
observation). Compare the browser rendering against the confirmed proposal
(Path A) or implementation brief (Path B) at specified viewports (mobile,
tablet, desktop). Verify that the visual result matches the user's confirmed
intent or the brief's visual specification.

**Optional — Claude Design visual comparison (Path B only):** If a Claude
Design visual reference is available and the user has authenticated, compare
the browser rendering against the visual reference as an additional fidelity
check. This comparison is OPTIONAL and must never substitute for direct
browser evidence. Record whether the visual reference was used and any
divergences found.

When browser automation is unavailable, pause with one concrete manual
instruction: "Open [URL] in a browser, verify [specific change], and
confirm." Record the user's confirmation as the visual evidence.

### 4. Produce verification report

Assemble the `[system:verification-report]` Evidence Ledger entry with
per-change status:

| Change | Code status | Visual status |
|---|---|---|
| Each confirmed change | present / missing / divergent | matches / divergent / unchecked |

Plus overall dimensions:

| Dimension | Status |
|---|---|
| Structural (confirmed changes in code) | checked |
| Visual (browser matches confirmed proposal/brief) | checked / manual |
| Visual (Claude Design reference comparison) | optional — not used / matches / diverges |
| Behavioral (interactions, state) | deferred |
| Full-stack (backend, data, auth) | deferred |
| Accessibility (WCAG, keyboard, screen reader) | deferred |

### 5. Report honestly

For each checked change: state whether it matches with evidence.
For deferred dimensions: state why deferred and what would be needed.
If corrections are needed, state what specifically diverges.

## Routing and termination

**Route when:**
- Verification report is complete — return to `conduct-work-object`.
- Corrections needed — route to `apply-design-direction` with the specific
  divergences.

**Terminate when:**
- Verification report is recorded in the Evidence Ledger.
- All confirmed changes are checked; deferred dimensions are documented.

## Output contract

The `[system:verification-report]` Evidence Ledger entry contains:

- `confirmed_proposal`: reference to the `[system:design-direction]` entry
  (confirmed proposal for Path A, implementation brief for Path B)
- `reference_type`: `proposal` or `brief` — which was used as the primary
  comparison reference
- `claude_design_visual_ref_used`: `true` | `false` — whether optional
  Claude Design visual comparison was performed
- `changes`: per-change status (present / missing / divergent) with evidence
- `dimensions`: per-dimension status (checked | deferred | optional) with:
  - `matches`: what aligned correctly (for checked dimensions)
  - `divergences`: what diverged, with evidence (for checked dimensions)
  - `reason`: why deferred (for deferred dimensions)
- `overall`: pass (all confirmed changes verified) | fail (divergences found)
  | partial (some dimensions deferred)

## Final self-check

- [ ] Verification report references the confirmed proposal or implementation brief
- [ ] `reference_type` is documented (`proposal` or `brief`)
- [ ] Each confirmed change has a code status and visual status
- [ ] Deferred dimensions are honestly reported with reasons
- [ ] Checks reference the confirmed reference, not assumptions
- [ ] Claude Design visual comparison (if used) is recorded as optional, never primary
- [ ] No code or design artifacts were modified
- [ ] Capability degradation (no browser automation) is explicit
