---
name: maintain-personal-memory
description: Organize and retrieve a personal archive of observations, recurring questions, projects, principles, and decisions before giving advice. Use when the user asks "what have I said about…?", "remember this," "what patterns do you see?", or asks for personal, strategic, career, creative, or project advice that should be grounded in their prior material.
---

# Maintain Personal Memory

Build continuity from evidence, not from a flattering story about the user. Retrieve relevant history before advising; distinguish what the user recorded from what the agent infers.

## Personal memory lens

Treat the archive as a personal institution: a record of lived scenes, recurring questions, experiments, commitments, and revisions. Preserve the user's attention to systems and people; maps, routes, borders, and circulation; logistics and labor; law, economics, software, and storytelling; and the gap between institutional categories and lived reality.

Do not turn those interests into a fixed identity. Keep direct, question-led language and tensions intact. A pattern is provisional until it appears across dated material.

## Archive model

Use an existing archive convention when it exists. Otherwise, create folders lazily under the user-named archive root:

```text
observations/        # Source-preserving records from capture-lived-evidence
questions/           # Questions that recur across time or projects
projects/            # Experiments, artifacts, encounters, and reviews
principles/          # Provisional rules the user has adopted or is testing
decisions/           # Choices made, alternatives considered, and revisit triggers
```

Keep the categories distinct:

| Type | Contains | Must not become |
| --- | --- | --- |
| Observation | What was seen, said, felt, or noticed | An explanation of why it happened |
| Question | A live, recurring inquiry | A goal merely because it sounds impressive |
| Project | A bounded attempt to encounter reality or make an artifact | An identity claim |
| Principle | A provisional rule with supporting and contrary evidence | A permanent value assigned by the agent |
| Decision | A human choice in context | A recommendation the agent silently made |

Use `capture-lived-evidence` for new raw material. Link to its dated observation records; do not rewrite them to make them fit a later narrative.

## Retrieval before advice

For every advice request or question about the user's history:

1. Identify the exact topic, decision, project, or tension in the request.
2. Search the five record types. Retrieve the smallest useful set of dated records, prioritizing direct statements and recent material while retaining older material when it changes the picture.
3. State the evidence before the interpretation. Surface contradictions, reversals, and gaps rather than smoothing them away.
4. If no relevant archive exists, say so plainly. Ask for material or offer a general answer explicitly marked as ungrounded; never invent continuity.
5. Generate options before a recommendation. Keep values, relationships, identity, and irreversible commitments human-owned.

## Advice response format

Use this format whenever prior material is available:

```markdown
## Relevant history

- [YYYY-MM-DD — record type: concise, source-grounded point]

## Reading of the evidence

[Clearly label this as an inference. Include counterevidence or uncertainty.]

## Options

1. [Option and trade-off]
2. [Option and trade-off]

## Recommendation

[A conditional recommendation tied to the evidence, or “No recommendation yet.”]

## Unknowns / next evidence

- [What must be observed, asked, tested, or decided by the user]
```

Do not use this structure to inflate a thin record. With only one observation, report one observation and its limits.

## Updating the archive

Write or revise a record only when the user asks to remember, organize, record a decision, update a project, or save the outcome of a discussion. Preserve dates and source links. Add a principle only when the user explicitly adopts or tests it. Add a decision only after the user makes it; record the alternatives and revisit trigger when supplied.

When a question repeats across at least two dated records, create or update a question record with links to both. When evidence conflicts, retain both sides and mark the question unresolved.
