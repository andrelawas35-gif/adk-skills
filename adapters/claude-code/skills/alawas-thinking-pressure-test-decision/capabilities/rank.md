# Rank

## Purpose

Given two or more credible, materially distinct options with known evidence,
trade-offs, and reversibility, order them by confidence — never manufacture
confidence beyond what the evidence directly supports.

## Inputs

- A decision point where two or more credible, materially distinct options
  exist.
- The evidence, trade-offs, and reversibility known for each option.

## Output

- Each option labeled with a confidence level on a fixed three-level scale
  tied to evidence directness: high (direct, corroborated evidence), medium
  (partial evidence or stated assumptions), low (a consequential gap
  remains).
- Each option's stated trade-off, distinct from its evidence.

## Guarantees

- Confidence is calibrated against the fixed three-level scale, not an
  ad hoc judgment call.
- Each option's confidence is independently stated, not computed from an
  aggregate score.

## Limitations

- Does not aggregate multiple partial judgments into one score.
- Does not produce the final recommendation shape (Recommended + bounded
  Alternatives) — see `generate.md` for that.

## Does not own

- Whether ranking should proceed at all when every option is low
  confidence (an explicit refusal condition) — that policy belongs to the
  composing skill, not this capability.
- Whether ranking is warranted in the first place (only when credible,
  materially distinct options exist — not a default step for every
  decision) — the composing skill judges this before invoking `rank`.
- Which option is ultimately selected, or the authority that selection
  carries.

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
