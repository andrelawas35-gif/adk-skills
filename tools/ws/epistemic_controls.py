"""Epistemic controls for Work Object lifecycle transitions.

Implements the async advisory model (Direction 3 from 2026-07-27-014):
transitions always succeed; after a transition, ``audit_epistemic_state()``
checks for expected epistemic evidence and appends ``[gap]`` entries for
missing evidence.

Consequence scaling (extended per 2026-07-27-015):
    - low: audit at verify transition only
    - meaningful: audit at build, verify, release
    - high: audit at every transition (build, verify, release, observe)

The 2026-07-27-015 model also introduced a "decision" audit branch, keyed to
a "decision" transition target. No such lifecycle state exists — `ws
transition --state` only ever accepts the eight real states — so that branch
was unreachable from its only call site. 2026-08-11-001 removed it and folded
its rationale check into the build-transition audit below, the one point in
the lifecycle where a decision is actually expected to already exist.
"""

import re
from typing import Dict, List, Optional, Tuple

from .sections import (
    VALID_EVIDENCE_TAGS,
    append_to_section,
    generate_evidence_entry,
    parse_decisions_table,
)


# ── Consequence audit map ─────────────────────────────────────────────────────
# Which target states are audited at each consequence level.

_CONSEQUENCE_AUDIT_MAP: Dict[str, Tuple[str, ...]] = {
    "low": ("verify",),
    "meaningful": ("build", "verify", "release"),
    "high": ("build", "verify", "release", "observe"),
}


def _has_evidence_gap(body: str) -> bool:
    """Check if the Evidence ledger contains any [gap] entries."""
    # Simple heuristic: look for | [gap] | in the evidence ledger section
    # We can't easily parse the markdown table, so a regex scan is sufficient.
    ledger_section = _get_section_body(body, "evidence ledger")
    if not ledger_section:
        return False
    return bool(re.search(r"\| \[gap\] \|", ledger_section))


def _get_section_body(body: str, section_name: str) -> Optional[str]:
    """Extract the body of a named section (without the heading) by scanning lines."""
    target = section_name.lower()
    lines = body.split("\n")
    in_section = False
    section_lines: List[str] = []
    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip().lower()
            if heading == target:
                in_section = True
                continue
            elif in_section:
                break
        elif in_section:
            section_lines.append(line)
    return "\n".join(section_lines).strip() if section_lines else None


def _has_structured_decision(body: str) -> bool:
    """Check if at least one structured decision record exists."""
    return bool(parse_decisions_table(body))


def _gap_entry(source_detail: str, text: str) -> str:
    """Convenience: build a [gap] evidence entry."""
    return generate_evidence_entry(
        tag="[gap]",
        source=f"ws transition audit ({source_detail})",
        text=text,
    )


def _commit_gaps(body: str, entries: List[Tuple[str, str]]) -> Tuple[str, Optional[str]]:
    """Append multiple gap entries to the evidence ledger.

    Each entry is (label, text). Returns (updated_body, combined_message)
    or (body, None) if entries is empty.
    """
    if not entries:
        return (body, None)

    messages: List[str] = []
    for label, text in entries:
        entry = _gap_entry(label, text)
        body = append_to_section(body, "evidence ledger", entry)
        messages.append(text)

    combined = "; ".join(messages)
    return (body, f"Audit: appended {len(entries)} [gap] — {combined}")


# ── Per-state audit functions ─────────────────────────────────────────────────


def _audit_build(body: str) -> Tuple[str, Optional[str]]:
    """Build-state audit: requires a decision with result: pass and a
    populated rationale (folded in from the former, unreachable
    "decision"-state audit — see 2026-08-11-001)."""
    decisions = parse_decisions_table(body)
    has_pass = any(d.get("result", "").strip() == "pass" for d in decisions)

    if not has_pass:
        return _commit_gaps(body, [
            ("build", (
                "No decision record with result: pass found at build transition. "
                "An accepted decision record is expected before entering build state."
            )),
        ])

    has_substantive = any(
        d.get("result", "").strip() == "pass" and _is_populated(d.get("rationale", ""))
        for d in decisions
    )

    if not has_substantive:
        return _commit_gaps(body, [
            ("build", (
                "A decision record with result: pass exists but none has a "
                "populated rationale. Claim sidecar expected to document "
                "contradiction and freshness exposure in the rationale field."
            )),
        ])

    return (body, None)


def _audit_verify(body: str) -> Tuple[str, Optional[str]]:
    """Verify-state audit: requires decision with result: pass and populated
    scope (requirement coverage), and checks for residual uncertainty gaps."""
    gaps: List[Tuple[str, str]] = []
    decisions = parse_decisions_table(body)

    has_verified = any(
        d.get("result", "").strip() == "pass"
        and _is_populated(d.get("scope", ""))
        for d in decisions
    )

    if not has_verified:
        gaps.append((
            "verify",
            "No decision record with result: pass and populated scope found. "
            "Requirement coverage evidence is expected before verify transition.",
        ))

    # Check for unresolved [gap] entries that indicate residual uncertainty
    if _has_evidence_gap(body):
        gaps.append((
            "verify",
            "Unresolved [gap] entries exist in the Evidence ledger. "
            "Residual uncertainty should be reviewed before proceeding.",
        ))

    return _commit_gaps(body, gaps)


def _audit_release(body: str) -> Tuple[str, Optional[str]]:
    """Release-state audit: requires at least one decision with result: pass
    (independence check) and review of unresolved gaps."""
    gaps: List[Tuple[str, str]] = []
    decisions = parse_decisions_table(body)

    has_pass = any(d.get("result", "").strip() == "pass" for d in decisions)

    if not has_pass:
        gaps.append((
            "release",
            "No decision record with result: pass found at release transition. "
            "Independence-appropriate evidence is expected before release.",
        ))

    # Unresolved gap review
    if _has_evidence_gap(body):
        gaps.append((
            "release",
            "Unresolved [gap] entries exist in the Evidence ledger. "
            "Unresolved gaps should be reviewed before release transition.",
        ))

    return _commit_gaps(body, gaps)


def _audit_observe(body: str) -> Tuple[str, Optional[str]]:
    """Observe-state audit: requires at least one decision with result:
    pass or fail (freeze ex ante basis)."""
    decisions = parse_decisions_table(body)

    has_outcome = any(
        d.get("result", "").strip() in ("pass", "fail")
        and _is_populated(d.get("rationale", ""))
        for d in decisions
    )

    if has_outcome:
        return (body, None)

    return _commit_gaps(body, [
        ("observe", (
            "No decision record with result: pass or fail and populated "
            "rationale found at observe transition. "
            "An ex ante basis freeze is expected before entering observe state."
        )),
    ])


def _is_populated(value: str) -> bool:
    """Check if a field value is substantively populated (not empty/placeholder)."""
    stripped = value.strip()
    if not stripped:
        return False
    # Exclude HTML comment placeholders
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return False
    return True


# ── Audit dispatch ────────────────────────────────────────────────────────────

_AUDIT_DISPATCH = {
    "build": _audit_build,
    "verify": _audit_verify,
    "release": _audit_release,
    "observe": _audit_observe,
}


def audit_epistemic_state(
    body: str,
    target_state: str,
    consequence: str,
) -> Tuple[str, Optional[str]]:
    """Audit a Work Object's epistemic state after a transition.

    Checks for expected evidence at the given target state and appends
    ``[gap]`` entries for anything missing. Returns ``(updated_body, message)``
    where ``message`` is a human-readable notice or ``None`` if no gaps were
    found.

    Extended per 2026-07-27-015: audits at decision, verify, release,
    and observe target states with consequence scaling.
    """
    # Determine which states to audit at this consequence level
    audit_states = _CONSEQUENCE_AUDIT_MAP.get(consequence, ())
    if target_state not in audit_states:
        return (body, None)

    # Dispatch to the per-state audit function
    audit_fn = _AUDIT_DISPATCH.get(target_state)
    if audit_fn is None:
        return (body, None)

    return audit_fn(body)
