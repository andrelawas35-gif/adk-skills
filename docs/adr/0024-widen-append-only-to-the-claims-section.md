# Widen Append-Only Scope to the Claims Section

- **Status:** Accepted
- **Date:** 2026-08-09
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (grilling session 2026-08-09, branch A accepted)
- **Related Work Object:** `2026-08-09-002` — Add conflict resolution to the schema so the gauge can fall
- **Related ADRs:**
  - revises: ADR 0022 (widens scope from three sections to four)
  - complements: ADR 0017 (the original History-only rule remains correct)
- **Supersedes:** None (ADR 0022's decisions remain correct; this ADR widens the scope, it does not reverse)
- **Superseded by:** None

## Context

ADR 0022 widened append-only protection from History alone to three sections:
History, Decisions and revisit triggers, and the Evidence ledger. Its governing
argument was that a freely-editable section must not be load-bearing for
enforcement — a gate could be passed or failed by editing a past entry's fields
after the fact.

The `## Claims` section did not exist when ADR 0022 was written. It was created
by `2026-07-27-016` (claim sidecar) and extended by `2026-07-27-019` (conflict
records). It now holds every `CLM-` and `CONF-` record in the workspace.

Two facts made its status decision-bearing:

**The section became load-bearing.** `tools/ws/dashboard_signals.py` reads
`## Claims` to compute both epistemic-pressure signals — unresolved conflicts
and claims below support adequacy. ADR 0022's argument now applies to Claims by
the same reasoning it used for Decisions: a mutable section means the signal
measures what someone last typed rather than what happened. An agent could make
the conflict gauge fall by rewriting a record instead of resolving a conflict.

**The conflict schema needs somewhere to record resolution.** The owner
confirmed the unresolved-conflicts count is a gauge — it should fall when a
conflict is resolved. `tools/ws/conflict.py` has no `resolution`, `status`, or
`disposition` field, so the count is structurally monotonic. Adding resolution
requires choosing between mutating the existing `CONF-` block and appending a
new record, and that choice depends entirely on whether Claims is protected.

## Decision

**The append-only rule applies to four Work Object body sections:** History,
Decisions and revisit triggers, the Evidence ledger, and **Claims**.

- Existing `CLM-` and `CONF-` blocks must not be edited, deleted, reordered, or
  renumbered.
- New records may only be appended to the section.
- Correction happens by appending a record that supersedes or clarifies the
  prior one, never by editing in place.

**A conflict is resolved by appending a `CONFRES-` record** that names the
conflict, the resolver, the disposition, and the rationale. The `CONF-` block
is never modified. `count_unresolved_conflicts` counts `CONF-` blocks with no
matching `CONFRES-`.

This extends to claim states. `2026-07-27-016` shipped three claim states
(`captured`, `supported`, `accepted_for_action`) intended to move between each
other. Under this ADR, moving a claim's state requires an appended record, not
an edit to its `state:` field. No claim has ever moved, so nothing breaks today,
but any future claim state machine must be append-based.

## Consequences

**Adopting the rule costs nothing today.** `tools/ws/claim.py:214` and
`tools/ws/conflict.py:199` both use `append_to_section`, and no update or edit
path exists for either record type. The Claims section is already append-only in
practice; this ADR declares what the code already does. There is no migration.

**The cost lands on resolution.** A resolved conflict is two records rather than
one, and the counter must join them rather than reading a field.

**Three properties come with the appended shape.** Both sides' pinned `versions`
survive untouched, satisfying Tracer 1's success criterion that "neither docs
nor code silently wins". Premature closure — the failure mode named for the
Conflict type in the epistemic engineering research — becomes auditable, because
the resolution is a dated record with a named resolver rather than a flipped
field. And a wrong resolution can be superseded without erasing the first
attempt.

**Enforcement is currently declaratory, and this ADR does not fix that.**
`tools/ws/validate.py` states at two points that full append-only verification
"requires git history comparison (as verify-append-only.py does)".
`tools/verify-append-only.py` is a deprecated wrapper whose body shells out to
`python3 -m tools.ws validate append-only`. The two point at each other: the
git-diff enforcement ADR 0022 mandated does not exist for any of the now-four
sections. This ADR adds Claims to a list no script checks. It governs agent
behavior through the constitution rather than through a gate that can fail, and
the gap is recorded here so that building the enforcement script covers four
sections rather than three.

## Alternatives considered

**Leave Claims unprotected; resolution as an in-place `resolution:` field.**
Simplest implementation, one record. Rejected because it makes the gauge
falsifiable by edit, and because the first in-place mutation would establish
editing as normal for the section holding every claim and conflict — reversing
that later would mean migrating live records rather than declaring a rule over
code that already complies.

**Protect `CONF-` but not `CLM-`.** Rejected without full costing: a split rule
inside one section is harder to state than either uniform rule, and no evidence
distinguishes the two record types on this axis.

## Revisit trigger

A decision that the append-only enforcement script will never be built. Without
enforcement this rule reduces to convention, and the simplicity of in-place
mutation becomes the stronger case. Secondary trigger: the first time a
resolution must itself be corrected, if the supersession chain proves unreadable
in practice.
