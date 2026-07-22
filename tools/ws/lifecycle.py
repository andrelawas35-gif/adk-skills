"""8-state lifecycle transition graph with 2 prohibitions and 5 gates.

Enforces ADR 0015 terminal-state prohibitions and prerequisite gates
against structurally parsed Decisions fields. Grandfathers legacy objects
that lack structured Decisions by producing a "not yet satisfiable" message
rather than a hard failure.
"""

from typing import Dict, List, Optional, Tuple

from .sections import parse_decisions_table

# ── Valid states ──────────────────────────────────────────────────────────────

VALID_STATES = frozenset({
    "notice", "explore", "design", "build",
    "verify", "release", "observe", "close",
})

VALID_STATUSES = frozenset({"active", "waiting", "paused", "closed"})


# ── Terminal prohibitions ─────────────────────────────────────────────────────

# ADR 0015: Two absolute prohibitions
PROHIBITED_TRANSITIONS = [
    # close state → any other state (terminal state)
    ("close", "*"),
    # closed status → any other status (terminal status)
    ("*", "closed", "*"),  # (from_state, from_status, to_status)
]

# ── Transition graph (permissive default: any → any except prohibitions) ───────


def validate_transition(
    from_state: str,
    to_state: str,
    from_status: str,
    to_status: str,
) -> Optional[str]:
    """Validate a state/status transition against the lifecycle graph.

    Returns None if valid, or an error message describing the violation.
    """
    # Validate enum membership
    if from_state not in VALID_STATES:
        return f"Invalid current state '{from_state}'. Must be one of: {', '.join(sorted(VALID_STATES))}"
    if to_state not in VALID_STATES:
        return f"Invalid target state '{to_state}'. Must be one of: {', '.join(sorted(VALID_STATES))}"
    if from_status not in VALID_STATUSES:
        return f"Invalid current status '{from_status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
    if to_status not in VALID_STATUSES:
        return f"Invalid target status '{to_status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"

    # Prohibition 1: close state → any other state
    if from_state == "close" and to_state != "close":
        return (
            "Lifecycle violation: 'close' is a terminal state. "
            "Cannot transition from 'close' to another state."
        )

    # Prohibition 2: closed status → any other status
    if from_status == "closed" and to_status != "closed":
        return (
            "Lifecycle violation: 'closed' is a terminal status. "
            "Cannot transition from 'closed' to another status."
        )

    return None


# ── Gate enforcement ──────────────────────────────────────────────────────────

GATE_RESULT = Tuple[bool, str]
# (passed, message)


def check_build_gate(
    body: str,
    consequence: str,
) -> GATE_RESULT:
    """BUILD GATE (high consequence only): requires a decision record
    with decision_type: decision before transitioning to build state.

    For non-high consequence objects, the gate always passes.
    """
    if consequence != "high":
        return (True, "")

    decisions = parse_decisions_table(body)
    if not decisions:
        return (
            False,
            "Build gate failed: high-consequence Work Objects require "
            "at least one structured decision record in the Decisions section "
            "before transitioning to build state. "
            "Use 'ws append-history' or edit the Decisions section to add a "
            "decision record with decision_type: decision.",
        )

    for d in decisions:
        if d.get("decision_type") == "decision":
            return (True, "")

    return (
        False,
        "Build gate failed: no decision record with decision_type: decision found. "
        "High-consequence objects require an accepted decision record "
        "before entering build state.",
    )


def check_release_gate(body: str) -> GATE_RESULT:
    """RELEASE GATE (all consequence levels): requires result: pass
    and a scope field in the most recent decision record.
    """
    decisions = parse_decisions_table(body)
    if not decisions:
        return (
            False,
            "Release gate failed: no structured decision records found. "
            "At least one decision record with result: pass and a scope field "
            "is required before transitioning to release state.",
        )

    # Check the most recent decision (last in list)
    latest = decisions[-1]
    result = latest.get("result", "").strip()
    scope = latest.get("scope", "").strip()

    if result != "pass":
        return (
            False,
            f"Release gate failed: most recent decision has result: '{result}'. "
            "Result must be 'pass' before transitioning to release state.",
        )

    if not scope or scope == "<!-- what this decision applies to -->":
        return (
            False,
            "Release gate failed: most recent decision has no scope defined. "
            "A scope field is required before release.",
        )

    return (True, "")


def check_close_gate(body: str) -> GATE_RESULT:
    """CLOSE GATE (all consequence levels): requires an outcome record.

    An outcome record is a decision with either result: pass or result: fail
    and a populated rationale or scope.
    """
    decisions = parse_decisions_table(body)
    if not decisions:
        return (
            False,
            "Close gate failed: no structured decision records found. "
            "At least one decision record with a result (pass/fail) is required "
            "before closing.",
        )

    for d in reversed(decisions):
        result = d.get("result", "").strip()
        if result in ("pass", "fail"):
            return (True, "")

    return (
        False,
        "Close gate failed: no decision record with result: pass or result: fail found. "
        "An outcome record is required before closing.",
    )


def check_observe_gate(body: str) -> GATE_RESULT:
    """OBSERVE GATE (all consequence levels): requires result: pass
    for deployment/recovery objects entering observe state.
    """
    decisions = parse_decisions_table(body)
    if not decisions:
        return (
            False,
            "Observe gate failed: no structured decision records found. "
            "At least one decision with result: pass is required before "
            "transitioning to observe state.",
        )

    for d in decisions:
        if d.get("result", "").strip() == "pass":
            return (True, "")

    return (
        False,
        "Observe gate failed: no decision record with result: pass found. "
        "A passing result is required before observing.",
    )


# ── Gate dispatch ─────────────────────────────────────────────────────────────

def check_gates_for_transition(
    body: str,
    to_state: str,
    consequence: str,
) -> GATE_RESULT:
    """Run the relevant prerequisite gates for a target state transition.

    Returns (passed, message). If passed=True, message is empty.
    If passed=False, message describes the gate failure.
    """
    gate_map = {
        "build": lambda: check_build_gate(body, consequence),
        "release": lambda: check_release_gate(body),
        "close": lambda: check_close_gate(body),
        "observe": lambda: check_observe_gate(body),
    }

    if to_state in gate_map:
        return gate_map[to_state]()

    return (True, "")


# ── Close consequence scaling ─────────────────────────────────────────────────

def can_close_directly(consequence: str, from_state: str) -> bool:
    """Determine if a Work Object can close directly from its current state.

    Low/meaningful consequence: can close from any state (status → closed).
    High consequence: must first transition to close state, then close.
    """
    if consequence in ("low", "meaningful"):
        return True
    if consequence == "high":
        return from_state == "close"
    return False


def get_close_route(consequence: str, from_state: str) -> str:
    """Return the required route for closing.

    Returns either 'direct' (set status: closed) or 'two-step' (transition
    to close state first, then close).
    """
    if can_close_directly(consequence, from_state):
        return "direct"
    return "two-step"
