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
