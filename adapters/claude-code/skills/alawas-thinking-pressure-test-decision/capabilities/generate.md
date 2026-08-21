# Generate (recommendation shape)

## Purpose

Given ranked options (confidence-labeled, trade-off-stated), produce one
bounded recommendation output: a single Recommended option plus at most two
Alternatives — never an unranked menu.

## Inputs

- Options already ordered and confidence-labeled by `rank.md`.
- Each option's stated trade-off and supporting evidence.

## Output

- One **Recommended** option: confidence, supporting evidence, trade-off,
  and what would change the recommendation.
- At most two **Alternative** entries, each with a confidence level and one
  distinct trade-off — not restated evidence.

## Guarantees

- Capped at 3 options total (1 recommended + up to 2 alternatives).
- Each Alternative states a genuinely distinct trade-off, not a repeat of
  the Recommended option's evidence in different words.

## Limitations

- Does not decide for the user — a recommendation is offered, not enacted.
- Does not itself compute confidence — that is `rank.md`'s job; this
  capability only shapes the output from already-ranked input.

## Does not own

- Whether to produce a recommendation at all when every credible option is
  low confidence (an explicit refusal condition) — that policy belongs to
  the composing skill, not this capability.
- Whether a recommendation is warranted in the first place (only when
  credible, materially distinct alternatives would actually help — not a
  default output shape for every response) — the composing skill judges
  this before invoking `generate`.
- Which option is selected, or the authority that selection carries.
- Whether accepting the recommendation authorizes anything beyond its
  stated scope — see `references/CONSEQUENCE-AUTHORITY.md` for authority
  rules governing what a recommendation's acceptance does and does not
  grant.

## Source

Split from `generate-recommendation.md` (WO `2026-08-17-013` Decision 2),
which was promoted from content independently present in
[`references/AGREEMENT-LOOP.md`](../references/AGREEMENT-LOOP.md) (the
"Choice Frame," lines 199–225) and restated independently in
[`skills/core/thinking-pressure-test-decision/SKILL.md`](../skills/core/thinking-pressure-test-decision/SKILL.md)'s
branch-walk step. Recorded by Work Object `2026-08-15-010` Decision 5 on
2026-08-15; split into `rank.md` and `generate.md` by Work Object
`2026-08-17-013` on 2026-08-17 after gap resolution found `capabilities/`
was not yet composed by any skill.
