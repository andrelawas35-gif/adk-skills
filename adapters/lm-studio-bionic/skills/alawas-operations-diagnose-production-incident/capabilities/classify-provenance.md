# Classify Provenance

## Purpose

Attach exactly one provenance tag to a piece of evidence at capture time,
marking where it came from — not whether it is true, verified, or approved.

## Inputs

- A claim or piece of evidence being recorded, at the moment it enters an
  Evidence Ledger entry.

## Output

- Exactly one tag from the canonical set defined in
  [`references/AGREEMENT-LOOP.md`](../references/AGREEMENT-LOOP.md) (lines
  96–111): `[system]`, `[decision]`, `[memory]`, `[testimony]`,
  `[inference]`, `[gap]`.
- Applied inline: `- [tag] <free text>`.

Some contexts use a reduced 3-tag variant (`[system]`, `[decision]`,
`[inference]`) that collapses `[gap]`, `[testimony]`, and `[memory]` into
`[inference]` when the finer category is uncertain — see
[`references/epistemic/epistemic-rules-essential.md`](../references/epistemic/epistemic-rules-essential.md)
and
[`references/epistemic/epistemic-rules-full.md`](../references/epistemic/epistemic-rules-full.md)
for the two variants and which skills use which.

## Guarantees

- The tag is a provenance marker, not a verdict — no `verified` flag, no
  confidence score, no state meaning "established."
- Applied at capture time; not retroactively upgraded by later confidence.

## Limitations

- Does not resolve conflicts between differently-tagged claims about the
  same fact — see the confidence-labeling and conflict-comparison rules in
  `references/AGREEMENT-LOOP.md`'s Grounding and personalization section.
- The reduced 3-tag variant has a documented degraded mode: finer
  distinctions between `[gap]`, `[testimony]`, and `[memory]` are lost when
  collapsed to `[inference]`.

## Does not own

- What a tag implies for a downstream decision — that is Agreement Loop /
  Evidence Model governance, not this operation.
- Whether a claim is true — provenance and truth are separate questions.

## Source

Promoted from content independently present in
[`references/AGREEMENT-LOOP.md`](../references/AGREEMENT-LOOP.md),
[`references/EVIDENCE-MODEL.md`](../references/EVIDENCE-MODEL.md),
[`references/epistemic/epistemic-rules-essential.md`](../references/epistemic/epistemic-rules-essential.md),
and
[`references/epistemic/epistemic-rules-full.md`](../references/epistemic/epistemic-rules-full.md).
Recorded as a capability by Work Object `2026-08-15-010` Decision 5, on
2026-08-15.
