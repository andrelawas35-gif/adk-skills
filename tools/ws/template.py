"""Body template generation for new Work Objects.

Generates the 7 required sections plus a structured Decisions template
for gate readiness per Decision 65 and Decision 70.
"""


def generate_body_template(title: str, obj_type: str, consequence: str) -> str:
    """Generate the complete body template for a new Work Object.

    Includes 7 required sections (Intent, Success evidence, Constraints and
    non-goals, Evidence ledger, Open questions, Next move, History) plus the
    structured Decisions and revisit triggers template.

    Args:
        title: Work Object title
        obj_type: One of change, inquiry, project, incident
        consequence: One of low, meaningful, high

    Returns:
        Complete body markdown string
    """
    sections = [
        _intent(title),
        _success_evidence(),
        _constraints_and_non_goals(),
        _decisions_template(consequence),
        _evidence_ledger(),
        _open_questions(),
        _next_move(),
        _history(),
    ]

    return "\n\n".join(sections) + "\n"


def _intent(title: str) -> str:
    return f"## Intent\n\n<!-- Describe what this Work Object accomplishes and why it exists. -->"


def _success_evidence() -> str:
    return (
        "## Success evidence\n\n"
        "<!-- Checklist of observable outcomes that indicate completion. -->\n"
        "- [ ] \n"
    )


def _constraints_and_non_goals() -> str:
    return (
        "## Constraints and non-goals\n\n"
        "**Constraints:**\n"
        "<!-- Boundaries the implementation must respect. -->\n\n"
        "**Non-goals:**\n"
        "<!-- Explicitly excluded work. -->"
    )


def _decisions_template(consequence: str) -> str:
    """Generate the structured Decisions template for gate readiness.

    Per Decision 65: ws create generates a structured Decisions section
    that the lifecycle gates can parse structurally.
    """
    build_note = ""
    if consequence == "high":
        build_note = (
            "<!-- BUILD GATE (high consequence): requires a decision record\n"
            "     with decision_type: decision before transitioning to build state.\n"
            "     Example entry below. -->\n"
        )

    return (
        "## Decisions and revisit triggers\n\n"
        "<!-- Structured decision records for lifecycle gate enforcement.\n"
        "     Each major decision gets its own record with the fields below.\n"
        "     The build, release, close, and observe gates read this section\n"
        "     structurally — keep field names exactly as shown. -->\n\n"
        f"{build_note}"
        "### Decision 1 — <summary>\n\n"
        "| Field | Value |\n"
        "|-------|-------|\n"
        "| **Decision type** | decision / authority / delegation |\n"
        "| **Result** | pass / fail / pending |\n"
        "| **Scope** | <!-- what this decision applies to --> |\n"
        "| **Authorization** | <!-- who or what authorized this --> |\n"
        "| **Confidence** | <!-- high / medium / low --> |\n"
        "| **Actor** | <!-- who made the decision --> |\n"
        "| **Revisit trigger** | <!-- condition that would cause reconsideration --> |\n"
        "| **Rationale** | <!-- why this decision was made --> |"
    )


def _evidence_ledger() -> str:
    return (
        "## Evidence ledger\n\n"
        "<!-- Tagged evidence entries. See references/EVIDENCE-MODEL.md for\n"
        "     allowed tags: [system], [decision], [inference], [observed],\n"
        "     [lived], [claimed], [inferred]. -->\n\n"
        "| Tag | Source | Entry |\n"
        "|-----|--------|-------|\n"
    )


def _open_questions() -> str:
    return (
        "## Open questions\n\n"
        "<!-- Unresolved questions that block progress or require a decision. -->"
    )


def _next_move() -> str:
    return (
        "## Next move\n\n"
        "<!-- The single next action this Work Object routes to. -->"
    )


def _history() -> str:
    return (
        "## History\n\n"
        "<!-- Append-only chronological record of state transitions,\n"
        "     decisions, and material changes. Each entry is a timestamped\n"
        "     subsection. -->"
    )
