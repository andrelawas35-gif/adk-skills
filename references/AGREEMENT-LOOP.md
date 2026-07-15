# Agreement Loop

The shared reasoning protocol for all Work Studio skills. Activates only at
unresolved decision boundaries — it is not a conversational loop for every
exchange.

## When to activate

The Agreement Loop activates when:
- A genuine decision with multiple viable branches exists
- The user has not already given clear authority
- The choice materially affects the Work Object outcome
- Further questions would change the recommendation

It does NOT activate for:
- Routine operational steps within established authority
- Questions answerable by reading existing evidence
- Already-decided matters (check Decisions section first)
- When the user has said `do recommended` or `just execute`

## Steps

1. **Orient** — Ground in the Work Object, memory, evidence, consequence, and current state. What do we know? What is decided? What is unresolved?

2. **Map** — Identify unresolved branches, dependencies, contradictions, and missing evidence. Surface what's at stake.

3. **Recommend** — Give ONE recommended answer with supporting evidence, trade-offs, and confidence level. Do not present a menu.

4. **Ask** — Ask exactly ONE decision-bearing question. Make it specific and answerable.

5. **Integrate** — Record the user's answer as a Decision with rationale and revisit trigger.

6. **Generate novelty** — Only when it changes the option space. Do not churn alternatives for their own sake.

7. **Test** — Test the emerging agreement with an edge case or failure scenario.

8. **Converge or route** — If agreement is sufficient, proceed. If not, loop back or route to a more appropriate skill.

## Termination conditions

The loop stops when:
- Agreement is sufficient and action can proceed
- Action or external evidence is needed before further deliberation
- Further questions will not change the recommendation
- The user proceeds with documented uncertainty
- Another skill is more appropriate for the situation

## Anti-patterns

- **Ceremony inflation**: Running the full loop for trivial choices
- **Interrogation fatigue**: Asking multiple sequential questions without progress
- **Menu dumping**: Presenting options without a recommendation
- **Loop cycling**: Revisiting settled decisions without new evidence
- **Novelty churn**: Generating alternatives that don't change the option space
