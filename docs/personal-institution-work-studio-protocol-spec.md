# Personal Institution ↔ Work Studio Shared Protocol

## Problem Statement

The user needs Personal Institution to make Work Studio more grounded in lived
evidence without turning Work Studio into a copy of a private archive or letting
Codex chat history create a stale, opaque identity profile. The two packages
currently have compatible aims but no released, enforceable handoff contract.
Their instructions can therefore drift: private material might be copied into a
Work Object, an inference might be presented as evidence, or a temporary
interest might become a default lens for unrelated work.

## Solution

Create Shared Protocol v0.1: a small, versioned contract used by separately
installable Personal Institution and Work Studio packages. It defines an
Evidence Bridge for minimum-necessary, user-approved context; a
Personalization Contract for revisable, evidence-backed guidance; protocol
version compatibility; and a single behavioral fixture that validates the
cross-package boundary. Personal Institution owns private records and contract
candidates. Work Studio consumes only approved, relevant bridge and contract
material and never scans or mutates the personal archive.

## User Stories

1. As the user, I want Personal Institution to retain my private observations separately from Work Studio, so that project continuity does not become a duplicate personal archive.
2. As the user, I want to approve the context that crosses from personal reflection into a Work Object, so that I control privacy and relevance.
3. As the user, I want an Evidence Bridge to contain the minimum necessary summary or stable reference, so that a project is grounded without oversharing.
4. As the user, I want each bridge claim to retain provenance and sensitivity, so that I can distinguish lived evidence from source, system, and inferred material.
5. As the user, I want Work Studio to function without access to personal memory, so that the packages can be installed, updated, and trusted independently.
6. As the user, I want current chat context to help the immediate conversation without silently changing persistent personalization, so that Codex memory remains under my authority.
7. As the user, I want to capture a chat statement deliberately when it should become durable evidence, so that important context is not lost.
8. As the user, I want Personalization Contract candidates to cite dated supporting and contrary records, so that personalization is inspectable rather than flattering narrative.
9. As the user, I want to confirm a candidate before it guides skills, so that an agent never infers a permanent preference or identity claim from one statement.
10. As the user, I want working-method entries to remain provisional and testable, so that a workflow preference can be revised when outcomes disagree.
11. As the user, I want active-lens entries to be narrow and time-bound, so that a current interest does not decorate unrelated technical or personal work.
12. As the user, I want hard-boundary entries to govern privacy, consent, safety, and authority until I explicitly revise them, so that important protections do not expire through inattention.
13. As the user, I want expired working-method and active-lens entries to become inactive rather than disappear, so that the system remembers context without continuing to apply it.
14. As the user, I want inactive entries to be visibly marked as historical context, so that a skill cannot present them as current guidance.
15. As a Work Studio skill, I want a single protocol version declaration, so that I can determine whether a handoff is supported before using it.
16. As a Work Studio skill, I want incompatible protocol versions to degrade to a manual, user-approved summary, so that version mismatch never results in direct archive access or silent data translation.
17. As a Personal Institution skill, I want to propose but not activate contract changes, so that the user remains the authority for personalization.
18. As an editor using Anti-Homogenization Editor, I want missing personal evidence to remain an explicit gap, so that no invented anecdote, emotion, or “voice” enters a revision.
19. As a maintainer, I want one high-level behavioral fixture for the handoff, so that contract changes are evaluated through observable outcomes rather than duplicated prompt wording.
20. As a maintainer, I want the fixture to cover privacy-by-default, approval, provenance, chat-memory boundaries, relevance, expiry, and version mismatch, so that the important integration failures regress visibly.
21. As a package maintainer, I want protocol evolution to be versioned independently from either skill package, so that compatibility decisions are deliberate and reviewable.
22. As a future agent, I want the shared vocabulary to be defined in the domain glossary and ADRs, so that terms such as Evidence Bridge and Active-lens entry are not reinterpreted in implementation.

## Implementation Decisions

- Introduce Shared Protocol v0.1 as a small, versioned specification, not a shared mega-skill. It defines terms, ownership, minimum fields, compatibility, and safe fallback behavior.
- Keep Personal Institution and Work Studio separately installable. Personal Institution owns personal-memory records, contract candidates, and the confirmation path; Work Studio owns Work Objects, execution decisions, and delivery records.
- Make an Evidence Bridge the only routine personal-to-work handoff. It requires explicit user approval and contains a minimum-necessary redacted summary or stable private reference, provenance, sensitivity, source attribution, and relevance to the receiving Work Object.
- Prohibit Work Studio from scanning, reading, or mutating the Personal Institution archive. Work Studio may receive only an approved bridge or contract entry supplied through the protocol.
- Represent persistent guidance as a Personalization Contract with three entry types: Working-method, Active-lens, and Hard-boundary.
- Require every contract entry to include its type, scope, supporting evidence, contrary evidence, confidence, approval state, and review trigger. Working-method and Active-lens entries also include active or inactive status.
- Restrict candidate creation to explicit, dated Personal Institution records. Current chat may be used in the present interaction but must be deliberately captured before it may support a persistent candidate.
- Require user confirmation before any candidate becomes active. No agent may infer or persist a personal preference, trait, identity, or value from chat or a single observation.
- Expire Working-method and Active-lens entries to inactive when their review trigger passes without renewal. Retain them as historical context. Keep Hard-boundary entries active until explicitly revised.
- Require skills to apply contract entries only when relevant to the current task and to default to neutral behavior when no current entry applies.
- Treat an incompatible protocol version as a capability degradation: report the mismatch, do not translate or access private data directly, and offer a manual user-approved summary.
- Preserve the existing Work Object provenance lanes. A bridge is recorded as lived evidence or inference according to its content; it is never relabeled as source or system evidence.
- Use the established domain glossary and ADRs as the source of terminology and architectural intent. The protocol implementation must preserve the decisions separating Personal Institution, Work Studio, evidence, personalization, and expiry.

## Testing Decisions

- Test only externally observable behavior: files or records created, explicit approval requests, provenance labels, visible status, and reported capability degradation. Do not test hidden reasoning or exact prompt text.
- Use one highest-level, cross-package behavioral fixture as the primary seam: the Personal Institution ↔ Work Studio handoff. This extends the repository's existing behavioral-fixture approach rather than adding component-specific prompt tests.
- The fixture must verify that private personal-memory content is neither read nor copied into a Work Object by default.
- The fixture must verify that an approved Evidence Bridge is minimal, attributed, sensitivity-aware, and represented in the correct provenance lane.
- The fixture must verify that chat does not silently create or update a Personalization Contract entry.
- The fixture must verify that a stale Active-lens entry is ignored for unrelated work.
- The fixture must verify that Anti-Homogenization Editor leaves unsupported personal specificity as a visible gap rather than inventing it.
- The fixture must verify that incompatible protocol versions produce explicit, safe degradation and a manual-summary fallback.
- A protocol or cross-package instruction change is not ready until the complete fixture passes. Existing Work Object behavioral fixtures are prior art for Given/When/Then structure, verification criteria, and authority-gate assertions.

## Out of Scope

- Migrating or exporting existing personal-memory records.
- Giving Work Studio direct archive access, including read-only filesystem discovery.
- Building a database, synchronization service, or background memory process.
- Inferring identity, psychological traits, values, or permanent preferences from chat history.
- Automatically publishing Evidence Bridges, Work Objects, or personal records to external systems.
- Adding new Personal Institution skills before the protocol and fixture establish a stable boundary.
- Implementing a full automated test runner beyond the established behavioral-fixture format.

## Further Notes

- The canonical definitions and approved decisions are recorded in the Work Studio domain glossary and ADRs 0001–0007.
- The initial fixture already documents the intended seam. The implementation should refine it only when a real behavior gap is found.
- Two follow-on experiments are intentionally deferred: a resistance log for recurring project friction, and a disconfirmed-self archive for expired or rejected personal hypotheses. Neither should become a contract feature without user-approved evidence and a bounded test.
