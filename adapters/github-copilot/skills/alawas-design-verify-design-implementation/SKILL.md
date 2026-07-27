---
name: alawas-design-verify-design-implementation
description: "Use when design implementation needs verification; checks that the agent's code changes match what the user confirmed — browser rendering matches the confirmed proposal; does not fix issues, only reports them."
default_tier: medium
platform: github-copilot
---
# Verify Design Implementation

## Governing principle

Verification must be honest about what it checks and what it defers.
The primary check is: does what the browser renders match what the user
confirmed? Structural and visual verification against the confirmed
proposal are the focus. Behavioral, full-stack, and accessibility
dimensions are explicitly deferred with status reporting, not silently
omitted.

## Boundaries and non-goals

This skill does:

- Verify that the agent's implementation matches the confirmed proposal
  from `alawas-design-apply-design-direction`.
- Check structural correctness: does the implementation contain the
  specified changes?
- Check visual correctness: does the browser rendering reflect the
  confirmed changes at specified viewports?
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
- A confirmed proposal from `alawas-design-apply-design-direction` (the `[system:design-direction]`
  evidence entry).
- Access to the running application in a browser (or manual-fallback).

**Preconditions:** the confirmed changes have been implemented. The target
project dev server is running and accessible.

## Required capabilities

- `file_read` — read confirmed proposal, target project code.
- `structured_output` — produce the verification report.
- `browser_automation` — inspect the running application (manual-fallback
  acceptable).

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill performs only reads and observations — **low consequence**.
- No code or design artifacts are modified.
- The verification report is written to the Evidence Ledger through the
  conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card
and wait for explicit entry; do not silently start a continuous session.

The verification lens asks:

1. Are the checked changes sufficient for the confirmed proposal's risk level?
2. Are unchecked aspects honestly reported?
3. Could a structural match hide a visual mismatch (or vice versa)?

## Skill Grilling Profile

Apply the `alawas-design-verify-design-implementation` profile and continuous Grilling
Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Load confirmed proposal

Read the `[system:design-direction]` evidence entry from
`alawas-design-apply-design-direction`. Extract the confirmed interpretation: what was
supposed to change, what was supposed to be preserved, and what was out
of scope.

### 2. Check implementation (structural)

Inspect the target project code. Verify: are the confirmed changes present
in the code? Are preserved elements still intact? Are there unintended
changes outside the confirmed scope?

### 3. Check implementation (visual)

Inspect the running application (via browser automation or manual
observation). Compare the browser rendering against the confirmed proposal
at specified viewports (mobile, tablet, desktop). Verify that the visual
result matches the user's confirmed intent.

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
| Visual (browser matches confirmed proposal) | checked / manual |
| Behavioral (interactions, state) | deferred |
| Full-stack (backend, data, auth) | deferred |
| Accessibility (WCAG, keyboard, screen reader) | deferred |

### 5. Report honestly

For each checked change: state whether it matches with evidence.
For deferred dimensions: state why deferred and what would be needed.
If corrections are needed, state what specifically diverges.

## Routing and termination

**Route when:**
- Verification report is complete — return to `alawas-governance-conduct-work-object`.
- Corrections needed — route to `alawas-design-apply-design-direction` with the specific
  divergences.

**Terminate when:**
- Verification report is recorded in the Evidence Ledger.
- All confirmed changes are checked; deferred dimensions are documented.

## Output contract

The `[system:verification-report]` Evidence Ledger entry contains:

- `confirmed_proposal`: reference to the `[system:design-direction]` entry
- `changes`: per-change status (present / missing / divergent) with evidence
- `dimensions`: per-dimension status (checked | deferred) with:
  - `matches`: what aligned correctly (for checked dimensions)
  - `divergences`: what diverged, with evidence (for checked dimensions)
  - `reason`: why deferred (for deferred dimensions)
- `overall`: pass (all confirmed changes verified) | fail (divergences found)
  | partial (some dimensions deferred)

## Final self-check

- [ ] Verification report references the confirmed proposal
- [ ] Each confirmed change has a code status and visual status
- [ ] Deferred dimensions are honestly reported with reasons
- [ ] Checks reference the confirmed proposal, not assumptions
- [ ] No code or design artifacts were modified
- [ ] Capability degradation (no browser automation) is explicit
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `structured_output` | `—` | native |
| `browser_automation` | `—` | manual-fallback |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: GitHub Copilot browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.
