# Andrelawas Work Studio

Andrelawas Work Studio is the execution and continuity system for bounded work. It receives user-approved, minimum-necessary context from adjacent systems without absorbing their private records.

## Language

**Personal Institution**:
The separate personal evidence and reflection system that preserves lived observations, recurring questions, and personal interpretation.
_Avoid_: personal-memory store, Work Studio archive

**Local-first**:
An ownership model in which Personal Institution records are stored on the user's own machine by default; sync and sharing require explicit later choices.
_Avoid_: cloud-first, automatic sync

**Observation**:
A short, firsthand record of something the user noticed, experienced, or thought, preserved in the user's own words before later interpretation.
_Avoid_: fact, conclusion, AI summary

**Observation revision**:
A user-authored correction or update to an Observation that preserves the original text and records the change as later history.
_Avoid_: overwrite, silent edit

**Question**:
An open inquiry the user wants to explore. A Question may exist without a Project and may inform one or more Projects.
_Avoid_: task, commitment

**Project**:
A bounded effort to create, change, or test something. A Project may contain multiple Questions.
_Avoid_: curiosity, ongoing theme

**Source**:
The provenance of an Observation. An Observation defaults to the self source; an external source may be attached when it prompted or supports the record.
_Avoid_: truth rating, fact checker

**Shared protocol**:
A small, versioned specification of the terms and handoff rules shared by separately installable Personal Institution and Work Studio packages.
_Avoid_: shared mega-skill, duplicated instructions

**Work Studio**:
The execution, decision, and delivery system whose canonical record is a Work Object.
_Avoid_: personal archive, life operating system

**Workspace Documentation Contract**:
The sole durable artifact created when an empty workspace is bootstrapped, at
`WORKSPACE-DOCUMENTATION-CONTRACT.md`. It defines how project documents are
discovered, named, owned, created, validated, and superseded before the
workspace records project-specific claims, and contains the canonical artifact
registry. An explicit bootstrap request grants authority to create this contract
only. It is a human-readable Markdown file with a rigid, parseable registry
section.
_Avoid_: project brief, empty documentation tree, implied repository convention

**Canonical Artifact Registry**:
The complete taxonomy declared in the Workspace Documentation Contract. It
names each supported artifact type and its lifecycle rules even when the
artifact's file has not been created. It includes generated adapters with their
canonical source and deterministic generation boundary. Every entry declares
its canonical name and location, purpose, owner, stage trigger, required
evidence, creation and update authority, provenance and freshness rule,
supersession rule, generated/canonical status, and validation method.
Each artifact type has exactly one canonical location; non-canonical copies
must declare their relationship to it. Its initial classes are domain context,
Work Objects, ADRs, plans/designs, Evidence Ledgers, runbooks, Verification
Records, outcome reviews, and generated adapters. Its parseable YAML structure
has a mandatory schema version and declares exact canonical locations for its
own workspace.
_Avoid_: generated document tree, evidence inventory, guessed path convention

**Missing Artifact Gap**:
The explicit state in which a registry-required artifact is absent from its
canonical location. A skill must inspect, report the gap, recommend the minimum
justified creation, and obtain scoped authority; it must not invent retrieval
or contents.
_Avoid_: implicit blank template, assumed project fact, silent file creation

**Artifact Conflict**:
A material disagreement between registered artifacts or revisions. A skill
compares declared ownership, provenance, freshness, and canonical status, then
surfaces the conflict for an accountable decision rather than silently
reconciling it.
_Avoid_: averaged conclusion, newest-file-wins, silent overwrite

**Artifact Supersession**:
The explicit relationship in which a current artifact identifies the exact
predecessor it replaces and why. The predecessor remains readable but
non-current.
_Avoid_: destructive replacement, implicit deprecation, erased rationale

**Documentation Contract Validation**:
Behavioral verification of the registry against empty, docs-only, and
code-without-docs workspaces, plus missing-reference, conflicting-record,
stale-record, and partially-generated-adapter scenarios. Each scenario proves
source discovery, no-hallucination behavior, and minimum-authority creation.
_Avoid_: prose-only review, happy-path check, template existence test

**Documentation Contract Custodian**:
`conduct-work-object`, the sole skill authorized to discover, bootstrap,
persist, or reconcile revisions to the Workspace Documentation Contract.
Specialist skills may inspect it and recommend a mutation but may not perform
one themselves. Direct specialist invocation routes to this custodian when the
contract is absent or conflicted, then resumes with inherited evidence.
_Avoid_: specialist-owned bootstrap, shared silent writer, direct contract edit

**Artifact Stage Trigger**:
The registered condition permitting an artifact to be created. It must be an
explicit user intent, accepted decision, or registered evidence; agent-inferred
project stage may recommend creation but cannot activate it.
_Avoid_: guessed lifecycle state, convenient template creation, implied authority

**Registry Architecture Change**:
A change to the Canonical Artifact Registry's taxonomy or schema. It requires
an ADR and explicit owner approval; ordinary evidence updates do not.
_Avoid_: routine documentation edit, silent schema migration, adapter-only change

**Artifact Freshness Rule**:
The type-specific review trigger declared for a registered artifact. It reflects
the artifact's own lifecycle rather than a universal documentation expiry
period.
_Avoid_: global TTL, newest-file assumption, permanent-current status

**Claim Provenance**:
The declared basis for a consequential artifact claim: observed system evidence,
an accountable decision, attributable testimony, inference, or an explicit gap.
A claim without provenance is not established project fact.
_Avoid_: undocumented assertion, inferred certainty, anonymous source

**Scoped Mutation Record**:
The pre-execution record for a proposed artifact mutation. It names exact
affected files, the authority source, any external effect, and the verification
boundary.
_Avoid_: blanket approval, unspecified write set, unverified documentation edit

**Legacy Documentation Migration**:
A separately authorized change that maps inspected pre-contract documents to
registered canonical artifacts. Bootstrap never moves, renames, or imports
legacy documents automatically.
_Avoid_: silent reorganization, automatic import, implied canonicalization

**Generated Adapter Artifact**:
A deterministic, non-canonical copy derived from a registered source artifact
for a target platform. It may be overwritten only by deterministic regeneration
after source validation and drift checking, but is never directly edited as the
authoritative source. Its cleanup requires separately scoped authority.
_Avoid_: canonical skill, hand-maintained fork, source of record

**Evidence Bridge**:
A user-approved, redacted summary or stable reference that carries only the minimum personal context needed into a Work Object.
_Avoid_: memory sync, archive export

**Personalization Contract**:
A versioned, user-approved set of working tendencies with scope, supporting and contrary evidence, confidence, and a review trigger. It guides a skill only when relevant and never establishes a fixed identity.
_Avoid_: user profile, permanent preference, inferred identity

**Working-method entry**:
A testable, revisable Personalization Contract entry that describes a preferred way of working.
_Avoid_: personality trait, permanent value

**Active-lens entry**:
A narrowly scoped, time-bound Personalization Contract entry for a live question or interpretive interest.
_Avoid_: identity claim, default theme

**Hard-boundary entry**:
An explicit Personalization Contract entry governing privacy, consent, safety, or authority; it changes only through deliberate review.
_Avoid_: preference, convenience rule

**Inactive contract entry**:
A Working-method or Active-lens entry whose review trigger passed without renewal; it remains as historical evidence but no longer guides skills.
_Avoid_: deleted preference, active default

**Work Object**:
The durable record of one activated inquiry, project, change, or incident in Work Studio.
_Avoid_: chat, personal note, task

**Grilling Session**:
A continuous, recommendation-led, one-question-at-a-time conversation that may
move across specialist skills without resetting its context or accepted
decisions.
_Avoid_: isolated skill interview, command sequence, output template

**Context Card**:
The visible, correctable opening or resume summary of goal, project stage,
approved preferences, inspected evidence, open branches, and active specialist.
_Avoid_: hidden personalization, full chat replay, unverified memory dump

**Decision Frontier**:
The single unresolved branch currently most likely to change the recommendation,
ranked by probability, impact, uncertainty, irreversibility, and dependency
reach.
_Avoid_: next checklist item, arbitrary question, unranked menu

**Evidence Ledger**:
The canonical Work Object record of attributable system evidence, decisions,
testimony, inference, conflicts, and gaps used by a Grilling Session.
_Avoid_: hidden reasoning, uncited code claim, averaged contradiction

**Skill Grilling Profile**:
The stage-specific policy defining what a specialist inspects, which tension it
pursues, how it challenges an answer, where it routes, and when its stage has
enough understanding.
_Avoid_: coverage checklist, duplicated conversational engine, generic interview

**Coverage Proof**:
The convergence record showing that material branches are resolved, routed,
deferred with triggers, or ruled out by evidence, and that no remaining question
is likely to change the recommendation.
_Avoid_: question count, completion assertion, exhaustive transcript

**Accepted answer**:
A Grilling Session answer that the user has confirmed and the agent has
checkpointed in the Work Object (Grilling section and Evidence Ledger). It does
not create a registered artifact on its own; it materializes into one only when
that artifact's declared stage trigger fires.
_Avoid_: registered decision, provisional answer, unrecorded agreement

**Registered decision**:
A decision recorded in a Work Object's Decisions section with full structure
(branch chosen, alternatives, rationale, trade-offs, confidence, revisit
trigger, edge cases, actor). It may originate from an Accepted answer that meets
the consequence threshold, or from any decision the user explicitly requests be
formally registered.
_Avoid_: accepted answer, ad-hoc choice, implicit default

**Personal-memory record**:
A private record maintained by Personal Institution; it remains outside a Work Object unless the user explicitly approves an Evidence Bridge.
_Avoid_: Work Object evidence, synced note
