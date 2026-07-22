# Git Commit SHAs as Lightweight References, Not Embedded Artifacts

- **Status:** Accepted
- **Date:** 2026-07-22
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (Grilling Session 13, ephemeral)
- **Related Work Object:** None — ephemeral grilling session
- **Related ADRs:**
  - complements: ADR 0017 (append-only History — commit SHAs are appended to History entries)
  - complements: ADR 0022 (append-only Evidence ledger — `[system]` entries may carry optional SHA)
  - related to: ADR 0014 (component ledger — `track-components` already stores `last-grilled-SHA`)
- **Supersedes:** None
- **Superseded by:** None

## Context

Work Studio and Git are two record-keeping systems in the same repository with no structured link between them. Work Objects store workflow reasoning — decisions, uncertainty, evidence provenance, authority records, lifecycle state, hypotheses, and outcome reviews. Git stores code artifacts — diffs, authorship, file lists, test output, deployment state. Neither system references the other.

The append-only verifier (`tools/verify-append-only.py`) once used Git history comparison but was deprecated in favor of structural checks. The `track-components` skill stores `last-grilled-SHA` for drift detection, but no other part of the system records a commit SHA. No Work Object references the commit that implemented its decisions. No commit message references the Work Object that authorized it.

The question: what workflow information belongs in Work Objects, and what should remain referenced from Git?

## Decision

Work Studio stores **workflow reasoning**; Git stores **code artifacts**. The commit SHA is the single bidirectional link — lightweight, immutable, and never duplicated. Git is authoritative for diffs, authorship, code history, file lists, test output, branch names, PR status, and deployment identifiers. Work Studio references Git by commit SHA at three points and embeds nothing that Git can regenerate.

### Five specific decisions

1. **Commit IDs are references, never embedded diffs.** Work Objects store commit SHAs as pointers to Git. Diffs, file contents, and code history remain in Git, retrievable via `git show <sha>` or `git diff <sha>..<sha>`.

2. **Target SHA: merge commit on `main`.** In the current direct-to-main workflow, the implementation commit IS the merge commit — they are the same SHA. If a PR workflow with squash-merge is adopted, the merge SHA differs from the implementation branch SHA, and `deploy-with-recovery` (which already owns post-ship observation) is the natural owner for recording the merge SHA in a follow-up History entry.

3. **Conductor appends commit SHA to History entries at commit time.** The conductor skill already owns commits (`git_operations`) and writes History entries. Adding the commit SHA is a one-field extension of an existing write path. The SHA is appended at the time of commit; it is never retroactively added to past entries.

4. **`[system]` evidence entries carry an optional commit SHA.** Recorded when evidence depends on a specific code state (test results, file contents, command output against a known revision). Omitted for live observations (user confirms behavior, terminal output from investigation, grilling session findings). The distinction prevents noise — a SHA on a live observation adds no verifiability — while closing the gap for code-dependent evidence.

5. **`track-components` needs no new field.** The existing `last-grilled-SHA` combined with location-scoped drift checking (`git diff <sha> -- <location(s)>`) already anchors component code to grilling state. A separate `implementation-SHA` would duplicate information without improving precision.

### Deferred with revisit triggers

These data types remain Git-referenced (not embedded) with concrete revisit triggers:

| Data type | Revisit trigger |
|---|---|
| File lists | Concrete traceability failure in outcome review (can't determine which files a past decision touched) |
| Test output | Concrete traceability failure in outcome review (can't reproduce or verify past test results) |
| Branch names | PR workflow adoption |
| PR status | PR workflow adoption |
| Deployment identifiers | Deployment pipeline exists |

## Scope

This decision applies to:

- History entries written by the conductor after a commit
- `[system]` evidence ledger entries that cite code-dependent facts
- The component ledger's existing `last-grilled-SHA` field (unchanged; confirmed as sufficient)

This decision does not apply to:

- `[decision]`, `[inference]`, `[gap]`, `[testimony]`, or `[memory]` evidence entries (these are not code-state-dependent)
- Non-Work-Object structures
- The Personal Institution or PKM systems

## Rationale

**Reference beats embedding for regenerable data.** Git already stores every artifact this decision defers — diffs, file lists, authorship, test output, deployment state. Embedding them in Work Objects would duplicate Git's storage, risk staleness (the Work Object's copy drifts from Git's), and bloat Work Objects with content that `git show` can reproduce on demand. A commit SHA is 40 characters; a diff is unbounded.

**The commit SHA is the narrowest bidirectional link.** It is immutable (Git guarantees content-addressing), universally resolvable (`git show <sha>` works on any checkout), and cheap to store (40 characters). It creates a one-hop path in both directions: from Work Object to code (`git show <sha>`) and from code to Work Object (search Work Objects for the SHA). No other identifier has all three properties.

**The system already has precedent.** `track-components` stores `last-grilled-SHA` and uses Git drift as a reopen trigger. Extending SHA storage to History and evidence entries follows the same pattern — a repo-level anchor combined with path-scoped inspection — rather than inventing a new mechanism.

**Optional SHA on evidence entries balances verifiability and noise.** A grilling session's `[system]` entry ("the user confirmed the fixture passes") doesn't benefit from a SHA — the evidence is the user's confirmation, not the code state. An implementation session's `[system]` entry ("test_validate.py: 240 passed") does benefit — six months later, you can `git show <sha>` and run the same test against the same code. Making the SHA optional preserves both use cases without forcing ceremony on live observations.

**The conductor is the natural recording point.** The conductor already owns commits, writes History, and consolidates specialist evidence. Adding a SHA field to its existing write path is a one-line extension. No new skill, workflow step, or authority boundary is required.

## Alternatives Considered

### Embed full diffs, file lists, and test output in Work Objects

Store everything. Work Objects become self-contained records with zero external dependencies.

Rejected because: this duplicates Git's storage, creates staleness risk (the Work Object's copy of a diff is not the canonical diff), and makes Work Objects unwieldy. The append-only rule means an embedded diff can never be corrected if it was recorded incorrectly — Git's history, by contrast, can be inspected afresh at any time.

### Commit-message trailers as the primary link (`Work-Object: 2026-07-15-001`)

Put the Work Object ID in the commit message. Work Objects optionally back-reference commits. The link is discoverable from either side.

Rejected as the primary mechanism because: it places the recording burden on the commit author (who may not be the conductor), it requires a convention that all committers must follow, and it doesn't help when you start from the Work Object and want to find the code. It is not rejected as a complementary practice — commit-message trailers and Work Object SHA references are compatible and could coexist.

### Store the implementation branch SHA, not the merge SHA

Record the commit SHA at the moment of implementation, on whatever branch it happens. Accept that this SHA may not survive a squash-merge or rebase.

Rejected because: the value of a Work Object is in post-hoc traceability — "what shipped and why?" — not in implementation-moment snapshots. A branch SHA that no longer exists in any ref provides a broken link. The merge SHA on `main` is durable as long as the repository exists.

### Mandatory SHA on all `[system]` evidence entries

Every `[system]` entry must carry a commit SHA, even live observations.

Rejected because: it forces ceremony on entries that don't benefit from it. A grilling session's observation that "the user confirmed the current hypothesis" gains nothing from a SHA — the code state is irrelevant to the confirmation. Mandatory fields that are routinely filled with meaningless values train readers to ignore them, weakening the field's signal for the entries where it matters.

## Consequences

**Positive:**
- Bidirectional traceability between workflow reasoning and code artifacts for the first time
- Evidence verifiability — code-dependent claims can be reproduced by checking out the recorded SHA
- Consistent contract: one rule ("reference, don't embed") governs all Git data types
- No new write paths, skills, or authority boundaries — the conductor's existing History write gains one field

**Negative:**
- Commit SHA recording is only as reliable as the conductor's commit behavior — if the conductor fails to record the SHA, the link is silently absent
- The evidence ledger table format (`Tag | Source | Entry`) has no column for an optional SHA — format change may impact the parser in `tools/ws/sections.py` and `validate.py`
- PR workflow adoption would require `deploy-with-recovery` to record merge SHAs — this path is designed but untested
- No existing Work Object has ever recorded a commit SHA — adoption is greenfield with no migration path for past objects

**Neutral:**
- `track-components` schema is unchanged — the existing `last-grilled-SHA` field is confirmed as sufficient
- File lists, test output, branch names, PR status, and deployment identifiers remain Git-referenced with explicit revisit triggers
