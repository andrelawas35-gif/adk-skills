# Generate Recommendation (superseded)

This capability has been split into two smaller primitives:

- [`rank.md`](rank.md) — compare and confidence-order options.
- [`generate.md`](generate.md) — produce the bounded Recommended +
  Alternatives output shape from ranked options.

Split by Work Object `2026-08-17-013` Decision 2, on 2026-08-17, after gap
resolution found this capability was not composed by any skill (documented
as "restated independently" in the section below, rather than referenced).
`thinking-pressure-test-decision/SKILL.md`'s branch-walk step now points to
`rank.md` and `generate.md` directly; the cap-at-3/refusal-condition policy
and the judgment of when a recommendation is warranted at all moved to that
skill, since gap resolution found no evidence either was reused as a
primitive elsewhere.

Preserved below for reference; not the current canonical content.

---

## Purpose (original, superseded)

Given a decision point with credible, materially distinct options, produce
one ranked recommendation with bounded alternatives — never an unranked
menu, never a forced choice when nothing clears the confidence bar.

## Inputs

- A decision point where two or more credible, materially distinct options
  exist.
- The evidence, trade-offs, and reversibility known for each option.

## Output

- One **Recommended** option: confidence, supporting evidence, trade-off,
  and what would change the recommendation.
- At most two **Alternative** entries, each with a confidence level and one
  distinct trade-off — not restated evidence.
- Confidence is calibrated on a fixed three-level scale tied to evidence
  directness: high (direct, corroborated evidence), medium (partial
  evidence or stated assumptions), low (a consequential gap remains).

## Guarantees

- Capped at 3 options total (1 recommended + up to 2 alternatives).
- Explicit refusal condition: when every credible option is low confidence,
  do not manufacture a ranked choice — say so instead.
- Only produced when credible, materially distinct alternatives would
  actually help; not a default output shape for every response.

## Limitations

- Does not decide for the user — a recommendation is offered, not enacted.
- Does not aggregate multiple partial judgments into one score; each
  option's confidence is independently stated, not computed.

## Does not own

- Which option is selected, or the authority that selection carries.
- Whether accepting the recommendation authorizes anything beyond its
  stated scope — see `references/CONSEQUENCE-AUTHORITY.md` for authority
  rules governing what a recommendation's acceptance does and does not
  grant.

## Source

Promoted from content independently present in
[`references/AGREEMENT-LOOP.md`](../references/AGREEMENT-LOOP.md) (the
"Choice Frame," lines 199–225) and restated independently in
[`skills/core/thinking-pressure-test-decision/SKILL.md`](../skills/core/thinking-pressure-test-decision/SKILL.md)'s
branch-walk step (list viable branches, recommend one, state the trade-off
and confidence, ask one question). Recorded as a capability by Work Object
`2026-08-15-010` Decision 5, on 2026-08-15.
