# Shared Protocols and Constitution — Component Plan

Grilling Session 6 output. Scope: the seven shared protocols (Evidence Model,
Consequence-Authority, Agreement Loop, Skill-Aware Grilling, Capability
Degradation, Shared Protocol, Workspace Documentation Contract) and whether
Work Studio needs a short, always-loaded constitution.

## 1. Current-state findings (file paths)

- `tools/generate-adapters.py:37-44` (`SHARED_REFERENCES`) copies all seven
  protocol files unconditionally into every generated skill's `references/`
  directory, via `build_reference_entries()` (`tools/generate-adapters.py:463-479`),
  regardless of whether that skill's `SKILL.md` body ever mentions the file.
- Checksums confirm the copies are byte-identical (1 distinct sha256 per file
  across the repo). This is mechanical, deterministic duplication, not
  hand-copied drift.
- Actual per-skill reference footprints (grep on `skills/core/*/SKILL.md`)
  are partial, not universal:
  - Agreement Loop: 14/14 skills
  - Skill-Aware Grilling: 14/14 skills
  - Consequence-Authority: 12/14
  - Capability Degradation: 11/14
  - Evidence Model: 9/14
  - Shared Protocol: 3/14 (`conduct-work-object`, `investigate-live-question`,
    `pressure-test-decision`)
  - Workspace Documentation Contract: 2/14 (`conduct-work-object`,
    `track-components`)
- `Shared Protocol` self-declares as a cross-*package* contract (Personal
  Institution ↔ Work Studio), not an intra-repo protocol
  (`references/SHARED-PROTOCOL.md:1-8`). It is the only one of the seven with
  a version field (`Protocol version: 0.1`), and ADR-0005 explains why:
  versioning exists specifically because the two sides are independently
  installable packages. The other six never cross an installation boundary,
  so file-level version fields were never applicable to them.
- No skill declares its protocol dependencies structurally. There is no
  `requires:`/`protocols:` frontmatter field on any `skills/core/*/SKILL.md`
  — only `name` and `description`.
- `build_reference_entries()`'s docstring claims *"Include every shared
  reference declared by the generated core skills"* — but the implementation
  never reads a declaration; it loops the fixed global list for every skill.
  The claim and the code disagree.
- `tools/verify-conformance.py` has no check that asserts a generated skill
  carries all seven reference files — the "Verify shared references exist"
  check (`tools/verify-conformance.py:~371`) only asserts the **canonical**
  `references/*.md` files exist, and only checks 5 of the 7 names
  (`WORK-OBJECT`, `AGREEMENT-LOOP`, `EVIDENCE-MODEL`, `CONSEQUENCE-AUTHORITY`,
  `CAPABILITY-DEGRADATION` — omitting `SHARED-PROTOCOL` and
  `SKILL-AWARE-GRILLING`, and including `WORK-OBJECT`, which is outside this
  session's seven-protocol scope).
- All executable checks in the repo (`tests/test_shared_protocol.py`,
  `tools/verify-conformance.py`) verify file presence, checksums, and
  required section headings/keyword strings — never runtime behavioral
  compliance. Rules like "no adapter may claim verification succeeded when
  the required capability was unavailable" (`CAPABILITY-DEGRADATION.md:4-6`)
  are enforced only by the model reading and following the prompt text in
  that turn.
- `conduct-work-object/SKILL.md:195-224` inlines its own restatement of the
  Work Object schema (`references/WORK-OBJECT.md:7-20`), explicitly "so the
  installed skill remains self-contained." The two copies are semantically
  identical but not byte-identical (different placeholder bracket
  conventions) — a real precedent for deliberate, non-verbatim restatement
  of shared content elsewhere in this repo.
- ADR-0013 states adapter generation copies Workspace Documentation Contract
  "so installed skills use the same rules" — a stated intent of universal
  distribution that conflicts with its actual 2/14 reference footprint.

## 2. Contradictions and risks

- **Docstring vs. implementation**: `build_reference_entries()` claims
  declared, selective inclusion; the code does unconditional, global
  inclusion. (Confirmed contradiction.)
- **ADR-0013 vs. proposed conditional copying**: the ADR's stated purpose
  (stop skills from inventing content or discovering artifacts
  inconsistently) is meant to apply to any installed skill, not just the 2
  that reference the file by name. Naively gating this file the same way as
  the other five would silently narrow behavior the ADR intended to be
  universal. Resolved in this plan by extracting a constitution-tier
  invariant sentence (see §3) rather than moving the whole file to the
  always-copied tier.
- **Verbatim vs. restated duplication**: the Work Object schema precedent
  shows this repo already tolerates deliberate, non-byte-identical
  restatement of shared content for self-containment. Constitution sentences
  are explicitly carved out as an exception to that precedent (must stay
  verbatim) because they are normative prose, not structural schema — risk
  is future contributors "helpfully" paraphrasing a constitution sentence
  the way the Work Object schema was paraphrased, silently breaking
  line-checksum pinning.
- **Conformance-check gaps**: `verify-conformance.py`'s existence check
  omits 2 of the 7 protocols and includes one file outside scope
  (`WORK-OBJECT`). Low severity, but signals protocol bookkeeping has been
  ad hoc rather than deliberately governed.
- **No enforcement substrate for sentence-level sync**: `EVIDENCE-MODEL.md`
  and `CAPABILITY-DEGRADATION.md` — source files for 2 of the 4 constitution
  invariants — have no version marker at all, so file-version pinning
  wasn't viable; the plan uses line-checksum pinning instead, which is new
  infrastructure (does not exist today).

## 3. Accepted decisions

1. The uniform, unconditional whole-list copy in `SHARED_REFERENCES` is an
   oversight, not an intentional design choice.
2. The constitution is built by extracting individual invariant *sentences*
   from source protocols, not by promoting whole files, and not gated by a
   "referenced by all 14 skills" bar (that bar wrongly admits Skill-Aware
   Grilling's catalogue content and wrongly excludes Evidence Model, whose
   principle is relied on without a filename reference).
3. Constitution membership requires direct textual grounding — an existing,
   locatable sentence in the corpus — not synthesis or invention. Of 8
   illustrative candidates, only 4 clear this bar:
   - "preserve provenance" (`EVIDENCE-MODEL.md:18`)
   - "never launder inference" (`EVIDENCE-MODEL.md:22`, exact match)
   - "never claim unavailable capability" (`CAPABILITY-DEGRADATION.md:4-6`)
   - "missing artifact is a gap, not permission to invent"
     (`WORKSPACE-DOCUMENTATION-CONTRACT.md:4-6`, near-verbatim)
4. Constitution entries are pinned by source-line checksum, not file-version
   comparison — 2 of the 4 source files have no version field, and ADR-0005
   confirms versioning was only ever meant for the cross-package boundary
   (Shared Protocol), not intra-repo protocols.
5. Constitution entries must be copied byte-for-byte verbatim everywhere,
   explicitly overriding the Work Object schema's self-contained-restatement
   precedent for this content type — normative prose carries its meaning in
   exact wording; structural schema fields do not.
6. `SHARED_REFERENCES` splits into two tiers: one always-copied file (the
   constitution) and six conditionally-copied protocol files (Agreement
   Loop, Skill-Aware Grilling, Consequence-Authority, Capability Degradation,
   Evidence Model remainder, Shared Protocol, Workspace Documentation
   Contract — full document), copied only when a skill declares them.
7. Per-skill protocol dependency becomes an explicit, human-authored
   `protocols:` frontmatter field on each `skills/core/*/SKILL.md`,
   replacing grep-based text-search inference (which both under- and
   over-includes).
8. Workspace Documentation Contract's full registry document stays
   conditionally-copied (only `conduct-work-object`, `track-components`
   declare it); ADR-0013's actual concern is satisfied instead by adding its
   invariant sentence to the constitution (decision 3, 4th bullet). ADR-0013
   needs a follow-up ADR recording this narrowing.

## 4. Target component boundary

- **New**: `references/CONSTITUTION.md` — canonical source for the 4
  invariant sentences, each tagged with its source file, source line, and a
  pinned checksum of that source line.
- **Changed**: `tools/generate-adapters.py` — `SHARED_REFERENCES` becomes two
  lists (`ALWAYS_REFERENCES = ["CONSTITUTION.md"]`,
  `CONDITIONAL_REFERENCES = [...6 files]`); `build_reference_entries()` reads
  each skill's declared `protocols:` frontmatter to decide which conditional
  files to copy, and always copies the constitution.
- **Changed**: every `skills/core/*/SKILL.md` — add `protocols:` frontmatter
  field listing the conditional protocols that skill actually depends on.
- **New**: `tools/verify-constitution-sync.py` (or an extension of
  `verify-conformance.py`) — checks each constitution entry's pinned
  checksum against the live source line in its origin file; fails loudly on
  drift.
- **Changed**: `tools/verify-conformance.py`'s existence check — include all
  7 protocol names (add `SHARED-PROTOCOL`, `SKILL-AWARE-GRILLING`), and
  either justify or drop the `WORK-OBJECT` entry given it's outside this
  session's declared scope.

## 5. Recommended architecture

Three tiers, replacing the current flat "seven files, copied to everyone":

1. **Constitution** (always-loaded, verbatim, line-checksum pinned) — short
   invariant sentences only. Nothing else qualifies for this tier regardless
   of how important its source protocol feels; the bar is textual grounding
   plus universality, not consequence or size.
2. **Selectively loaded protocols** (conditional, declared via frontmatter,
   copied whole) — the six remaining protocol files, each pulled in only by
   the skills that declare a dependency on them.
3. **Executable validators** (deterministic checks, no model compliance
   required) — the new constitution line-checksum check, plus the existing
   structural/checksum checks in `verify-conformance.py`, extended to cover
   all 7 protocol names.

Rules that are "normative but unenforced" (e.g., Consequence-Authority's gate
table, most of Capability Degradation's runtime behavior) remain
prompt-text-only in this plan — building executable enforcement for those is
explicitly out of scope here and listed under Deferred Decisions.

## 6. Migration steps

1. Author `references/CONSTITUTION.md` with the 4 grounded invariant
   sentences, each recording source file, source line number, and a sha256
   of that exact line.
2. Add `protocols:` frontmatter to each of the 14 `skills/core/*/SKILL.md`
   files, based on their actual current reference footprint (§1) as a
   starting point, reviewed by a human rather than auto-derived by grep.
3. Split `SHARED_REFERENCES` in `tools/generate-adapters.py` into
   `ALWAYS_REFERENCES` and `CONDITIONAL_REFERENCES`; update
   `build_reference_entries()` to read each skill's `protocols:` field.
4. Add the constitution line-checksum verifier; wire it into
   `tools/verify-conformance.py --all` (or a new `--constitution` flag).
5. Extend the "Verify shared references exist" check to all 7 protocol
   names; resolve the `WORK-OBJECT` scope question (drop it from this check
   or open a follow-up session to formally bring it into protocol scope).
6. Regenerate all adapters (`python3 tools/generate-adapters.py`) and diff
   the output — expect most skills to shrink their `references/` directory
   from 7 files to the constitution plus whatever they declared.
7. Open a follow-up ADR superseding ADR-0013's "copies the contract so
   installed skills use the same rules" language, recording that the *rule*
   is now universal via the constitution while the *document* is
   conditional.

## 7. Tests and evidence required

- `tools/verify-conformance.py --check` must pass post-migration with zero
  regressions.
- New test: for each of the 4 constitution entries, assert the pinned
  checksum matches the live source line — must fail deliberately once
  (mutate a source line in a scratch copy) to prove the check actually
  detects drift, not just that it runs.
- New test: for each skill, assert every file in its generated
  `references/` directory is either the constitution or named in that
  skill's `protocols:` frontmatter — no orphaned copies.
- Manual verification: regenerate adapters, confirm byte-identical
  constitution text across all skills that carry it, confirm conditional
  files are absent where not declared.
- Re-run `tests/test_shared_protocol.py` unchanged — it tests the
  cross-package installed-adapter checksum path, which this plan doesn't
  touch.

## 8. Deferred decisions

- Disposition of the 5 candidate invariants that didn't clear the grounding
  bar this session: "proportion authority to consequence" (grounded
  structurally in a table, not a sentence — would require someone to author
  new prose, which risks laundering inference into fact if done casually),
  "prefer reversible changes" (diffuse, no single source sentence), "separate
  recommendation from authorization" (diffuse), "use deterministic tools for
  mutation" (no grounding found at all — possibly pure invention), and
  "preserve append-only history" (grounded, but only in `WORK-OBJECT.md`,
  which is outside this session's declared seven-protocol scope).
- Whether `WORK-OBJECT.md` should be formally brought into protocol-review
  scope as an eighth document — it's already checked for existence in
  `verify-conformance.py` and hand-duplicated into `conduct-work-object`,
  despite never being named in this session's brief and never being
  distributed by the generator.
- Building actual runtime enforcement for the "normative but unenforced"
  rules identified in §1 (Consequence-Authority's gates, most of Capability
  Degradation) — this plan only adds enforcement for the 4 constitution
  sentences, not the full rule surface of all seven protocols.
- The minor `verify-conformance.py` existence-check gap (missing 2 names,
  includes an out-of-scope one) is noted as a cleanup item bundled into
  migration step 5, not a separately negotiated decision.

## 9. Smallest tracer bullet

Prove the riskiest new mechanism — line-checksum pinning — on exactly one
invariant before building the rest:

1. Create `references/CONSTITUTION.md` with a single entry: "never launder
   inference as source evidence," sourced from `EVIDENCE-MODEL.md:22`,
   pinned checksum included.
2. Add a ~30-line standalone script that reads that one entry, re-reads line
   22 of `EVIDENCE-MODEL.md`, hashes it, and compares.
3. Run it green. Then hand-edit `EVIDENCE-MODEL.md:22`'s wording and re-run —
   confirm it fails loudly.
4. Only after that round-trip is proven, extend to the other 3 invariants,
   the frontmatter field, and the generator split.

This isolates the one genuinely new piece of infrastructure (sentence-level
drift detection) from the larger, more mechanical refactor (splitting
`SHARED_REFERENCES`, adding frontmatter), so a failure in the new mechanism
is caught before 14 skills' worth of generation logic depends on it.
