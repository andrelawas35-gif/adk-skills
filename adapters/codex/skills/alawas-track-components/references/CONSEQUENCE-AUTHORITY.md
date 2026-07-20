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

## Authority gates

| Action | Low consequence | Meaningful consequence | High consequence |
|--------|----------------|----------------------|------------------|
| Create Work Object | Agent may proceed | Agent may proceed | Ask first |
| Update Work Object body | Agent may proceed | Agent may proceed | Ask first |
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
