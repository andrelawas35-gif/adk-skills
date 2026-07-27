# Consequence and Authority

Consequence and sensitivity are independent axes. Both govern what gates apply.

## Consequence levels

| Level | Definition | Required gates |
|-------|------------|----------------|
| **Low** | Private, cheap, reversible. | Stages may be compressed. No formal decision record required. |
| **Meaningful** | Affects durable data, substantial effort, public artifacts, or other people. | Framing evidence, decision record, and verification evidence required. |
| **High** | Affects safety, privacy, money, production, irreversible data, identity claims, or external commitments. | Explicit human authority required for every transition. Verification, recovery plan, and post-deployment observation required. |

Consequence follows effects, not emotional intensity or urgency.

## Sensitivity classes

| Class | Definition | Storage rules |
|-------|------------|---------------|
| **Ordinary** | Normal project information. | Standard Git or workspace storage. |
| **Private** | Personal, proprietary, financial, relationship, or internal operational information. | `.work-studio/` (Git-excluded). No automatic export. |
| **Restricted** | Credentials, intimate regulation history, security-sensitive infrastructure, identity documents, or similarly harmful material. | Never store in Work Objects. Link to protected sources; reference by pointer only. |

Work Studio must not scan, read, or mutate a personal archive it does not own.
Personal context enters a Work Object only as a minimum-necessary summary the
user supplies and approves for that Work Object, recorded with its provenance
and sensitivity. An interpretation of personal context remains `[inference]`
and must never be relabelled as system evidence.

## Authority gates

| Action | Low consequence | Meaningful consequence | High consequence |
|--------|----------------|----------------------|------------------|
| Create Work Object | Agent may proceed | Agent may proceed | Ask first |
| Update Work Object body | Agent may proceed | Agent may proceed | Ask first |
| **Write restricted-sensitivity body content** | **Ask first** | **Ask first** | **Ask first** |
| Modify frontmatter `status` or `state` | Agent appends History | Agent appends History | Ask first |
| Export or share | Ask first | Ask first | Ask first |
| Destructive action | Ask first | Ask first | Ask first |
| Schema migration | Ask first | Ask first | Ask first |
| Write to external systems | Ask first | Ask first | Ask first |
| Deployment | Not applicable | Ask first | Ask first |

## Implicit authority

The following require no additional confirmation:
- Reading Work Objects within the current workspace
- Appending History entries for routine transitions
- Updating `updated_at` on any write
- Recording evidence and decisions discussed in the current conversation

## Explicit authority

The following always require explicit human confirmation:
- Destructive operations (delete, reset, force-push)
- External writes (outside `.work-studio/` and the current workspace)
- Deployments, exports, or sharing of any kind
- Schema migrations
- Changing a Work Object's `type` (which should be done via successor, not mutation)

`just execute` accepts the current recommendation within stated scope and records its assumptions and revisit trigger. It never bypasses safety, privacy, destructive-action, or external-commitment gates.

## Structured authority records

When the system requires explicit human confirmation for an action (per the
authority gates table above), the authorization and its scope must be recorded
in the Work Object's History section — not left in ephemeral chat.

### Authority History entry format

```markdown
### YYYY-MM-DDTHH:MM:SSZ — Authority: <gated action name>

- **Scope:** <affected files, systems, or objects>
- **Evidence reviewed:** <what was checked before granting>
- **Constraints:** <any limits the user attached, or "none">
- **Authority mode:** accepted-recommendation | independent-authorization
- **Granted by:** <user identifier or "conversation">
```

### Authority modes

- `accepted-recommendation` — the agent proposed a specific action and the user
  confirmed it. The recommendation is recorded in the History entry immediately
  preceding the authority entry.
- `independent-authorization` — the user directed the action without an agent
  recommendation. The direction replaces the recommendation in the preceding
  entry.

Non-gated History entries remain freeform. A gated-action History entry must
capture: (1) the gated action name, (2) the scope granted, (3) the evidence
reviewed before granting, and (4) any constraints the user attached.

## Consequence assignment

Before setting `consequence:` in a Work Object's frontmatter, the agent must
answer three structural questions. The answers must be recorded as the Work
Object's first History entry.

### Consequence assessment prompt

```markdown
### YYYY-MM-DDTHH:MM:SSZ — Consequence assessment

- **Reversible?** yes | no → <implication>
- **Affects beyond workspace?** yes | no → <implication>
- **Failure affects safety/privacy/money?** yes | no → <implication>
- **Assigned consequence:** low | meaningful | high
```

### Decision rules

1. Is the action reversible? If no → at least `meaningful`.
2. Does it affect systems or people beyond this workspace? If yes → at least
   `meaningful`.
3. Could a failure here affect safety, privacy, or money? If yes → `high`.

Consequence follows effects, not emotional intensity or urgency. When in doubt
between two levels, choose the higher one and record the reasoning in the
assessment entry.

## Auditable-but-not-preventable actions

Five action categories cannot be mechanically prevented until a
platform-agnostic CLI exists:

1. Export
2. Destructive actions
3. Schema migration
4. External writes
5. Deployment

These are auditable through structured authority History entries but are not
preventable at runtime. The CLI becomes the highest-priority enforcement
deliverable. Until then, the pre-commit hook, inlined skill authority checks,
and structured authority records provide defense-in-depth through prompt-level,
commit-level, and audit-level enforcement.
