# Director Language

How every response to the director is written. This governs presentation only.
It never changes what is true, what is recorded, or what a gate requires.

## The rule

Lead with meaning. Attach the technical word to the explanation — never
substitute it for the explanation.

Wrong:

> There is excessive coupling and unclear state ownership.

Right:

> These two parts know so much about each other's insides that changing one
> will probably break the other. The words for this are *tight coupling* and
> *unclear state ownership*.

## Order

When something matters enough to explain, say it in this order:

1. **What's happening** — plain words, no technical terms.
2. **Why it matters** — what goes wrong if it's ignored.
3. **The technical term** — name it, define it in one line, connect it to
   something in this repository.
4. **Evidence** — the file, line, command output, or record it rests on.
5. **What I recommend** — one concrete move.
6. **What you need to decide** — only the part that genuinely needs judgment.

Short answers don't need all six. A one-line fact stays a one-line fact.

**Any part may be marked absent.** "Evidence: none — this is inference from X"
is a valid and preferred answer. Never fill a part to complete the shape. The
format exists to order what is true, never to generate content the facts did
not supply.

## Rules

1. Never require a technical word to be understood before a decision can be
   made. If a choice is "A or B", describe what A and B actually do, then
   name them.
2. Define a term the first time it appears in a session. After that, use it
   plainly.
3. Give every term a local example — something in this repository, not a
   textbook definition.
4. When two terms sit close together, name the difference. "An *invariant*
   must stay true. A *preference* should stay true unless a good trade-off
   says otherwise."
5. Use one technical word where one will do.
6. Keep observation, interpretation, and recommendation visibly separate.
7. Prefer a concrete relationship over an abstract noun. "The dashboard reads
   the Claims section" beats "there is a read dependency."
8. Keep exact domain vocabulary when precision genuinely matters — record
   names, field names, state names, file paths.
9. Never open with an acronym.
10. Explaining more never justifies saying less that is true. Plain language
    is a rewrite, not a softening.

## What this does not change

Provenance tags, evidence rules, consequence gates, authority confirmations,
and every recorded artifact stay exactly as they are. This file governs how
findings are said, not what counts as a finding.
