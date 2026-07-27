# Epistemic Rules — Binary (2‑tag)

This skill uses the binary epistemic system. Every evidence‑ledger entry
MUST use exactly one of the following tags:

| Tag | Meaning |
|-----|---------|
| `[verified]` | Confirmed fact — system‑verified or directly observed |
| `[unverified]` | Unconfirmed or uncertain — includes inferences, testimony, gaps, and memory |

Entries use the inline convention: `- [tag] <free text>`.

The binary system minimises tag‑confusion risk on models with limited
epistemic‑category reasoning. All finer distinctions (`[decision]`,
`[inference]`, `[gap]`, `[testimony]`, `[memory]`) are collapsed into
`[unverified]` unless the model has direct system confirmation.
