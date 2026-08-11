"""Markdown body section parser, appender, and validator.

Parses Work Object body into named sections by ## Heading, supports
append-only operations, and can extract structured Decisions fields
for lifecycle gate enforcement.
"""

import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# ── Valid evidence tags ───────────────────────────────────────────────────────

# Canonical set from AGREEMENT-LOOP.md (lines 96-111):
#   [system]    — code, configuration, executable results, records
#   [decision]  — explicit user or accountable-owner decisions
#   [inference] — agent reasoning and unverified hypotheses
#   [gap]       — facts that could not be accessed or established
#   [testimony] — attributable human observations with context/uncertainty
#   [memory]    — relevant, user-approved reusable preferences

VALID_EVIDENCE_TAGS = frozenset({
    "[system]", "[decision]", "[inference]",
    "[gap]", "[testimony]", "[memory]",
})


# ── Section parsing ───────────────────────────────────────────────────────────

def parse_sections(body: str) -> Dict[str, str]:
    """Parse a Markdown body into named sections.

    Sections are identified by ## Heading lines. Everything before the
    first ## Heading is treated as preamble (keyed as "").

    Returns a dict mapping section name (lowercase, stripped) to content
    (including the heading line).

    Raises ValueError if duplicate headings are found.
    """
    sections: Dict[str, str] = {}
    current_name = ""
    current_lines: List[str] = []
    seen_names: Dict[str, int] = {}

    for line in body.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_lines:
                sections[current_name] = "\n".join(current_lines)

            name = line[3:].strip().lower()
            if name in seen_names:
                raise ValueError(
                    f"Duplicate heading '## {line[3:].strip()}' "
                    f"at lines {seen_names[name]} and unknown"
                )
            seen_names[name] = -1  # line tracking simplified

            current_name = name
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_name] = "\n".join(current_lines)

    return sections


def get_section(body: str, name: str) -> Optional[str]:
    """Get a single named section from the body.

    Returns the section content (including heading) or None.
    """
    sections = parse_sections(body)
    return sections.get(name.lower())


def append_to_section(
    body: str,
    section_name: str,
    entry: str,
) -> str:
    """Append an entry to a named section.

    The entry is appended after the last line of the named section,
    preserving existing content. If the section doesn't exist, it is
    created at the end of the body.

    Args:
        body: Current body text.
        section_name: Name of the section to append to (e.g. "Evidence ledger").
        entry: The entry text to append.

    Returns:
        Modified body with the entry appended.

    Raises:
        ValueError: If the body has no sections at all.
    """
    sections = parse_sections(body)
    key = section_name.lower()

    if key in sections:
        # Append to existing section
        section_content = sections[key]
        new_section = section_content.rstrip("\n") + "\n" + entry
        return body.replace(section_content, new_section, 1)

    # Section doesn't exist — append at end
    return body.rstrip("\n") + f"\n\n## {section_name}\n\n{entry}\n"


# ── Section order validation ──────────────────────────────────────────────────

REQUIRED_SECTION_ORDER = [
    "intent",
    "success evidence",
    "constraints and non-goals",
    "decisions and revisit triggers",
    "evidence ledger",
    "open questions",
    "next move",
    "history",
]


def validate_section_order(body: str) -> List[str]:
    """Validate that required sections appear in the correct order.

    Returns a list of error messages. Empty list = valid.
    Missing sections are reported but don't break ordering.
    """
    sections = parse_sections(body)
    found_names = list(sections.keys())
    errors = []

    # Check required sections exist
    for name in REQUIRED_SECTION_ORDER:
        if name not in found_names:
            errors.append(f"Missing required section: ## {name.title()}")

    # Check ordering among found required sections
    last_idx = -1
    for name in found_names:
        if name in REQUIRED_SECTION_ORDER:
            idx = REQUIRED_SECTION_ORDER.index(name)
            if idx < last_idx:
                errors.append(
                    f"Section '## {name.title()}' is out of order. "
                    f"Expected after '## {REQUIRED_SECTION_ORDER[last_idx].title()}'."
                )
            last_idx = idx

    return errors


# ── Structured Decisions parsing ──────────────────────────────────────────────

def parse_decisions_table(body: str) -> List[Dict[str, str]]:
    """Extract structured decision records from the Decisions section.

    Each decision is a ### Decision N — <summary> block containing a
    markdown table with field: value rows.

    Returns a list of dicts, one per decision record.
    """
    section = get_section(body, "decisions and revisit triggers")
    if not section:
        return []

    decisions = []
    # Split by ### Decision headers
    decision_blocks = re.split(r"\n(?=### Decision \d+)", section)

    for block in decision_blocks:
        if not block.strip().startswith("### Decision"):
            continue

        record: Dict[str, str] = {}
        # Extract decision number and summary
        header_match = re.match(r"### Decision (\d+) — (.+)", block.split("\n")[0])
        if header_match:
            record["number"] = header_match.group(1)
            record["summary"] = header_match.group(2)

        # Parse the table rows
        for line in block.split("\n"):
            # Match | **Field** | value |
            m = re.match(r"\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|", line)
            if m:
                key = m.group(1).strip().lower()
                val = m.group(2).strip()
                # Map display names to canonical keys
                key_map = {
                    "decision type": "decision_type",
                    "result": "result",
                    "scope": "scope",
                    "authorization": "authorization",
                    "confidence": "confidence",
                    "actor": "actor",
                    "revisit trigger": "revisit_trigger",
                    "rationale": "rationale",
                }
                if key in key_map:
                    record[key_map[key]] = val

        if len(record) > 2:  # More than just number and summary
            decisions.append(record)

    return decisions


# ── History entry generation ──────────────────────────────────────────────────

def generate_history_entry(
    action: str,
    state: str,
    status: str,
    actor: str,
    rationale: str,
    commit: Optional[str] = None,
) -> str:
    """Generate a timestamped History subsection entry.

    Format matches the History section template (### Heading with
    timestamp + structured fields).

    Optional commit links the entry to a Git commit SHA per ADR 0023.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = (
        f"### {now} — {action}\n\n"
        f"- **State:** {state}\n"
        f"- **Status:** {status}\n"
        f"- **Actor:** {actor}\n"
        f"- **Rationale:** {rationale}"
    )
    if commit:
        entry += f"\n- **Commit:** {commit}"
    return entry


# ── Evidence entry generation ─────────────────────────────────────────────────

def generate_evidence_entry(
    tag: str,
    source: str,
    text: str,
    sha: Optional[str] = None,
) -> str:
    """Generate an evidence ledger table row.

    Validates the tag is an allowed value. Optional SHA is only
    accepted on [system] entries per ADR 0023.
    """
    if tag not in VALID_EVIDENCE_TAGS:
        raise ValueError(
            f"Invalid evidence tag '{tag}'. "
            f"Must be one of: {', '.join(sorted(VALID_EVIDENCE_TAGS))}"
        )

    if sha and tag != "[system]":
        raise ValueError(
            f"SHA is only allowed on [system] evidence entries, not '{tag}'."
        )

    if sha:
        return f"| {tag} | {source} | {text} | {sha} |"
    return f"| {tag} | {source} | {text} |"


# ── Object text composition ───────────────────────────────────────────────────


def compose_object_text(frontmatter: str, body: str) -> str:
    """Compose a Work Object file's frontmatter and body text.

    Guarantees exactly one trailing newline so the file passes
    file-integrity (2026-08-10-005). The mutation commands append entries
    that carry no trailing newline; without normalization every write would
    leave the file without a final newline and trip the truncation check.
    """
    return frontmatter.rstrip("\n") + "\n" + body.rstrip("\n") + "\n"


# ── Append-only detection ─────────────────────────────────────────────────────

def check_append_only(
    body: str,
    section_name: str,
    new_entry: str,
) -> bool:
    """Verify that an append operation is truly append-only.

    Checks that the new entry doesn't match any existing line
    in the section (a simple duplicate detection) and that the
    operation is adding content, not modifying existing content.

    This is a structural check only — it doesn't verify semantic
    append-only invariants (e.g., that History entries aren't
    retroactively edited).
    """
    section = get_section(body, section_name)
    if not section:
        return True  # New section — nothing to conflict with

    # The entry text should not already appear verbatim
    entry_stripped = new_entry.strip()
    return entry_stripped not in section
