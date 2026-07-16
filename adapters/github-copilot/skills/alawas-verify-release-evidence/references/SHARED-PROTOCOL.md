# Personal Institution ↔ Work Studio Shared Protocol

**Protocol version: `0.1`**

This protocol defines the minimum, user-governed contract between separately
installable Personal Institution and Work Studio packages. It is a shared
reference, not a shared skill, archive, synchronization service, or identity
profile.

## Compatibility

A cross-package handoff is supported only when both packages declare Protocol
version `0.1`. A package declaring any other version is incompatible with this
release.

On version mismatch, the receiving package must report the unsupported handoff
and offer a manual, user-approved summary. It must not directly access, scan,
read, mutate, translate, or synchronize the other package's storage.

## Ownership and boundary

Personal Institution owns personal-memory records, the private evidence behind
them, Personalization Contract candidates, and confirmation of their updates.
Work Studio owns Work Objects, execution decisions, and delivery records.

Work Studio must not scan, read, or mutate the Personal Institution archive.
Personal Institution must not create or alter a Work Object unless the user has
explicitly requested Work Studio work. Neither package may treat current chat
history as a persistent personalization store.

## Evidence Bridge

An **Evidence Bridge** is the only routine path for personal context to enter a
Work Object. It is an approved handoff, not a copied personal-memory record.

Before creating or using an Evidence Bridge, the user must approve the proposed
handoff. The bridge contains only a Minimum-necessary summary or stable private
reference needed for the stated work; it never includes credentials, intimate
records, or unrelated private detail.

An Evidence Bridge records:

| Field | Requirement |
| --- | --- |
| User approval | The user's explicit approval for this handoff and receiving work |
| Receiving Work Object | Immutable Work Object ID, or a stated pending activation |
| Relevance | The concrete decision, inquiry, or task the bridge supports |
| Summary or reference | Minimum-necessary redacted summary or stable private reference |
| Provenance | `lived` or `inference`, with the source record or reasoning chain identified |
| Sensitivity | `ordinary`, `private`, or `restricted` |
| Limits | What the bridge does not establish or authorize |

Work Studio records a bridge as lived evidence only for a supplied direct
observation; an interpretation remains inference. A bridge must never be
relabeled as source evidence or system evidence.

## Personalization Contract

A **Personalization Contract** is a versioned collection of user-approved
guidance entries. It helps a relevant skill choose an approach but must not
establish identity, values, motives, or permanent preferences.

Every entry records:

| Field | Requirement |
| --- | --- |
| Type | Working-method, Active-lens, or Hard-boundary |
| Scope | The task contexts where the entry may guide a skill |
| Supporting evidence | Explicit, dated Personal Institution record references |
| Contrary evidence | Explicit, dated record references or `None known` |
| Confidence | `low`, `medium`, or `high` |
| Approval | User confirmation and date |
| Review trigger | The event or date that reopens the entry |
| Status | `active` or `inactive` for revisable entry types |

### Entry types

- **Working-method**: a testable, revisable way of working. It may guide a
  skill only in its stated scope.
- **Active-lens**: a narrow, current question or interpretive interest. It is
  never decorative and must be ignored for unrelated work.
- **Hard-boundary**: an explicit privacy, consent, safety, or authority rule.
  It remains active until explicitly revised.

Only explicit, dated Personal Institution records may support a candidate.
Current chat may guide the immediate interaction, but it must be deliberately
captured as a dated observation before it may support a candidate. A candidate
does not become active until the user confirms it.

When a Working-method or Active-lens review trigger passes without renewal, the
entry must become inactive. Inactive entries remain historical evidence and
must not guide skills by default. Hard-boundary entries remain active until the
user explicitly revises them.

## Use and degradation rules

Skills apply only active contract entries whose scope is relevant to the
current task. They default to neutral behavior when no relevant entry exists.
They may surface an inactive entry as clearly marked historical context, but
must not treat it as current guidance.

Missing approval, missing required bridge fields, or an incompatible protocol
version stops the cross-package handoff. The safe fallback is a manual,
user-approved summary supplied in the current interaction; it does not grant
archive access or permission to persist personalization.
