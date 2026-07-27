# Epistemic Rules — Full (6‑tag)

This skill uses the complete 6‑tag epistemic system. Every evidence‑ledger
entry MUST use exactly one of the following tags:

| Tag | Meaning |
|-----|---------|
| `[system]` | Verified fact from a system, tool, or document |
| `[decision]` | Human decision with rationale and authority |
| `[inference]` | Reasoned conclusion from available evidence |
| `[gap]` | Known unknown — information that is missing or unresolved |
| `[testimony]` | Reported information from a person or source |
| `[memory]` | Prior observation from an earlier interaction |

Entries use the inline convention: `- [tag] <free text>`.

The 6‑tag system provides fine‑grained provenance tracking but requires the
model to reliably distinguish all six categories. When in doubt, use
`[inference]`.
