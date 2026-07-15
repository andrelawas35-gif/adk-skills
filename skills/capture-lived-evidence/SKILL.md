---
name: capture-lived-evidence
description: Convert notes, voice dumps, photos, and conversations into dated, source-preserving observation records without premature interpretation. Use when the user says "log this," "capture this thought," "save this observation," or provides a personal note, transcript, photo, or conversation to preserve for later reflection.
---

# Capture Lived Evidence

Capture what happened before explaining what it means. Produce an observation record that can support later reflection without smuggling in a conclusion.

## Capture workflow

1. Identify the source: `note`, `voice dump`, `photo`, `conversation`, or `mixed`.
2. Date the record using the current local date when available. Preserve a user-provided event date separately when it differs from the capture date. Never guess a time, location, speaker, identity, intention, emotion, or cause.
3. Preserve the user's original wording. For a voice dump or conversation, retain short salient excerpts verbatim; label paraphrases as paraphrases.
4. Write only what was observed, said, done, felt, or explicitly thought. Use concrete, sensory, behavioral language.
5. Separate uncertainty from fact. Use `Unknown` or a question rather than filling gaps.
6. Do not interpret, diagnose, advise, turn the record into a goal, infer identity, or connect it to prior patterns unless the user explicitly requests a second reflective step.

## Record format

Return one Markdown record unless the user asks for another format:

```markdown
## Observation — YYYY-MM-DD

- **Captured:** YYYY-MM-DD [time and timezone if known]
- **Event date:** YYYY-MM-DD | Unknown
- **Source:** note | voice dump | photo | conversation | mixed
- **Context:** [place, situation, or participants only when supplied]

### Record

[A concise factual account. Preserve relevant first-person experience as reported: “I felt…”, “I noticed…”, “I thought…”.]

### Exact language

> [Short, material quote(s), or “None retained.”]

### Unknown / to preserve

- [Ambiguity, missing context, or unanswered factual question]

### Interpretation

Deferred.
```

For a photo, describe visible details and user-supplied context. Do not identify people, infer relationships, diagnose emotions, or assert unseen events. For a conversation, distinguish direct quotations from the user's recollection and attribute only when the speaker is known.

## Storage

Return the record in chat by default. Save or append it only when the user names a file or has established an archive location in the current task. Preserve existing archive conventions; otherwise use one Markdown file per observation and never silently overwrite material.

## Reflection handoff

If the user asks what an observation means, finish the capture first, then explicitly begin a separate reflection. Cite the observation record and label every inference as an interpretation.
