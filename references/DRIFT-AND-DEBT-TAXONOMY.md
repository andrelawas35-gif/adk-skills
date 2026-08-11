# Drift and Debt Taxonomy

Sixteen classes of misalignment that can accumulate in the studio's records,
code, and contracts. Each class names a specific failure shape, gives a
definition, a grounded example from the current tree, and the correct
response pattern.

**Drift** (classes 1–6): something changed and something else didn't follow.
The correct response is reconciliation — bring them back into agreement.

**Debt** (classes 7–16): something was never done. The correct response is a
decision about whether and when to pay it.

---

## Drift classes

### 1. Contradiction

Two simultaneously applicable records make materially incompatible claims.

| Field | Value |
|-------|-------|
| **Example** | ADR 0018 removes numeric attention caps; `check_attention_limits` (`validate.py:1067-1085`) still enforces max 1 Primary, 2 Supporting, 3 total. |
| **Correct response** | Preserve both sources, open or attach a conflict, identify owner and precedence, obtain disposition. |

### 2. Contract drift

Implementation and its declared normative contract no longer match.

| Field | Value |
|-------|-------|
| **Example** | `next_action` and `revisit_trigger` are absent from generator and validator. `private` is valid in `schema.py:15` but rejected by `ws create` (`__main__.py:771`). The CLI-only write rule conflicts with direct-edit instructions in skill contracts. |
| **Correct response** | Repair implementation or supersede prose through an explicit decision; add regression test. |

### 3. Generated drift

Deterministic output differs from canonical input.

| Field | Value |
|-------|-------|
| **Example** | Adapter generator (`tools/generate-adapters.py`) detects this class; inspected tree passed at time of recording. |
| **Correct response** | Regenerate only after source validation; fail CI on mismatch. |

### 4. Reference drift

A locator no longer resolves to the identity it claimed.

| Field | Value |
|-------|-------|
| **Example** | Evidence-freshness warnings from `2026-08-10-010`; some use ambiguous roots such as `AGREEMENT-LOOP.md` without a path prefix. |
| **Correct response** | Surface for re-read; improve canonical root resolution; never mark claim false automatically. |

### 5. Dependency drift

A source or contract changed but declared dependents were not reopened.

| Field | Value |
|-------|-------|
| **Example** | `COMP-001` behind HEAD; correction fan-out (`2026-08-10-011`) only reaches named dependents. |
| **Correct response** | Derive candidate affected edges, mark coverage, require human re-review for material cases. |

### 6. State/register drift

A projection disagrees with canonical object state.

| Field | Value |
|-------|-------|
| **Example** | Active objects absent from `active.md`; duplicate entries also present. |
| **Correct response** | Rebuild or reconcile projection through the conductor; do not make the projection canonical. |

---

## Debt classes

### 7. Lifecycle debt

Work remains in a state or status with no valid next or return edge.

| Field | Value |
|-------|-------|
| **Example** | Open objects without `next_action`; waiting/paused objects without `revisit_trigger`. |
| **Correct response** | Require closure metadata at transition time; report orphaned nodes. |

### 8. Outcome debt

Action or decision reached observe or close without recorded evaluation.

| Field | Value |
|-------|-------|
| **Example** | Objects reported by `check_outcome_review` (`validate.py:2073+`). |
| **Correct response** | Schedule bounded review; distinguish unavailable observation from skipped review. |

### 9. Epistemic debt

Consequential claim lacks adequate attributable support, counterevidence
review, scope, or freshness.

| Field | Value |
|-------|-------|
| **Example** | Claims below current support-adequacy heuristic in `epistemic_controls.py`; unresolved legacy tag debt. |
| **Correct response** | Show exact missing support; avoid composite score; strengthen or scope claim. |

### 10. Authority debt

An action's permission, scope, expiry, or execution mediation is absent or
ambiguous.

| Field | Value |
|-------|-------|
| **Example** | Read-only grants exist (`validate.py:878`); external-effect tools are not mediated. |
| **Correct response** | Deny or ask on ambiguity where runtime wrapper exists; otherwise disclose auditable-only status. |

### 11. Component debt

A durable capability has stale pointers, unresolved findings, or dependency
changes since last review.

| Field | Value |
|-------|-------|
| **Example** | Ledger check reports component staleness against HEAD. |
| **Correct response** | Re-grill selected component; do not auto-create work. |

### 12. Governance activation debt

A useful governance path has no evidence it is encountered or used.

| Field | Value |
|-------|-------|
| **Example** | Memory candidate, grilling nomination, method promotion, and revisit pathways have weak or zero fire data. |
| **Correct response** | Instrument encounter states prospectively before redesign. |

### 13. Constraint debt

A required boundary is unaddressable, unvalidated, silently relaxed, or
lacks expiry or revisit behavior.

| Field | Value |
|-------|-------|
| **Example** | Constraints are narrative only; accepted-deviation schema is deferred (`2026-08-10-009`, `design/waiting`). |
| **Correct response** | Promote only consequential constraints; record deviations explicitly after real need appears. |

### 14. Verification debt

A check passes without testing the claimed property or is vacuous.

| Field | Value |
|-------|-------|
| **Example** | A verification path that passes while its parser yields no entries. |
| **Correct response** | Mutation-test the verifier; require proof that a deliberately broken fixture fails. |

### 15. Research/proposal debt

A proposed architecture is spoken of as shipped or has no disposition.

| Field | Value |
|-------|-------|
| **Example** | Epistemic and constraint research Work Objects contain unimplemented schemas and services. |
| **Correct response** | Label status; map each proposal to repair, build, test, defer, or reject. |

---

## Classification notes

- **Dependency drift vs. component debt**: dependency drift is about any
  source/dependent pair; component debt is specifically about ledger-tracked
  durable capabilities. They can share an instance but differ in scope and
  response.

- **Contract drift can produce contradictions** when two contracts disagree
  about the same action (e.g., the CLI-only write rule vs. direct-edit
  instructions). The distinguishing test: if one source is implementation and
  the other is its declared spec, it's contract drift. If both are normative
  and simultaneously applicable, it's a contradiction.

- **Governance activation debt vs. verification debt**: governance activation
  debt means the check is never encountered (no evidence it runs).
  Verification debt means it runs but is vacuous (passes without testing the
  claimed property).
