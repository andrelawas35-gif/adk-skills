# Evidence Model

This document describes how evidence entries attach to a persisted Work
Object's Evidence ledger section. For the canonical provenance tag taxonomy
and rules governing tag usage, see `references/AGREEMENT-LOOP.md` (lines
96-111), which is the single authoritative source for tag definitions and
the laundering guard.

## In the Work Object

Evidence ledger entries use an inline-tag convention:

```
- <ISO8601 timestamp> — [tag] <free text>
```

Where `[tag]` is one of: `[system]`, `[decision]`, `[inference]`, `[gap]`,
`[testimony]`, or `[memory]` — as defined in `AGREEMENT-LOOP.md`. No
structured fields (`**Provenance**:`, `**Claim**:`, `**Source**:`,
`**Confidence**:`, `**Corroboration**:`) are used in real Work Objects;
the inline-tag convention is the canonical format.

The Evidence ledger is append-only (ADR 0017, widened by ADR 0022).
Correction happens by appending a new entry, never by editing an existing
one. Timestamps must be unique at whole-second precision within a Work
Object.

Evidence entries carry provenance markers at capture time — what is known
now, not what might be known later. The producer writes a tag and free text
without needing confidence, corroboration, or structured field values that
may not be available at the moment of observation.

## Confidence on a decision record

A decision's `Confidence` field states a label **and its basis**. A bare
`high` records a feeling, not a judgement someone else can check or revisit.

When the parts of a decision are not equally well supported, scope-qualify the
label rather than averaging it:

```
| **Confidence** | high for the bounded local behavior; no claim about later
lived use — basis: the check ran here, nothing observed in use |
```

This is not a new requirement so much as a recorded one. Authors have already
written scope-qualified confidence by hand when a single label could not carry
what they meant; the field permits it explicitly so the practice is uniform.

Do not decompose confidence into a fixed set of sub-scores, and do not
aggregate the label with any other field into a single epistemic number. A
single score obscures calibration, resolution, base rates, and decision
utility, and optimizing one scoring rule need not serve every decision that
reads it ([Kleinberg et al., 2023](https://proceedings.mlr.press/v195/kleinberg23a.html)).
Probabilities and scoring rules earn their keep on repeated forecasts with
observable outcomes; a one-off architectural judgement is not that. Use a
qualitative label, always with a reason and a revisit condition.

## Projections of the record

Any view over Work Objects — a report, a summary, a graph, a dashboard — is a
read-only projection. It never becomes a source, and writing to it is not a
way to change what the record says.

**A missing edge means "not recorded," not "false."** An absent link, an empty
section, or a sparse graph reports the limits of what was captured. Reading it
as a negative finding converts a gap into evidence, which is the laundering
this model exists to prevent.
