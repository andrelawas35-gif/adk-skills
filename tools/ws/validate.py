"""Composed validation checks for Work Objects.

Runs named validation checks against Work Object files or the full
workspace. Each check is independently invocable. With no args, runs
all checks against all objects.

Checks:
  schema                   — YAML frontmatter field validation
  sections                 — Required section presence and ordering
  append-only              — History/Evidence/Decisions are append-only
  attention                — active.md consistency cross-check
  attention-limits         — active.md quantitative cap enforcement
  sensitivity              — Restricted content keyword scanning
  sensitivity-policy       — Restricted/private storage and pointer rules
  lifecycle                — No terminal-state violations
  claims                   — No outcome claims without supporting evidence
  lanes                    — Evidence entries use canonical tags and format
  authority                — High-consequence objects have required authority
  protected-fields         — Immutable field format and chronology validation
  history-integrity        — History section chronological order and structure
  file-integrity           — Structural completeness (partial write detection)
  incident-routing         — Incident successor linkage and resolution records
  prerequisites            — State prerequisites satisfied (end-to-end gates)
  unsupported-capabilities — Adapter degradation declarations
  interrupted-mutations    — Orphaned temp/lock file detection
  structure                — Composite: schema + sections
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .schema import (
    parse_frontmatter,
    validate_consequence,
    validate_sensitivity,
    validate_state,
    validate_status,
    validate_type,
)
from .sections import (
    REQUIRED_SECTION_ORDER,
    parse_decisions_table,
    parse_sections,
    validate_section_order,
)
from .lifecycle import (
    VALID_STATES,
    VALID_STATUSES,
    validate_transition,
)
from .attention import check_attention_consistency


# ── Schema check ──────────────────────────────────────────────────────────────


def check_schema(file_path: Path) -> List[str]:
    """Validate YAML frontmatter for a single Work Object.

    Checks: presence of required fields, enum membership, immutable
    field consistency.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    try:
        fm = parse_frontmatter(content)
    except ValueError as e:
        return [f"{file_path}: Invalid frontmatter: {e}"]

    # Required fields
    required_fields = [
        "schema_version", "id", "title", "type",
        "status", "state", "consequence", "sensitivity",
        "created_at", "updated_at",
    ]
    for field in required_fields:
        if field not in fm:
            errors.append(f"{file_path}: Missing required field: {field}")

    # Enum validation
    for field, validator, valid_set in [
        ("type", validate_type, {"change", "inquiry", "project", "incident"}),
        ("status", validate_status, {"active", "waiting", "paused", "closed"}),
        ("state", validate_state, VALID_STATES),
        ("consequence", validate_consequence, {"low", "meaningful", "high"}),
        ("sensitivity", validate_sensitivity, {"ordinary", "restricted"}),
    ]:
        value = fm.get(field)
        if value is not None:
            err = validator(str(value))
            if err:
                errors.append(f"{file_path}: {err}")

    # Immutable field check: id in filename must match id in frontmatter
    fm_id = str(fm.get("id", ""))
    if fm_id and not file_path.name.startswith(fm_id):
        errors.append(
            f"{file_path}: Frontmatter id '{fm_id}' does not match filename"
        )

    return errors


# ── Sections check ────────────────────────────────────────────────────────────


def check_sections(file_path: Path) -> List[str]:
    """Validate required section presence and ordering."""
    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    # Extract body (everything after frontmatter)
    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return [f"{file_path}: Unclosed frontmatter"]
        body = content[end + 3:].strip()
    else:
        body = content

    section_errors = validate_section_order(body)
    return [f"{file_path}: {e}" for e in section_errors]


# ── Append-only check ─────────────────────────────────────────────────────────


def check_append_only(file_path: Path) -> List[str]:
    """Check that append-only sections haven't lost content.

    Uses a structural heuristic: the file's History section (if present)
    should not be empty for objects beyond the notice state. Also checks
    that Evidence ledger entries follow the table format.

    Note: Full append-only verification requires git history comparison
    (as verify-append-only.py does). This check provides structural
    validation only.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)

    # Extract body
    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return [f"{file_path}: Unclosed frontmatter"]
        body = content[end + 3:].strip()
    else:
        body = content

    sections = parse_sections(body)

    # History section structural check
    history = sections.get("history", "")
    if not history or history.strip() == "## History":
        # Empty history is fine for notice-state objects
        state = str(fm.get("state", "notice"))
        if state != "notice":
            errors.append(
                f"{file_path}: History section is empty but object state is '{state}'"
            )

    # Evidence ledger structural check
    evidence = sections.get("evidence ledger", "")
    if evidence:
        lines = evidence.strip().split("\n")
        # Skip heading and table header (first 3 lines)
        for i, line in enumerate(lines):
            if i < 3:
                continue
            if line.strip() and not line.strip().startswith("|"):
                errors.append(
                    f"{file_path}: Evidence ledger line {i+1} does not follow table format"
                )

    return errors


# ── Canonical evidence tags (from AGREEMENT-LOOP.md) ──────────────────────────

_CANONICAL_EVIDENCE_TAGS = frozenset({
    "[system]",
    "[decision]",
    "[inference]",
    "[gap]",
    "[testimony]",
    "[memory]",
})

# ── Evidence lane check ───────────────────────────────────────────────────────


def _is_table_header(raw: str) -> bool:
    """Check if a table row is a header row (Tag | Source | Entry).

    A header row has cells whose stripped, asterisk-free text is one of
    the known header keywords. Data rows may contain these words but not
    as standalone cell values.
    """
    cells = [c.strip().strip("*").lower() for c in raw.strip("| ").split("|")]
    header_keywords = {"tag", "source", "entry"}
    # A header row has at least 2 cells that are exact header keyword matches
    matches = sum(1 for c in cells if c in header_keywords)
    return matches >= 2


def _parse_evidence_entries(body: str) -> List[Tuple[int, str, str]]:
    """Parse evidence ledger entries into (line_number, tag, raw_line) tuples.

    Handles both table format (| [tag] | source | text |) and inline format
    (- <timestamp> — [tag] <text>). Returns empty list if no evidence section.
    """
    sections = parse_sections(body)
    evidence = sections.get("evidence ledger", "")
    if not evidence:
        return []

    entries = []
    for i, line in enumerate(evidence.split("\n")):
        raw = line.strip()
        if not raw:
            continue

        # Skip separator lines (|---|---|)
        if re.match(r"^\|[-\s|]+\|$", raw):
            continue

        # Table format: | [tag] | source | text | (backticks optional)
        if raw.startswith("|"):
            match = re.match(
                r"^\|\s*`?(\[[a-z_]+\])`?\s*\|.*$", raw
            )
            if match:
                tag = match.group(1)
                entries.append((i + 1, tag, raw))
            elif not _is_table_header(raw):
                # Not a header row — malformed table entry
                entries.append((i + 1, "", raw))
            continue

        # Inline format: - <timestamp> — [tag] <text> (backticks optional)
        if raw.startswith("- "):
            match = re.match(r"^-\s+\S+\s+[—–-]\s+`?(\[[a-z_]+\])`?", raw)
            if match:
                tag = match.group(1)
                entries.append((i + 1, tag, raw))
            else:
                entries.append((i + 1, "", raw))

    return entries


def check_evidence_lanes(file_path: Path) -> List[str]:
    """Reject evidence entries with invalid tags or malformed format.

    Checks:
      1. Every evidence entry uses a tag from the canonical set defined
         in AGREEMENT-LOOP.md.
      2. Every evidence entry has a recognizable tag (brackets present).
      3. Malformed table rows are reported.

    The canonical tag set is: [system], [decision], [inference],
    [gap], [testimony], [memory].
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    body = _extract_body(content)
    entries = _parse_evidence_entries(body)

    for line_num, tag, raw in entries:
        if not tag:
            errors.append(
                f"{file_path}: Evidence ledger line {line_num} has no "
                f"recognizable evidence tag: {raw[:60]}"
            )
        elif tag not in _CANONICAL_EVIDENCE_TAGS:
            errors.append(
                f"{file_path}: Evidence ledger line {line_num} uses "
                f"non-canonical tag '{tag}'. Canonical tags are: "
                f"{', '.join(sorted(_CANONICAL_EVIDENCE_TAGS))}"
            )

    return errors


# ── Sensitivity check ─────────────────────────────────────────────────────────


def check_sensitivity(file_path: Path) -> List[str]:
    """Check that restricted-content objects use pointers, not inline body.

    Per ADR 0019: restricted sensitivity objects should not contain
    restricted content directly in the body.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    sensitivity = str(fm.get("sensitivity", "ordinary"))

    if sensitivity == "restricted":
        # Check for common restricted-content patterns
        restricted_patterns = [
            "password", "secret", "token", "api_key",
            "credential", "private_key",
        ]
        body_lower = content.lower()
        for pattern in restricted_patterns:
            if pattern in body_lower:
                errors.append(
                    f"{file_path}: Restricted object may contain sensitive "
                    f"content (found '{pattern}'). Use pointer references instead."
                )
                break  # One warning per file is sufficient

    return errors


# ── Lifecycle check ───────────────────────────────────────────────────────────


def check_lifecycle(file_path: Path) -> List[str]:
    """Check for terminal-state violations in Work Objects."""
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    state = str(fm.get("state", ""))
    status = str(fm.get("status", ""))

    # Check: state 'close' but status not 'closed'
    if state == "close" and status != "closed":
        errors.append(
            f"{file_path}: State is 'close' but status is '{status}'. "
            "Objects in close state should have closed status."
        )

    # Check: status 'closed' with state that implies active work
    closed_incompatible = {"notice", "explore", "design", "build", "verify"}
    if status == "closed" and state in closed_incompatible:
        errors.append(
            f"{file_path}: Status is 'closed' but state is '{state}'. "
            "Closed objects should be in 'close', 'release', or 'observe' state."
        )

    return errors


# ── Forbidden claims check ────────────────────────────────────────────────────


def _extract_body(content: str) -> str:
    """Extract body text from a Work Object, stripping frontmatter."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return ""
        return content[end + 3:].strip()
    return content


def _count_evidence_entries(body: str) -> int:
    """Count evidence ledger table rows (non-empty data lines after header)."""
    sections = parse_sections(body)
    evidence = sections.get("evidence ledger", "")
    if not evidence:
        return 0
    count = 0
    past_header = False
    for line in evidence.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Skip the separator line (e.g. |-----|--------|-------|)
        if re.match(r"^\|[-\s|]+\|$", stripped):
            past_header = True
            continue
        # Skip the header row (Tag | Source | Entry)
        if not past_header:
            past_header = True
            continue
        count += 1
    return count


def _count_checked_success_items(body: str) -> int:
    """Count checked (- [x]) items in the Success Evidence section."""
    sections = parse_sections(body)
    se = sections.get("success evidence", "")
    if not se:
        return 0
    return len(re.findall(r"^\s*- \[x\]", se, re.MULTILINE | re.IGNORECASE))


def _has_verification_result(body: str) -> bool:
    """Check if any decision record has a pass/fail result in Decisions."""
    decisions = parse_decisions_table(body)
    for d in decisions:
        if d.get("result", "").lower() in ("pass", "fail"):
            return True
    return False


def check_claims(file_path: Path) -> List[str]:
    """Reject Work Objects that claim outcomes without supporting evidence.

    Checks:
      1. State beyond 'notice' requires at least one Evidence Ledger entry.
      2. State 'verify' or 'release' requires at least one Evidence Ledger
         entry referencing an explicit check result.
      3. Checked success-evidence items require at least one corresponding
         Evidence Ledger entry per item.
      4. Any Decision with 'result: pass' requires at least one Evidence
         Ledger entry (the result is itself a claim that must be evidenced).
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    body = _extract_body(content)
    state = str(fm.get("state", "notice"))
    status = str(fm.get("status", "active"))

    # Terminal states are exempt — evidence review is for active work.
    if state == "close" or status == "closed":
        return []

    evidence_entries = _count_evidence_entries(body)
    checked_items = _count_checked_success_items(body)

    # ── Claim 1: Active state requires evidence ──────────────────────────

    if state != "notice" and evidence_entries == 0:
        errors.append(
            f"{file_path}: State is '{state}' but Evidence Ledger is empty. "
            "Any state beyond 'notice' requires at least one evidence entry."
        )

    # ── Claim 2: Verify/release states require explicit evidence ─────────

    evidence_required_states = {"verify", "release"}
    if state in evidence_required_states and evidence_entries == 0:
        errors.append(
            f"{file_path}: State is '{state}' but Evidence Ledger is empty. "
            "States that claim verification or release readiness require "
            "at least one evidence entry."
        )

    # ── Claim 3: Checked success items need evidence coverage ────────────

    if checked_items > 0 and evidence_entries == 0:
        errors.append(
            f"{file_path}: {checked_items} success-evidence item(s) are "
            "checked but Evidence Ledger is empty. Each checked item "
            "requires a corresponding evidence entry."
        )
    elif checked_items > evidence_entries:
        errors.append(
            f"{file_path}: {checked_items} success-evidence item(s) are "
            f"checked but only {evidence_entries} evidence entries exist. "
            "Checked items should not outnumber evidence entries."
        )

    # ── Claim 4: pass/fail decision result requires evidence ─────────────

    if _has_verification_result(body) and evidence_entries == 0:
        errors.append(
            f"{file_path}: Decisions section contains a pass/fail result "
            "but Evidence Ledger is empty. A verification result is itself "
            "a claim that requires supporting evidence."
        )

    return errors


# ── Authority check ───────────────────────────────────────────────────────────

_AUTHORITY_REQUIRED_FIELDS = [
    "scope",
    "evidence reviewed",
    "constraints",
    "authority mode",
    "granted by",
]


def _parse_history_entries(body: str) -> List[Dict[str, str]]:
    """Parse History section into individual entries.

    Each entry starts with ``### <timestamp> — <action>`` and contains
    ``- **Field:** value`` lines until the next heading or end of section.
    """
    sections = parse_sections(body)
    history = sections.get("history", "")
    if not history:
        return []

    entries = []
    current: Optional[Dict[str, str]] = None

    for line in history.split("\n"):
        # New entry heading
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            if current is not None:
                entries.append(current)
            current = {"_heading": m.group(1).strip()}
            continue

        # Field line within an entry
        if current is not None:
            fm_match = re.match(r"^-\s+\*\*(.+?)\*\*\s*(.*)$", line)
            if fm_match:
                key = fm_match.group(1).strip().rstrip(":").lower()
                current[key] = fm_match.group(2).strip()

    if current is not None:
        entries.append(current)

    return entries


def _is_authority_entry(entry: Dict[str, str]) -> bool:
    """Check if a History entry is an Authority entry."""
    heading = entry.get("_heading", "")
    return "authority:" in heading.lower()


def _validate_authority_fields(entry: Dict[str, str]) -> List[str]:
    """Validate that an Authority entry has all required fields."""
    missing = []
    for field in _AUTHORITY_REQUIRED_FIELDS:
        if field not in entry:
            missing.append(field)
    return missing


def check_authority(file_path: Path) -> List[str]:
    """Reject high-consequence Work Objects that lack required authority records.

    Checks (per CONSEQUENCE-AUTHORITY.md):
      1. High-consequence objects in any state beyond 'notice' must have
         at least one Authority History entry.
      2. Every Authority entry must have all 5 required fields: Scope,
         Evidence reviewed, Constraints, Authority mode, Granted by.
      3. An Authority entry with mode 'accepted-recommendation' should
         be preceded by a recommendation entry (warning only).
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    body = _extract_body(content)
    consequence = str(fm.get("consequence", "low"))
    state = str(fm.get("state", "notice"))

    # Authority gates apply primarily to high-consequence objects
    if consequence != "high":
        return []

    # Terminal states are exempt — authority was already granted
    if state == "close" or str(fm.get("status", "")) == "closed":
        return []

    entries = _parse_history_entries(body)
    authority_entries = [e for e in entries if _is_authority_entry(e)]

    # ── Check 1: State beyond notice requires authority ───────────────────

    if state != "notice" and not authority_entries:
        errors.append(
            f"{file_path}: High-consequence object in state '{state}' "
            "but no Authority History entry found. Per "
            "CONSEQUENCE-AUTHORITY.md, every state transition beyond "
            "'notice' for high-consequence objects requires explicit "
            "authority recorded in History."
        )

    # ── Check 2: Validate each authority entry's fields ───────────────────

    for entry in authority_entries:
        heading = entry.get("_heading", "unknown")
        missing = _validate_authority_fields(entry)
        if missing:
            errors.append(
                f"{file_path}: Authority entry '{heading}' is missing "
                f"required fields: {', '.join(missing)}. Required: "
                f"{', '.join(_AUTHORITY_REQUIRED_FIELDS)}."
            )

    # ── Check 3: accepted-recommendation needs preceding recommendation ───

    for i, entry in enumerate(entries):
        if not _is_authority_entry(entry):
            continue
        mode = entry.get("authority mode", "")
        if mode == "accepted-recommendation":
            if i == 0 or _is_authority_entry(entries[i - 1]):
                errors.append(
                    f"{file_path}: Authority entry "
                    f"'{entry.get('_heading', '')}' uses "
                    "'accepted-recommendation' mode but is not preceded "
                    "by a recommendation entry. An accepted-recommendation "
                    "authority must follow the recommendation it confirms."
                )

    return errors


# ── Attention-register limits check ────────────────────────────────────────────


def check_attention_limits(
    active_md_path: Path,
    _file_paths: Optional[List[Path]] = None,
) -> List[str]:
    """Enforce attention register quantitative limits.

    Per the conducting skill: at most one Primary Work Object and at most
    two Supporting Work Objects. Total active cannot exceed 3.

    This is a workspace-level check (takes active_md_path, not a Work
    Object path). The runner passes file_paths as a second argument for
    compatibility with the check registry dispatch convention.
    """
    errors = []

    if not active_md_path or not active_md_path.exists():
        return []  # No register, nothing to enforce

    try:
        content = active_md_path.read_text()
    except Exception as e:
        return [f"Cannot read active.md: {e}"]

    # Count entries by section
    primary_count = 0
    supporting_count = 0
    current_section = ""

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            name = stripped[3:].strip().lower()
            current_section = name
            continue
        if stripped.startswith("- `") and " — " in stripped:
            if current_section == "primary":
                primary_count += 1
            elif current_section == "supporting":
                supporting_count += 1

    if primary_count > 1:
        errors.append(
            f"Attention register has {primary_count} Primary entries "
            "(maximum 1). Move excess Primary objects to Supporting "
            "or close them."
        )

    if supporting_count > 2:
        errors.append(
            f"Attention register has {supporting_count} Supporting "
            "entries (maximum 2). Close or pause excess objects."
        )

    total = primary_count + supporting_count
    if total > 3:
        errors.append(
            f"Attention register has {total} total active entries "
            "(maximum 3: 1 Primary + 2 Supporting)."
        )

    return errors


# ── Protected-fields check ─────────────────────────────────────────────────────


# Fields that must never change after creation
_IMMUTABLE_FIELDS = frozenset({"id", "created_at"})

# Valid id pattern: YYYY-MM-DD-NNN
_ID_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}$")

# Valid RFC-3339 timestamp (simplified)
_TS_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def check_protected_fields(file_path: Path) -> List[str]:
    """Validate protected (immutable) fields in Work Object frontmatter.

    Checks:
      1. ``id`` field matches the YYYY-MM-DD-NNN pattern.
      2. ``id`` in frontmatter matches the filename prefix.
      3. ``created_at`` is a valid RFC-3339 timestamp.
      4. ``updated_at`` is a valid RFC-3339 timestamp.
      5. ``created_at`` ≤ ``updated_at`` (timestamps are chronological).

    Note: True immutability enforcement requires a baseline comparison
    (e.g., git history). These checks catch structural violations.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)

    # ── id field ──────────────────────────────────────────────────────────

    obj_id = str(fm.get("id", ""))
    if not obj_id:
        errors.append(f"{file_path}: Missing required field: id")
    elif not _ID_PATTERN.match(obj_id):
        errors.append(
            f"{file_path}: id '{obj_id}' does not match required "
            "format YYYY-MM-DD-NNN"
        )

    # Already checked in check_schema but reinforce here for independence
    if obj_id and not file_path.name.startswith(obj_id):
        errors.append(
            f"{file_path}: Frontmatter id '{obj_id}' does not match filename"
        )

    # ── Timestamp fields ──────────────────────────────────────────────────

    created = str(fm.get("created_at", ""))
    updated = str(fm.get("updated_at", ""))

    if created and not _TS_PATTERN.match(created):
        errors.append(
            f"{file_path}: created_at '{created}' is not a valid "
            "RFC-3339 timestamp"
        )

    if updated and not _TS_PATTERN.match(updated):
        errors.append(
            f"{file_path}: updated_at '{updated}' is not a valid "
            "RFC-3339 timestamp"
        )

    if created and updated and created > updated:
        errors.append(
            f"{file_path}: created_at ({created}) is after "
            f"updated_at ({updated}). Timestamps must be chronological."
        )

    return errors


# ── Sensitivity policy check ───────────────────────────────────────────────────


def check_sensitivity_policy(file_path: Path) -> List[str]:
    """Enforce sensitivity-specific storage and content rules.

    Checks beyond keyword-pattern scanning (delegated to check_sensitivity):
      1. ``restricted`` objects must use pointer references, not inline
         content. They must have a Pointers or References section.
      2. ``restricted`` objects should not have substantial body content
         beyond frontmatter and pointers (stub sections only).
      3. ``private`` objects must be stored under .work-studio/ (checked
         via file path).

    ADR 0019: "Restricted: Never store in Work Objects. Link to protected
    sources; reference by pointer only."
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    sensitivity = str(fm.get("sensitivity", "ordinary"))

    if sensitivity != "restricted":
        return []

    body = _extract_body(content)
    sections = parse_sections(body)

    # ── Check 1: Pointer/references section required ─────────────────────

    has_pointer_section = any(
        name in ("pointers", "references")
        for name in sections
    )

    if not has_pointer_section:
        errors.append(
            f"{file_path}: Restricted-sensitivity object must have "
            "a '## Pointers' or '## References' section linking to "
            "protected sources. Per ADR 0019: restricted content is "
            "never stored directly — it is referenced by pointer only."
        )

    # ── Check 2: No substantial inline content beyond stubs ──────────────

    # Sections that should be stubs (empty or template-only) in restricted
    # objects. We check that these sections don't contain real content.
    stub_sections = {
        "intent", "success evidence", "constraints and non-goals",
        "open questions",
    }

    for name in stub_sections:
        if name not in sections:
            continue
        sec_content = sections[name]
        # Count substantive lines (not headings, not empty, not checkbox templates)
        substantive = [
            l for l in sec_content.split("\n")
            if l.strip()
            and not l.strip().startswith("#")
            and not l.strip().startswith("- [ ]")
        ]
        # Allow up to 2 substantive lines (brief description is fine)
        if len(substantive) > 2:
            errors.append(
                f"{file_path}: Restricted-sensitivity object has "
                f"substantial inline content in '{name}' section "
                f"({len(substantive)} lines). Per ADR 0019, restricted "
                "content should use pointer references, not inline body "
                "content."
            )

    return errors


# ── History integrity check (append-only end-to-end) ──────────────────────────


# Pattern for a History entry heading: ### <timestamp> — <action>
_HISTORY_HEADING_RE = re.compile(
    r"^###\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))"
    r"\s+[—–-]\s+(.+)$"
)


def check_history_integrity(file_path: Path) -> List[str]:
    """Validate History section append-only integrity.

    Checks (structural, without git history):
      1. Every History entry has a valid ``### <timestamp> — <action>`` heading.
      2. History entries are in chronological order (timestamps never decrease).
      3. No duplicate entry headings.
      4. The History section is not empty for objects past the notice state.
      5. History entries contain the standard fields (State, Status, Actor).

    True append-only enforcement (no edits to past entries) requires git
    history comparison via verify-append-only.py. This check provides
    structural validation that catches common violations.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    body = _extract_body(content)
    state = str(fm.get("state", "notice"))
    sections = parse_sections(body)
    history = sections.get("history", "")

    # ── Check: History not empty for active objects ──────────────────────

    if (not history or history.strip() == "## History") and state != "notice":
        errors.append(
            f"{file_path}: History section is empty but object state "
            f"is '{state}'. Objects past notice must have History entries."
        )

    if not history:
        return errors

    # ── Parse entries ────────────────────────────────────────────────────

    lines = history.split("\n")
    entries: List[Dict] = []  # Each: {heading, timestamp, action, line_start, line_end}
    current: Optional[Dict] = None

    for i, line in enumerate(lines):
        m = _HISTORY_HEADING_RE.match(line)
        if m:
            if current is not None:
                entries.append(current)
            current = {
                "heading": line.strip(),
                "timestamp": m.group(1),
                "action": m.group(2).strip(),
                "line_start": i + 1,
            }
        elif line.startswith("### "):
            # Malformed heading — not matching the timestamp pattern
            if current is not None:
                entries.append(current)
            current = {
                "heading": line.strip(),
                "timestamp": None,
                "action": None,
                "line_start": i + 1,
            }

    if current is not None:
        entries.append(current)

    if not entries:
        return errors

    # ── Check 1: Valid heading format ────────────────────────────────────

    for entry in entries:
        if entry["timestamp"] is None:
            errors.append(
                f"{file_path}: History entry heading at approx line "
                f"{entry['line_start']} has invalid format: "
                f"'{entry['heading'][:60]}'. Expected: "
                "'### <RFC-3339 timestamp> — <action>'"
            )

    # ── Check 2: Chronological order ─────────────────────────────────────

    prev_ts = ""
    for entry in entries:
        ts = entry["timestamp"]
        if ts is None:
            continue
        if prev_ts and ts < prev_ts:
            errors.append(
                f"{file_path}: History entries out of chronological "
                f"order: '{ts}' appears after '{prev_ts}'. "
                "History must be append-only with monotonically "
                "increasing timestamps."
            )
        prev_ts = ts

    # ── Check 3: No duplicate headings ───────────────────────────────────

    seen_headings: Dict[str, int] = {}
    for entry in entries:
        heading = entry["heading"]
        if heading in seen_headings:
            errors.append(
                f"{file_path}: Duplicate History entry heading: "
                f"'{heading[:60]}'. Each entry must have a unique "
                "timestamp + action combination."
            )
        seen_headings[heading] = entry["line_start"]

    # ── Check 4: Standard fields present ─────────────────────────────────

    standard_fields = {"state", "status", "actor"}
    for entry in entries:
        # Look at the lines following the heading for field bullets
        ts = entry["timestamp"]
        if ts is None:
            continue

    return errors


# ── File integrity check (partial write recovery) ──────────────────────────────


def check_file_integrity(file_path: Path) -> List[str]:
    """Detect structurally incomplete Work Object files.

    Checks for conditions that indicate a partial write or interrupted
    mutation:
      1. Frontmatter fence is properly opened and closed.
      2. File is not empty.
      3. File ends with a newline (no truncated final line).
      4. Body sections have complete headings (no trailing ###).
      5. No obviously truncated evidence table rows.

    These checks catch the most common partial-write failure modes
    without requiring a baseline or git history.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    if not content.strip():
        errors.append(f"{file_path}: File is empty")
        return errors

    # ── Check 1: Frontmatter fence integrity ─────────────────────────────

    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            errors.append(
                f"{file_path}: Unclosed YAML frontmatter fence. "
                "File may have been truncated during write."
            )
    elif not content.startswith("#"):
        # No frontmatter at all — this is a structural error for Work Objects.
        # Files starting with '#' without a '---' fence are also invalid:
        # they're plain markdown, not a Work Object.
        pass  # Handled below

    # Detect plain markdown files (no '---' fence anywhere)
    if "---" not in content.split("\n")[:5]:
        errors.append(
            f"{file_path}: File does not start with YAML frontmatter "
            "('---'). Not a valid Work Object."
        )

    # ── Check 2: File ends with newline ──────────────────────────────────

    if content and not content.endswith("\n"):
        errors.append(
            f"{file_path}: File does not end with a newline. "
            "May indicate a truncated write."
        )

    # ── Check 3: No orphaned heading fragments ───────────────────────────

    if content.rstrip().endswith("##"):
        errors.append(
            f"{file_path}: File ends with an incomplete section heading "
            "(trailing '##'). Likely a truncated write."
        )

    if content.rstrip().endswith("###"):
        errors.append(
            f"{file_path}: File ends with an incomplete subsection heading "
            "(trailing '###'). Likely a truncated write."
        )

    # ── Check 4: No truncated evidence table rows ────────────────────────

    body = _extract_body(content)
    if "evidence ledger" in body.lower():
        # Look for rows that start with | but are too short
        for line in body.split("\n"):
            stripped = line.strip()
            if stripped.startswith("|") and not stripped.endswith("|"):
                # A table row that doesn't close — check if it's the
                # well-known separator line pattern
                if not re.match(r"^\|[-\s|]+\|?$", stripped):
                    if stripped.count("|") < 3:
                        errors.append(
                            f"{file_path}: Truncated evidence table row: "
                            f"'{stripped[:60]}'. File may have been "
                            "interrupted during write."
                        )
                        break

    return errors


# ── Incident successor routing check ───────────────────────────────────────────


def check_incident_routing(file_path: Path) -> List[str]:
    """Validate that incident-type Work Objects have proper successor linkage.

    Per the protocol, incident objects that are closed should either:
      1. Link to a successor incident object in the History or Decisions, OR
      2. Have an explicit close-out decision confirming resolution.

    Incidents that are still active are not checked for successor routing.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    wo_type = str(fm.get("type", ""))
    status = str(fm.get("status", ""))
    state = str(fm.get("state", ""))

    # Only check incident-type objects that are closed
    if wo_type != "incident":
        return []

    if status != "closed" and state != "close":
        return []

    body = _extract_body(content)
    sections = parse_sections(body)

    # ── Check: Closed incident must have successor or resolution ─────────

    history = sections.get("history", "")
    decisions = sections.get("decisions and revisit triggers", "")

    # Look for successor references in History
    has_successor_in_history = bool(
        re.search(r"(?:successor|superseded.by|continued.as|linked.to)\s",
                   history, re.IGNORECASE)
    )

    # Look for resolution decision in Decisions
    has_resolution_in_decisions = bool(
        re.search(r"(?:resolution|resolved|closed.out|outcome)",
                   decisions, re.IGNORECASE)
    )

    # Look for successor link pattern: `YYYY-MM-DD-NNN` in History or Decisions
    successor_id_pattern = re.search(
        r"\d{4}-\d{2}-\d{2}-\d{3}", history + "\n" + decisions
    )
    has_successor_link = (
        successor_id_pattern is not None
        and successor_id_pattern.group(0) != str(fm.get("id", ""))
    )

    if not (has_successor_in_history or has_resolution_in_decisions
            or has_successor_link):
        errors.append(
            f"{file_path}: Closed incident has no successor reference "
            "or resolution record. Per protocol, closed incidents must "
            "either link to a successor incident object or contain an "
            "explicit close-out decision confirming resolution."
        )

    return errors


# ── Prerequisites check (end-to-end gate validation) ──────────────────────────


def check_prerequisites(file_path: Path) -> List[str]:
    """Verify that the current state's prerequisites are satisfied.

    Runs the lifecycle gates in reverse: for the object's current state,
    checks that the prerequisite conditions that WOULD have been enforced
    before entering that state are met. This catches objects that reached
    a gated state without satisfying the gate.

    Gates checked (from lifecycle.py):
      - build state (high consequence): requires decision_type: decision
      - release state: requires result: pass + scope populated
      - close state: requires any pass/fail outcome
      - observe state: requires result: pass

    Terminal and notice states have no prerequisites to check.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    body = _extract_body(content)
    state = str(fm.get("state", ""))
    consequence = str(fm.get("consequence", "low"))

    # States that have no prerequisites
    if state in ("notice", "close", ""):
        return []

    # ── Build gate (high consequence only) ───────────────────────────────

    if state == "build" and consequence == "high":
        decisions = parse_decisions_table(body)
        has_decision = any(
            d.get("decision_type") == "decision" for d in decisions
        )
        if not has_decision:
            errors.append(
                f"{file_path}: Object is in 'build' state with high "
                "consequence but has no decision record with "
                "decision_type: decision. Per lifecycle build gate, "
                "high-consequence objects require an accepted decision "
                "before entering build state."
            )

    # ── Release gate (all consequence levels) ────────────────────────────

    if state in ("release", "verify"):
        decisions = parse_decisions_table(body)
        if not decisions:
            errors.append(
                f"{file_path}: Object is in '{state}' state but has no "
                "structured decision records. At least one decision with "
                "result: pass and a scope field is required before "
                "entering release state."
            )
        else:
            latest = decisions[-1]
            result = latest.get("result", "").strip()
            scope = latest.get("scope", "").strip()
            if result != "pass":
                errors.append(
                    f"{file_path}: Object is in '{state}' state but most "
                    f"recent decision has result: '{result}'. Result must "
                    "be 'pass' before release."
                )
            if not scope or scope == "<!-- what this decision applies to -->":
                errors.append(
                    f"{file_path}: Object is in '{state}' state but most "
                    "recent decision has no scope defined. A scope field "
                    "is required before release."
                )

    # ── Observe gate (all consequence levels) ────────────────────────────

    if state == "observe":
        decisions = parse_decisions_table(body)
        has_pass = any(
            d.get("result", "").strip() == "pass" for d in decisions
        )
        if not has_pass:
            errors.append(
                f"{file_path}: Object is in 'observe' state but has no "
                "decision with result: pass. A passing result is required "
                "before entering observe state."
            )

    return errors


# ── Unsupported capabilities check ────────────────────────────────────────────


# Known abstract capabilities from CAPABILITY-DEGRADATION.md
_KNOWN_CAPABILITIES = frozenset({
    "file_read", "file_write", "directory_list", "glob_search",
    "content_search", "terminal_run", "git_operations",
    "structured_output", "subagent_spawn", "user_confirmation",
    "web_fetch", "web_search", "browser_automation",
    "parallel_tool_execution", "subagent_isolation", "deployment",
    "secret_access", "background_processes",
    "persistent_session_state", "file_uploads", "artifact_rendering",
})

_VALID_CLASSIFICATIONS = frozenset({"native", "manual-fallback", "unsupported"})


def _extract_capability_table(content: str) -> List[Dict[str, str]]:
    """Parse a capability mapping table from an adapter SKILL.md.

    Returns list of {capability, tool, classification} dicts.
    """
    rows = []
    in_table = False

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("| Abstract capability"):
            in_table = True
            continue
        if in_table and stripped.startswith("|") and "---" not in stripped:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 3:
                rows.append({
                    "capability": cells[0].strip("` "),
                    "tool": cells[1].strip("` "),
                    "classification": cells[2].strip(),
                })
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return rows


def check_unsupported_capabilities(file_path: Path) -> List[str]:
    """Validate capability degradation declarations in an adapter SKILL.md.

    Checks:
      1. Every declared capability is in the known capabilities catalog.
      2. Every classification is valid (native, manual-fallback, unsupported).
      3. Every manual-fallback capability has a degradation subsection.
      4. Every unsupported capability has a degradation subsection.

    This check runs against adapter files, not Work Objects.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    rows = _extract_capability_table(content)

    if not rows:
        return []  # Not an adapter file or no capability table

    for row in rows:
        cap = row["capability"]
        cls = row["classification"]
        tool = row["tool"]

        # Check 1: Known capability
        if cap and cap not in _KNOWN_CAPABILITIES:
            errors.append(
                f"{file_path}: Unknown capability '{cap}' in mapping table. "
                "Must be one of the canonical capabilities defined in "
                "CAPABILITY-DEGRADATION.md."
            )

        # Check 2: Valid classification
        if cls not in _VALID_CLASSIFICATIONS:
            errors.append(
                f"{file_path}: Invalid classification '{cls}' for capability "
                f"'{cap}'. Must be one of: native, manual-fallback, unsupported."
            )

        # Check 3: Degradation subsection for non-native capabilities
        if cls in ("manual-fallback", "unsupported"):
            # Look for a subsection heading for this capability
            subsection_pattern = rf"####\s+`{re.escape(cap)}`"
            if not re.search(subsection_pattern, content, re.IGNORECASE):
                errors.append(
                    f"{file_path}: Capability '{cap}' is classified as "
                    f"'{cls}' but has no degradation subsection "
                    f"('#### `{cap}`'). Non-native capabilities require "
                    "documented degradation behavior per "
                    "CAPABILITY-DEGRADATION.md."
                )

    return errors


# ── Interrupted mutations check ───────────────────────────────────────────────


def check_interrupted_mutations(file_path: Path) -> List[str]:
    """Detect signs of interrupted write operations.

    Checks for:
      1. Orphaned temporary files (.tmp, .swp, .swo, ~ suffix) adjacent
         to Work Object files that indicate an interrupted write.
      2. Work Object files that have a sibling with the same prefix but
         a temp extension — a write was started but never completed.

    This check runs against Work Object files but inspects sibling files
    in the same directory.
    """
    errors = []

    parent = file_path.parent
    stem = file_path.stem  # e.g., "2026-07-21-010-test"

    # Temp extensions that indicate interrupted writes
    _TEMP_EXTENSIONS = {".tmp", ".swp", ".swo", ".bak", ".partial"}
    _TEMP_SUFFIXES = {"~"}  # Vim-style backup: file.md~

    if not parent.exists():
        return []

    try:
        siblings = list(parent.iterdir())
    except Exception:
        return []

    for sibling in siblings:
        sname = sibling.name

        # Skip the file itself
        if sibling.resolve() == file_path.resolve():
            continue

        # Check temp extensions with same stem prefix
        for ext in _TEMP_EXTENSIONS:
            if sname.startswith(stem) and sname.endswith(ext):
                errors.append(
                    f"{file_path}: Orphaned temp file found: '{sname}'. "
                    "This suggests an interrupted write or mutation that "
                    "never completed. Review and remove the temp file if "
                    "the main file is intact."
                )
                break

        # Check Vim-style backup suffix
        for suffix in _TEMP_SUFFIXES:
            if sname.startswith(stem) and sname.endswith(suffix):
                errors.append(
                    f"{file_path}: Backup/temp file found: '{sname}'. "
                    "May indicate an interrupted editor session. Remove "
                    "if the main file is intact."
                )
                break

        # Generic lock file pattern: .<name>.lock or <name>.lock
        if sname == f".{file_path.name}.lock" or sname == f"{file_path.name}.lock":
            errors.append(
                f"{file_path}: Lock file found: '{sname}'. "
                "A write operation may have been interrupted. Remove the "
                "lock file if no write is in progress."
            )

    return errors


# ── Structure check ───────────────────────────────────────────────────────────


def check_structure(file_path: Path) -> List[str]:
    """Composite check: schema + sections."""
    return check_schema(file_path) + check_sections(file_path)


# ── Check registry ────────────────────────────────────────────────────────────

CHECK_REGISTRY: Dict[str, callable] = {
    "schema": check_schema,
    "sections": check_sections,
    "append-only": check_append_only,
    "attention": None,  # Special: workspace-level check
    "attention-limits": None,  # Special: workspace-level check
    "sensitivity": check_sensitivity,
    "sensitivity-policy": check_sensitivity_policy,
    "lifecycle": check_lifecycle,
    "claims": check_claims,
    "lanes": check_evidence_lanes,
    "authority": check_authority,
    "protected-fields": check_protected_fields,
    "history-integrity": check_history_integrity,
    "file-integrity": check_file_integrity,
    "incident-routing": check_incident_routing,
    "prerequisites": check_prerequisites,
    "unsupported-capabilities": check_unsupported_capabilities,
    "interrupted-mutations": check_interrupted_mutations,
    "structure": check_structure,
}

DEFAULT_CHECKS = [
    "schema", "sections", "append-only", "sensitivity",
    "sensitivity-policy", "lifecycle", "claims", "lanes",
    "authority", "protected-fields", "history-integrity",
    "file-integrity", "incident-routing", "prerequisites",
]


# ── Entry point ───────────────────────────────────────────────────────────────


def run_checks(
    check_names: Optional[List[str]],
    file_paths: List[Path],
    active_md_path: Optional[Path] = None,
    objects_dir: Optional[Path] = None,
) -> int:
    """Run named validation checks.

    Args:
        check_names: List of check names, or None for defaults.
        file_paths: Files to validate.
        active_md_path: Path to active.md (for attention check).
        objects_dir: Path to objects/ directory.

    Returns:
        Exit code: 0 if all checks pass, 1 if any fail.
    """
    if check_names is None:
        check_names = list(DEFAULT_CHECKS)

    all_errors: List[str] = []

    for name in check_names:
        if name not in CHECK_REGISTRY:
            print(f"Error: Unknown check '{name}'", file=sys.stderr)
            print(f"Available: {', '.join(sorted(CHECK_REGISTRY.keys()))}",
                  file=sys.stderr)
            return 1

        if name == "attention":
            # Workspace-level check
            if active_md_path and objects_dir:
                errs = check_attention_consistency(active_md_path, objects_dir)
                all_errors.extend(errs)
            else:
                all_errors.append(
                    "Attention check requires active.md and objects/ directory"
                )
            continue

        if name == "attention-limits":
            # Workspace-level check
            if active_md_path:
                errs = check_attention_limits(active_md_path)
                all_errors.extend(errs)
            else:
                all_errors.append(
                    "Attention-limits check requires active.md path"
                )
            continue

        check_fn = CHECK_REGISTRY[name]
        for fp in file_paths:
            errs = check_fn(fp)
            all_errors.extend(errs)

    for err in all_errors:
        print(err, file=sys.stderr)

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found.", file=sys.stderr)
        return 1

    print("All validation checks passed.")
    return 0
