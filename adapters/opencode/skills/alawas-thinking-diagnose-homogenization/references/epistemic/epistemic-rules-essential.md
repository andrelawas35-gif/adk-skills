# Epistemic Rules — Essential (3‑tag)

This skill uses the essential 3‑tag epistemic system. Every evidence‑ledger
entry MUST use exactly one of the following tags:

| Tag | Meaning |
|-----|---------|
| `[system]` | Verified fact from a system, tool, or document |
| `[decision]` | Human decision with rationale and authority |
| `[inference]` | Reasoned conclusion from available evidence |

Entries use the inline convention: `- [tag] <free text>`.

The 3‑tag system prevents the two worst hallucination modes: stating
unsourced facts as system‑verified, and stating inferences as decisions.
`[gap]`, `[testimony]`, and `[memory]` are collapsed into `[inference]` when
their finer category is uncertain.
