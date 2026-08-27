# V0 Proof Packet Template

Each of the five proof cases (S001-S005) follows this packet shape. It defines
what goes in, what the critic must return, and how a human judges the result.

## Packet shape (Work Object 2026-08-23-002 Decision 10)

| Field | Content |
|-------|---------|
| `shot_id` | The case id, e.g. `S001` |
| `before image` | The generated before image (file reference) |
| `shot_object` | Small structured intent: `intent`, `subject`, `camera`, `mood`, `preserve`, `change`, `avoid` |
| `required critic output schema` | The structured critique the model must return (below) |
| `human_judgment` | The fields the director fills in after revising (below) |

## Required critic output schema (Decision 6)

V0 emits structured revision instructions only — diagnosis, protect lists,
revision targets, instructions, reasons, and avoid lists. It does NOT emit
executable ComfyUI parameter changes.

```json
{
  "shot_id": "S001",
  "critique": {
    "diagnosis": "<what is wrong and why it misses intent>",
    "protect": ["<what must not change>"],
    "revision_targets": ["<what to fix, mapped to the shot object's change list>"],
    "instructions": ["<how to fix, step by step>"],
    "reasons": ["<why each instruction improves it against intent>"],
    "avoid": ["<what to avoid, mapped to the shot object's avoid list>"]
  }
}
```

## Human judgment (Decisions 7 & 10)

```json
{
  "human_judgment": {
    "better_against_intent": "yes|no|partial",
    "preserve_violations": ["<any preserved element that was changed>"],
    "avoid_violations": ["<any avoid list element that appeared>"],
    "notes": "<free text>"
  }
}
```

## Success threshold (Decision 7)

At least 3 of 5 revised images are clearly better against shot intent, with
zero preserve/avoid violations.
