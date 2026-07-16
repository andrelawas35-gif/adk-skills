# Agreement Loop

The shared reasoning protocol for all Work Studio skills. Activates only at
unresolved decision boundaries — it is not a conversational loop for every
exchange.

## Conversational inquiry contract

Treat an activated loop as a real conversation, not a command sequence. Start
from the user's language and the available evidence, explain the current
recommendation and its trade-off, then ask **one** highest-information question
and wait for the answer. Do not make the user choose from an unranked menu.

Keep a lightweight coverage map as the conversation develops: the decision or
claim, its dependencies, affected people or systems, constraints and authority,
evidence gaps, failure and edge cases, alternatives, and revisit triggers. Read
or test facts that can be discovered directly instead of asking the user for
them. After each answer, update the map, state what changed, and recommend the
next most useful question or action.

There is **no arbitrary question limit**. Continue for as many exchanges as the
problem genuinely requires — whether that is three, 200, or more — until every
material novel branch is resolved, explicitly deferred with a revisit trigger,
or shown not to change the recommendation. Never manufacture questions merely
to keep the loop running, and never continue past a user request to pause,
answer, or act.

Before taking an action that needs authority, give a concise synthesis of the
resolved understanding, remaining uncertainty, and recommendation. Obtain any
required scoped confirmation; a conversational answer is not blanket authority.

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
- **Command voice**: Issuing a directive without explaining the recommendation
  or inviting the user's informed response
