---
name: alawas-design-audit-accessibility
description: "Use when a rendered interface's accessibility conformance needs checking; audits contrast, semantic structure, and accessible names against WCAG baselines or stewarded expectations; never fixes findings or claims compliance."
default_tier: medium
platform: claude-code
---
# Audit Accessibility

## Governing principle

Two skills already touch accessibility and both explicitly stop short of
testing it: `alawas-design-steward-experience-patterns` stewards accessibility as a
*written expectation*, and disclaims any compliance claim from that writing
alone; `alawas-design-verify-design-implementation` marks WCAG, keyboard, and
screen-reader checks `deferred` and states accessibility is not its focus.
Neither gap is an oversight — each skill is honest that conformance
verification is a different job. This skill is that job: it checks a real
rendered interface against WCAG baselines (or a stewarded expectation, when
one exists) and reports findings. It fixes nothing and certifies nothing —
only `alawas-design-apply-design-direction` and its implementation/verification chain
change code, and no written report substitutes for a real compliance audit
by qualified reviewers when regulatory certification is at stake.

## Boundaries and non-goals

This skill does:

- Check a real rendered interface for WCAG contrast ratio conformance
  (text/background pairs, both normal and large-text thresholds).
- Check basic semantic structure: heading hierarchy, discernible accessible
  names on interactive elements, and whether a state or severity signal is
  conveyed by color alone.
- Compare findings against a stewarded `[system:pattern]` accessibility
  expectation from `alawas-design-steward-experience-patterns` when one exists for the
  audited surface; fall back to WCAG's own generic thresholds as the
  baseline when none does, and say explicitly that a generic baseline was
  used instead of a project-specific expectation.
- Prefer real browser-computed styles and DOM structure (via browser
  automation) as the audit mechanism; degrade to static HTML/CSS parsing
  when browser automation is unavailable, and say which mechanism produced
  each finding.
- Produce a `[system:accessibility-audit]` Evidence Ledger entry with
  per-check status and the concrete value behind each finding.
- Explicitly defer, not silently omit, keyboard-navigation, focus-order, and
  screen-reader-behavior checks that require live interaction rather than
  static or single-frame inspection — name them as deferred dimensions with
  a reason, matching `alawas-design-verify-design-implementation`'s own honesty pattern.

This skill does not:

- Fix, patch, or otherwise mutate any code, style, or markup — findings
  route to `alawas-design-apply-design-direction` as candidate direction changes.
- Claim legal, regulatory, or certified accessibility compliance from its
  findings — it reports conformance against declared or generic thresholds,
  never a certification.
- Author or approve an accessibility-expectations pattern — that remains
  `alawas-design-steward-experience-patterns`'s domain; this skill only tests against
  whatever pattern already exists (or the WCAG generic baseline).
- Perform dynamic checks needing live interaction (keyboard traversal, focus
  order, screen-reader announcement behavior) in this version — those are
  named as deferred, not attempted with a weaker proxy.
- Modify the frontier-ownership map or pipeline documentation on its own —
  registering a new frontier is a routing change the conductor and pipeline
  reference own.

## Inputs and preconditions

**Required input:** a readable Work Object with access to a real, rendered
interface to audit — a target project's running application, or a
Work-Studio-owned static projection (e.g. `.work-studio/*.html`). No
particular Work Object state is required: accessibility conformance is
orthogonal to whether a specific creative direction has been confirmed, the
same independence `alawas-design-build-design-foundation` already claims from structural
discovery.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. The surface to audit is identifiable and
reachable (a URL, a dev server, or a real file path). A stewarded
accessibility-expectations pattern is helpful but not required — its absence
is reported, not treated as a blocker.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback,
or unsupported and follows `references/CAPABILITY-DEGRADATION.md` when
needed.

- `file_read` — read the target file, or the stewarded expectations pattern
  when one exists.
- `browser_automation` — inspect computed styles, real DOM structure, and
  accessible-name computation on the rendered surface (manual-fallback: a
  described check the user confirms, same posture as
  `alawas-design-verify-design-implementation`).
- `content_search` — locate a stewarded accessibility-expectations pattern
  for the audited surface, when one exists.
- `structured_output` — produce the accessibility-audit report.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill performs only reads and observations — **low consequence**.
- No code, styles, markup, or design artifacts are modified.
- The audit report is written to the Evidence Ledger through the conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and
wait for explicit entry; do not silently start a continuous session.

The accessibility lens asks:

1. Was each finding checked against a real rendered surface, not assumed
   from markup alone?
2. Is the mechanism (browser-computed vs. static-parsed) disclosed per
   finding, since the two carry different blind spots?
3. Are deferred dimensions (keyboard, focus order, screen-reader behavior)
   named honestly, never silently folded into "passed"?

## Skill Grilling Profile

Apply the `alawas-design-audit-accessibility` profile and continuous
Grilling Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Identify the surface and mechanism

Identify the real rendered interface to audit. If browser automation is
available, use it to read computed styles and the live DOM/accessibility
tree. If not, degrade to static HTML/CSS parsing and record that
degradation explicitly — static parsing cannot see cascade, `:hover`/
`:focus` states, or JS-driven color, and any finding from it carries that
caveat.

### 2. Load the expectation baseline

Search for a stewarded `[system:pattern]` accessibility expectation covering
the audited surface. If found, use its stated expectations as the pass/fail
spec. If none exists, use WCAG's own generic thresholds (4.5:1 contrast for
normal text, 3:1 for large text; one logical heading per section; every
interactive element needs a discernible accessible name) and say plainly
that no project-specific expectation was available.

### 3. Check contrast

For each distinct text/background color pair on the surface, compute the
WCAG contrast ratio and compare against the applicable threshold. Report
pass/fail/undetermined with the concrete ratio — never a bare pass/fail
without the number behind it.

### 4. Check semantic structure

Check heading hierarchy (one logical top-level heading, no skipped levels),
whether interactive elements expose a discernible accessible name (visible
text, `aria-label`, or equivalent), and whether any state/severity signal
depends on color alone with no non-color backup (icon, text, weight, or
pattern).

### 5. Report deferred dimensions

State explicitly, as a named table, which dimensions this pass did not
check and why: keyboard navigation, focus order, and live screen-reader
announcement behavior all require interaction this version does not
simulate.

### 6. Produce the audit report

Assemble the `[system:accessibility-audit]` Evidence Ledger entry: the
surface audited, the mechanism used (browser-computed or static-parsed) and
its known blind spot, the baseline used (stewarded pattern or WCAG generic),
per-check findings with concrete values, and the deferred-dimensions table.

## Routing and termination

**Route when:**
- The audit report is complete — return to `alawas-governance-conduct-work-object`.
- A finding should be fixed — route to `alawas-design-apply-design-direction` with the
  specific finding as a candidate direction change; this skill does not fix
  it directly.
- No stewarded expectation exists for the surface and the director wants
  one — route to `alawas-design-steward-experience-patterns` to author it, then re-audit
  against it rather than the generic baseline.

**Terminate when:**
- The accessibility-audit report is recorded in the Evidence Ledger.
- All checkable dimensions are checked or explicitly deferred with reasons.

## Output contract

The `[system:accessibility-audit]` entry contains:

- `surface`: the file, URL, or dev-server path audited
- `mechanism`: `browser-computed` | `static-parsed`, plus its known blind
  spot
- `baseline`: `stewarded-pattern` (with a reference to the pattern) or
  `wcag-generic`
- `contrast_findings`: per-pair status (pass/fail/undetermined) with the
  concrete ratio and threshold
- `structure_findings`: per-check status with the concrete detail behind it
  (e.g., which element, what's missing)
- `deferred_dimensions`: table of dimension, deferred, and reason
- `overall`: a count summary (e.g., "N/M contrast pairs pass, N/M structure
  checks pass"), never a single pass/fail collapsing distinct findings

## Final self-check

- [ ] Every finding is checked against a real rendered surface, not assumed
- [ ] The mechanism (browser-computed vs. static-parsed) is disclosed, with
      its blind spot named
- [ ] The baseline used (stewarded pattern vs. WCAG generic) is disclosed
- [ ] Contrast findings carry the concrete ratio, not a bare pass/fail
- [ ] Deferred dimensions are named with reasons, never silently folded into
      a pass
- [ ] No code, style, markup, or design artifact was modified
- [ ] No compliance or certification claim was made from the findings alone
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

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

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
| `file_read` | `Read` | native |
| `browser_automation` | `—` | manual-fallback |
| `content_search` | `Grep` | native |
| `structured_output` | `—` | native |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Claude Code browser automation differs from Codex. Complex page interactions may require manual steps.
