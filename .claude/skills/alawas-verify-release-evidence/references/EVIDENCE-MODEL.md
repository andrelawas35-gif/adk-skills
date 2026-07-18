# Evidence Model

Evidence is categorized into provenance lanes. Memory retrieves records into
these lanes; memory is not itself evidence.

## Provenance lanes

| Lane | Definition | Examples |
|------|------------|----------|
| **Lived Evidence** | Dated observations, conversations, field encounters, direct experience | User reports, observed behavior, personal notes |
| **Source Evidence** | Papers, documentation, laws, records, attributable external material | API docs, specifications, legal texts, research papers |
| **System Evidence** | Code, tests, logs, metrics, browser checks, deployment results | Test output, type errors, build logs, runtime metrics |
| **Inference** | Interpretation connecting available evidence | "Based on A and B, we infer C" |
| **Decision** | A human-owned choice with alternatives, rationale, and revisit trigger | Architecture decisions, design choices, scope decisions |

## Rules

1. Every factual claim must carry a provenance marker: `[lived]`, `[source]`, `[system]`, `[inference]`, or `[decision]`.
2. Inference must be clearly distinguished from direct evidence.
3. Uncertainty must be stated explicitly: "The paper says X [source], but the sample size is small."
4. Decisions record alternatives considered, rationale, and revisit triggers.
5. Do not launder inference as source evidence.

## In the Work Object

The Evidence ledger section in a Work Object body records entries as:

```markdown
### YYYY-MM-DD — <summary>

- **Provenance**: lived | source | system | inference | decision
- **Claim**: What is asserted
- **Source**: Attribution (person, document, system, reasoning chain)
- **Confidence**: high | medium | low
- **Corroboration**: Supporting or contradicting evidence
```
