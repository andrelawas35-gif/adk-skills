"""Composed validation checks for Work Objects.

Runs named validation checks against Work Object files or the full
workspace. Each check is independently invocable. With no args, runs
all checks against all objects.

Checks:
  schema                   — YAML frontmatter field validation
  sections                 — Required section presence and ordering
  append-only              — Snapshot-diff enforcement of History/Decisions/Evidence/Claims append-only
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
  contract-drift           — schema.py VALID_* enums vs __main__.py CLI choices
  outcome-review           — Advisory observe/close outcome-review coverage
  evidence-freshness       — Advisory [system] source locator resolution
  evidence-relations       — Advisory candidate supports/counters relations
  verification-freshness   — Advisory re-run of re-runnable verification commands
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .schema import (
    parse_frontmatter,
    validate_campaign,
    validate_consequence,
    validate_sensitivity,
    validate_state,
    validate_status,
    validate_type,
    VALID_TYPES,
    VALID_CONSEQUENCES,
    VALID_STATES,
    VALID_STATUSES,
    VALID_SENSITIVITIES,
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
from .dashboard_signals import (
    count_claims_below_support_adequacy,
    count_unresolved_conflicts,
)


# ── Schema check ──────────────────────────────────────────────────────────────


def check_schema(file_path: Path) -> List[str]:
    """Validate YAML frontmatter for a single Work Object.

    Checks: presence of required fields, enum membership, immutable
    field consistency.
    """
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
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
        ("sensitivity", validate_sensitivity, {"ordinary", "private", "restricted"}),
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

    if "campaign" in fm:
        err = validate_campaign(fm["campaign"])
        if err:
            errors.append(f"{file_path}: {err}")

    return errors


# ── Non-blocking plausibility warnings ────────────────────────────────────────


def _find_workspace_root(file_path: Path) -> Optional[Path]:
    """Return the workspace root containing a .work-studio object."""
    for parent in file_path.resolve().parents:
        if parent.name == ".work-studio":
            return parent.parent
    return None


def check_campaign_anchor(file_path: Path) -> List[str]:
    """Warn when a valid campaign field points to a missing design document."""
    try:
        content = file_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
    except (OSError, ValueError):
        return []

    campaign = fm.get("campaign")
    if campaign is None or validate_campaign(campaign):
        return []

    workspace_root = _find_workspace_root(file_path)
    if workspace_root is None:
        return []

    anchor = workspace_root / str(campaign)
    if anchor.is_file():
        return []
    return [
        f"{file_path}: campaign anchor '{campaign}' does not exist"
    ]


def check_consequence_plausibility(file_path: Path) -> List[str]:
    """Warn when explicit scope markers make a low consequence implausible."""
    try:
        content = file_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
    except (OSError, ValueError):
        return []

    if str(fm.get("consequence", "")) != "low":
        return []

    body = _extract_body(content)
    reasons: List[str] = []

    supersedes = fm.get("supersedes")
    if supersedes not in (None, "", "None", "none"):
        reasons.append("supersedes link")

    if re.search(
        r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?"
        r"(?:files touched|changed files)(?:\*\*)?\s*:",
        body,
    ):
        reasons.append("files touched")

    adr_action = re.compile(
        r"(?im)^.*(?:"
        r"(?:amend|update|modify|supersed)\w*.*\bADR[- ]?\d+"
        r"|\bADR[- ]?\d+.*(?:amend|update|modify|supersed)\w*"
        r").*$"
    )
    if adr_action.search(body):
        reasons.append("ADR amended")

    try:
        evidence = parse_sections(body).get("evidence ledger", "")
    except ValueError:
        evidence = ""
    if re.search(r"(?i)\bexternal[- ]effect\b", evidence):
        reasons.append("external effect")

    if not reasons:
        return []
    return [
        f"{file_path}: consequence 'low' may be implausible; "
        f"scope indicators: {', '.join(reasons)}"
    ]


# ── Retroactive cutoff ────────────────────────────────────────────────────────

# Objects created before the retrospective checks' requirements were
# introduced are excluded from those checks without being rewritten.
# Both check_prerequisites and check_history_integrity entered validate.py
# in commit 936b4af (2026-07-22); the Decisions template entered the same day
# in aa92aa6 (2026-08-10-005, Decisions 3-4).
RETROACTIVE_CUTOFF = "2026-07-22T00:00:00Z"


def _predates_cutoff(file_path: Path) -> bool:
    """Return True if the object's created_at predates RETROACTIVE_CUTOFF.

    Pre-cutoff objects are excluded from the retrospective checks (sections,
    history-integrity, prerequisites) without being rewritten. The comparison
    is a strict created_at < cutoff, so objects created exactly at the
    boundary remain evaluated on their own history.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return False
    fm = parse_frontmatter(content)
    created = str(fm.get("created_at", ""))
    return bool(created) and created < RETROACTIVE_CUTOFF


# ── Sections check ────────────────────────────────────────────────────────────


def check_sections(file_path: Path) -> List[str]:
    """Validate required section presence and ordering."""
    if _predates_cutoff(file_path):
        return []
    try:
        content = file_path.read_text(encoding="utf-8")
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

# Sections protected by the append-only rule (ADR 0017, 0022, 0024).
_APPEND_ONLY_SECTIONS = (
    "history",
    "decisions and revisit triggers",
    "evidence ledger",
    "claims",
)

# RFC-3339 whole-second timestamp base (uniqueness per section, ADR 0022).
_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

# History entry heading: ### <whole-second ts> — <action>.
_ENTRY_HEADING_RE = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")


def _find_snapshot(file_path: Path) -> Optional[Path]:
    """Return the most recent local snapshot (.bak-<ts>) sibling for an object.

    Work Objects live under .work-studio/objects/, which is Git-excluded by
    policy. The established baseline is a sibling ``.bak-<ts>`` snapshot taken
    before mutations (the same file used for rollback). Returns the most
    recent such snapshot, or None if the object has none.
    """
    siblings = sorted(file_path.parent.glob(file_path.name + ".bak-*"))
    return siblings[-1] if siblings else None


def _entry_timestamps(text: str, section: str) -> List[str]:
    """Return whole-second timestamps that identify entries in a section.

    Only timestamps that identify entries count for collision detection
    (ADR 0022 citation-uniqueness); timestamps appearing elsewhere in prose
    do not (per Decision 9):
      - History: the ``### <ts> —`` heading timestamp.
      - Decisions: entries are identified by ``### Decision N —`` headings,
        which carry no timestamp — no structural entry timestamps.
      - Evidence ledger / Claims: the first timestamp of an entry line
        (a table row or bullet), not timestamps deeper in prose.
    """
    lines = text.split("\n")
    if section == "history":
        out: List[str] = []
        for ln in lines:
            m = _ENTRY_HEADING_RE.match(ln)
            if m:
                out.append(m.group(1))
        return out
    if section == "decisions and revisit triggers":
        return []
    if section == "evidence ledger":
        # Entry rows are "| [tag] | source | entry |"; the entry-identifier
        # timestamp is at the start of the entry cell, not mid-prose.
        out = []
        for ln in lines:
            s = ln.strip()
            if s.startswith("|"):
                cells = s.strip("|").split("|")
                if len(cells) >= 3:
                    m = _TIMESTAMP_RE.match(cells[2].strip())
                    if m:
                        out.append(m.group(0))
        return out
    # Claims: bullets; the entry-identifier timestamp is at the start of the
    # bullet text.
    out = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("- ") or s.startswith("* "):
            m = _TIMESTAMP_RE.match(s[2:].strip())
            if m:
                out.append(m.group(0))
    return out


def check_append_only(file_path: Path) -> List[str]:
    """Check that append-only sections haven't lost content.

    Diffs each protected section (History, Decisions and revisit triggers,
    Evidence ledger, Claims) against the object's most recent local snapshot
    (a .bak-<ts> sibling) and fails if any existing entry's text changed or
    was removed. New appended entries pass. Also fails on duplicate
    whole-second timestamps within a section.

    A file with no snapshot baseline is surfaced by ``check_append_only_baseline``
    as an explicit, non-blocking warning; it is never a silent pass.
    """
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
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
        # Skip heading and table header (first 3 lines).
        # Track HTML comment blocks (the ws create template embeds a
        # `<!-- Tagged evidence entries... -->` comment in the ledger); the
        # comment opener can be inside the first 3 lines, so detect it before
        # the header skip.
        in_comment = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if "<!--" in stripped:
                in_comment = True
            if in_comment:
                if "-->" in stripped:
                    in_comment = False
                continue
            if i < 3:
                continue
            if stripped and not stripped.startswith("|"):
                errors.append(
                    f"{file_path}: Evidence ledger line {i+1} does not follow table format"
                )

    # ── Snapshot diff: existing entries must be a prefix (append-only) ─────
    snapshot = _find_snapshot(file_path)
    if snapshot is not None:
        try:
            snap_sections = parse_sections(_extract_body(snapshot.read_text(encoding="utf-8")))
        except Exception as e:
            errors.append(f"{file_path}: Cannot parse snapshot {snapshot.name}: {e}")
            snap_sections = {}
        for sec in _APPEND_ONLY_SECTIONS:
            if sec not in snap_sections:
                continue
            # Trailing blank lines are not append-only content: a legitimate
            # append via append_to_section drops the blank line after a
            # non-terminal section, so the post-append section lacks the
            # trailing newline the snapshot's section retains. Strip trailing
            # empty lines from both sides before comparing (WO 2026-08-17-004
            # Decision 1; incident 2026-08-17-002).
            snap_lines = [l.rstrip() for l in snap_sections[sec].split("\n")]
            cur_lines = [l.rstrip() for l in sections.get(sec, "").split("\n")]
            while snap_lines and snap_lines[-1] == "":
                snap_lines.pop()
            while cur_lines and cur_lines[-1] == "":
                cur_lines.pop()
            if len(cur_lines) < len(snap_lines) or cur_lines[:len(snap_lines)] != snap_lines:
                errors.append(
                    f"{file_path}: append-only violation in section "
                    f"'{sec}': an existing entry was edited or removed "
                    f"(diff vs snapshot {snapshot.name})"
                )
    # No snapshot: append-only cannot be diffed; check_append_only_baseline
    # surfaces that as an explicit, non-blocking warning.

    # ── Whole-second entry-timestamp uniqueness per section (ADR 0022) ─────
    # Only timestamps that identify entries collide (Decision 9); prose
    # date-time strings are not entry timestamps.
    for sec in _APPEND_ONLY_SECTIONS:
        if sec not in sections:
            continue
        seen: Dict[str, bool] = {}
        for base in _entry_timestamps(sections[sec], sec):
            if base in seen:
                errors.append(
                    f"{file_path}: duplicate whole-second timestamp "
                    f"'{base}' in section '{sec}'"
                )
                break  # one report per section is enough
            seen[base] = True

    return errors


def check_append_only_baseline(file_path: Path) -> List[str]:
    """Advisory warning: object has no snapshot baseline for append-only diffing.

    Append-only cannot be verified for an object without a .bak-<ts> snapshot.
    Surfaced explicitly (never a silent pass) but non-blocking, per the
    accepted wiring; making it blocking is a later decision (open question 2).
    """
    if _find_snapshot(file_path) is None:
        return [
            f"{file_path}: no baseline snapshot (.bak-*) found; "
            "append-only is not verifiable for this object"
        ]
    return []


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
        content = file_path.read_text(encoding="utf-8")
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


# ── Evidence freshness check ─────────────────────────────────────────────────

_LOCAL_LOCATOR_RE = re.compile(
    r"^`?(?P<path>[^`\s|:][^`\s|]*):(?P<start>\d+)"
    r"(?:[-–](?P<end>\d+))?`?$"
)


def _parse_evidence_table_cells(raw: str) -> Optional[List[str]]:
    """Return table cells for a simple evidence row, or None if not a row."""
    stripped = raw.strip()
    if not stripped.startswith("|") or _is_table_header(stripped):
        return None
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return cells if len(cells) >= 3 else None


def _parse_local_locator(source: str) -> Optional[Tuple[Path, int, int]]:
    """Parse an exact local ``path:line`` or ``path:start-end`` source."""
    match = _LOCAL_LOCATOR_RE.match(source.strip())
    if not match:
        return None
    start = int(match.group("start"))
    end = int(match.group("end") or start)
    if start < 1 or end < start:
        return None
    return Path(match.group("path")), start, end


# One fixed disclosure appended whenever this check has findings to report.
# It names the check's reach boundary (Direction 3 fallback, WO 2026-08-10-011
# Decision 2): fan-out below only ever matches an exact path:line citation, so
# dependencies expressed as prose conditions are never covered by any
# mechanism here — they stay a human re-read.
_FRESHNESS_COVERAGE_NOTE = (
    "evidence-freshness: reaches only exact-citation matches; prose-condition "
    "dependencies are not covered — re-read them by hand when a related "
    "correction lands."
)


def _system_locators(
    file_paths: List[Path],
) -> List[Tuple[Path, int, str, Tuple[Path, int, int]]]:
    """Collect every [system] row with a parseable local locator.

    Returns one tuple per row: (object file, evidence-line number within its
    ledger, raw source text, parsed (rel_path, start, end) locator). Used both
    to test resolution and, for a moved citation, to fan out to co-citers.
    """
    rows: List[Tuple[Path, int, str, Tuple[Path, int, int]]] = []
    for obj_file in sorted(file_paths):
        try:
            content = obj_file.read_text(encoding="utf-8")
        except Exception:
            continue

        body = _extract_body(content)
        sections = parse_sections(body)
        evidence = sections.get("evidence ledger", "")
        if not evidence:
            continue

        for line_num, line in enumerate(evidence.split("\n"), start=1):
            cells = _parse_evidence_table_cells(line)
            if cells is None:
                continue

            tag = cells[0].strip("`")
            if tag != "[system]":
                continue

            source = cells[1].strip()
            locator = _parse_local_locator(source)
            if locator is None:
                continue

            rows.append((obj_file, line_num, source, locator))

    return rows


def check_evidence_freshness(
    file_paths: List[Path],
    objects_dir: Optional[Path] = None,
) -> List[str]:
    """Advisory read-time check for stale local [system] source locators.

    This check is intentionally mechanical. It only evaluates exact local
    ``path:line`` and ``path:start-end`` sources on ``[system]`` evidence rows.
    Non-locator and ambiguous sources are skipped; other evidence tags are out
    of scope. A finding means "citation moved — re-read", not "claim false".

    Canonical root (WO 2026-08-14-006 Decision 1): every relative locator is
    resolved against the repository root — the parent of ``.work-studio/``,
    computed below as ``objects_dir.parent.parent`` — never against
    ``.work-studio/`` itself or the citing object's own directory. A citation
    missing a leading path segment (e.g. ``inbox.md`` instead of
    ``.work-studio/inbox.md``) is an incomplete citation, not evidence that a
    different root is intended.

    When a citation is flagged moved, this also fans the flag out to every
    other object citing the identical pre-move locator (WO 2026-08-10-011,
    Direction 4): a shared exact path:line citation predicts genuine
    dependency, so a co-citer is surfaced as "possibly affected" whether or
    not it named the dependency itself. The join is exact-match only — no
    bare-filename matching, no fuzzy matching — matching the flood risk
    already ruled out for this mechanism.
    """
    if objects_dir is None:
        return ["evidence-freshness check requires the objects/ directory path"]

    ws_root = objects_dir.parent.parent
    rows = _system_locators(file_paths)
    warnings: List[str] = []

    for obj_file, line_num, source, (rel_path, start, end) in rows:
        target = rel_path if rel_path.is_absolute() else ws_root / rel_path

        if not target.exists() or not target.is_file():
            reason = "file not found"
        else:
            try:
                line_count = len(target.read_text(encoding="utf-8").splitlines())
            except Exception as exc:
                reason = f"cannot read source: {exc}"
            else:
                reason = (
                    f"line out of range; file has {line_count} line(s)"
                    if end > line_count
                    else None
                )

        if reason is None:
            continue

        warnings.append(
            f"evidence-freshness: {obj_file}: Evidence ledger line "
            f"{line_num}: citation moved — re-read: {source} ({reason})"
        )

        for other_file, other_line, other_source, other_locator in rows:
            if (other_file, other_line) == (obj_file, line_num):
                continue
            if other_locator != (rel_path, start, end):
                continue
            warnings.append(
                f"evidence-freshness: {obj_file}: Evidence ledger line "
                f"{line_num}: citation moved — re-read: {source} "
                f"— possibly affected: {other_file} (shares this citation "
                f"at Evidence ledger line {other_line})"
            )

    if warnings:
        warnings.append(_FRESHNESS_COVERAGE_NOTE)

    return warnings


# One fixed disclosure appended whenever this check has findings to report.
# Names the check's reach boundary (WO 2026-08-11-008 Decision 2, narrowed
# from the tracer-bullet test, then broadened from exact-range to file-level
# per director confirmation 2026-08-14): same-file citation overlap only, not
# exact line-range overlap. Keyword matching was tested (802 candidates
# against 34) and found to be almost entirely noise, so it is deliberately
# not part of this mechanism. File-level matching itself is known to include
# some false positives from generically-cited files (e.g. README.md,
# AGREEMENT-LOOP.md) — the tracer-bullet test measured ~70% precision (24/34
# hand-checked candidates genuinely related), not 100%.
_RELATIONS_COVERAGE_NOTE = (
    "evidence-relations: surfaces candidates only, from same-file citation "
    "overlap between [system] rows in different objects — confirm each by "
    "hand; a shared citation is not itself proof of support or contradiction, "
    "and citing the same file is not always a real relationship."
)


def check_evidence_relations(
    file_paths: List[Path],
    objects_dir: Optional[Path] = None,
) -> List[str]:
    """Advisory read-time candidate supports/counters relation surfacing.

    Groups [system] evidence rows across different objects that cite the
    same local file (any line), and surfaces each cross-object pair as a
    candidate relation for human confirmation. No new field is written and
    no relation is stored — WO 2026-08-11-008 Decision 2 narrowed the
    mechanism to citation overlap only, after a tracer-bullet test found
    keyword matching (e.g. "contradicts", "confirms" anywhere in entry text)
    surfaced almost entirely noise. Matching is file-level, not exact-range:
    the tracer-bullet test that set Decision 2's ~70% precision expectation
    measured file-level overlap, not the stricter exact path:line/range
    matching `check_evidence_freshness` uses to avoid bare-filename flood
    risk. This reuses the same locator extraction as `check_evidence_freshness`
    but groups by file only.
    """
    if objects_dir is None:
        return ["evidence-relations check requires the objects/ directory path"]

    rows = _system_locators(file_paths)
    by_file: Dict[Path, List[Tuple[Path, int, str]]] = {}
    for obj_file, line_num, source, locator in rows:
        rel_path, _start, _end = locator
        by_file.setdefault(rel_path, []).append((obj_file, line_num, source))

    warnings: List[str] = []
    for rel_path, citers in by_file.items():
        distinct_objects = {obj_file for obj_file, _, _ in citers}
        if len(distinct_objects) < 2:
            continue

        for i in range(len(citers)):
            for j in range(i + 1, len(citers)):
                obj_i, line_i, _ = citers[i]
                obj_j, line_j, _ = citers[j]
                if obj_i == obj_j:
                    continue
                warnings.append(
                    f"evidence-relations: candidate relation — {obj_i} "
                    f"(Evidence ledger line {line_i}) and {obj_j} (Evidence "
                    f"ledger line {line_j}) both cite {rel_path}"
                )

    if warnings:
        warnings.append(_RELATIONS_COVERAGE_NOTE)

    return warnings


# One fixed disclosure appended whenever this check has findings to report.
# Names the check's reach boundary (WO 2026-08-11-012 Decision 1, refined by
# Decision 2): only bullets containing a single backtick-delimited command
# starting with a known executable prefix are re-run. Real-corpus sampling
# found this covers ~26% of real Verification and release evidence bullets;
# judgment-based, narrative, and decision/constraint-boundary claims are not
# covered and are not claimed to be. No stable ID, no version binding -- the
# check re-runs the claim itself rather than binding to what version it
# originally verified.
_VERIFICATION_COVERAGE_NOTE = (
    "verification-freshness: only re-runs bullets with a single "
    "backtick-delimited command starting with a known executable prefix "
    "-- narrative and judgment-based verification claims are not covered."
)

# Extensible allow-list of recognized command prefixes (WO 2026-08-11-012
# Decision 2): a bare backtick span is not enough -- the real corpus produced
# a false positive (a skill name in backticks, not a command) under a rule
# that accepted any backtick content.
_VERIFICATION_CMD_PREFIXES = ("python3", "python", "sh", "bash", "git", "pytest")

_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _extract_verifiable_commands(body: str) -> List[Tuple[int, str]]:
    """Extract (bullet index, command) pairs from Verification bullets.

    Only a bullet whose backtick-delimited span starts with a recognized
    executable prefix is treated as a command; other backtick spans (e.g. a
    skill name mentioned in prose) are ignored.
    """
    sections = parse_sections(body)
    section = sections.get("verification and release evidence", "")
    if not section:
        return []

    bullets = re.split(r"\n(?=- )", section)
    commands = []
    for idx, bullet in enumerate(bullets):
        joined = re.sub(r"\s+", " ", bullet).strip()
        if not joined:
            continue
        for m in _BACKTICK_RE.finditer(joined):
            candidate = m.group(1).strip()
            first_token = candidate.split(" ", 1)[0] if candidate else ""
            if first_token in _VERIFICATION_CMD_PREFIXES:
                commands.append((idx, candidate))

    return commands


def check_verification_freshness(
    file_paths: List[Path],
    objects_dir: Optional[Path] = None,
) -> List[str]:
    """Advisory read-time re-check of re-runnable verification commands.

    For each `## Verification and release evidence` bullet containing a
    single backtick-delimited command with a recognized executable prefix,
    re-runs the command from the workspace root and reports whether it still
    passes. Does not bind to a version of anything -- WO 2026-08-11-012
    Decision 1 chose this over a stable-ID scheme because real Verification
    bullets overwhelmingly don't cite a resolvable locator (0/19 in the
    corpus sample), while a meaningful minority (5/19, refined to require an
    executable prefix per Decision 2) are directly re-runnable commands.
    """
    if objects_dir is None:
        return ["verification-freshness check requires the objects/ directory path"]

    ws_root = objects_dir.parent.parent
    warnings: List[str] = []

    for obj_file in sorted(file_paths):
        try:
            content = obj_file.read_text(encoding="utf-8")
        except Exception:
            continue

        body = _extract_body(content)
        commands = _extract_verifiable_commands(body)

        for idx, command in commands:
            try:
                result = subprocess.run(
                    command, shell=True, cwd=ws_root,
                    capture_output=True, text=True, timeout=120,
                )
            except (subprocess.SubprocessError, OSError) as exc:
                warnings.append(
                    f"verification-freshness: {obj_file}: bullet {idx}: "
                    f"could not execute `{command}`: {exc}"
                )
                continue

            if result.returncode != 0:
                warnings.append(
                    f"verification-freshness: {obj_file}: bullet {idx}: "
                    f"`{command}` no longer passes (exit {result.returncode})"
                )

    if warnings:
        warnings.append(_VERIFICATION_COVERAGE_NOTE)

    return warnings


# ── Sensitivity check ─────────────────────────────────────────────────────────


def check_sensitivity(file_path: Path) -> List[str]:
    """Check that restricted-content objects use pointers, not inline body.

    Per ADR 0019: restricted sensitivity objects should not contain
    restricted content directly in the body.
    """
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
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
        content = file_path.read_text(encoding="utf-8")
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
        content = file_path.read_text(encoding="utf-8")
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

# Optional fields recognized as part of the Authority record shape (Decision 2,
# Branch C normalization). These extend the shipped five-field contract with
# the doc's `subject` and `expiry/revocation` concepts. They are OPTIONAL:
# existing entries without them remain valid (no silent rewrite), so they are
# NOT part of _AUTHORITY_REQUIRED_FIELDS.
_AUTHORITY_OPTIONAL_FIELDS = [
    "subject",
    "expiry",
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
        content = file_path.read_text(encoding="utf-8")
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


# One fixed comment on the mechanism's reach (WO 2026-08-11-009 Decision 1):
# reuse only fires on an exact (Decision N, object-id) citation already
# present in the new entry's action text. An Authority entry without that
# citation always mints a new AUTH-* id -- no reuse, no failure, and no
# agent-composed judgment call. The false-collapse risk (two distinct grants
# citing the same Decision-N/object-id pair) is untested against real data
# and is not mitigated by this mechanism.
_AUTH_DECISION_REF_RE = re.compile(r"\(Decision\s+(\d+),\s*([\w-]+)\)")
_AUTH_ID_RE = re.compile(r"\bAUTH-(\d+)\b")


def _extract_decision_reference(text: str) -> Optional[Tuple[str, str]]:
    """Extract a `(Decision N, object-id)` citation from entry text, if present."""
    m = _AUTH_DECISION_REF_RE.search(text)
    if m is None:
        return None
    return (m.group(1), m.group(2))


def mint_or_reuse_auth_id(action: str, objects_dir: Path) -> str:
    """Compute the AUTH-* id for a new Authority History entry.

    Reuses an existing AUTH-* id when the new entry's action text carries a
    `(Decision N, object-id)` citation that matches an existing Authority
    entry elsewhere in the corpus (WO 2026-08-11-009 Decision 1, refined
    from exact-heading-text matching after that mechanism was tested and
    found to split one real 11-object grant into 3 groups). Otherwise mints
    the next sequential AUTH-<n> id.
    """
    new_ref = _extract_decision_reference(action)

    max_seq = 0
    for obj_file in sorted(objects_dir.rglob("*.md")):
        try:
            content = obj_file.read_text(encoding="utf-8")
        except Exception:
            continue
        body = _extract_body(content)
        for entry in _parse_history_entries(body):
            if not _is_authority_entry(entry):
                continue
            heading = entry.get("_heading", "")
            id_match = _AUTH_ID_RE.search(heading)
            if id_match:
                max_seq = max(max_seq, int(id_match.group(1)))
            if new_ref is not None and new_ref == _extract_decision_reference(heading):
                if id_match:
                    return f"AUTH-{id_match.group(1)}"

    return f"AUTH-{max_seq + 1:03d}"


# ── Attention-register limits check ────────────────────────────────────────────


def check_attention_limits(
    active_md_path: Path,
    _file_paths: Optional[List[Path]] = None,
) -> List[str]:
    """Enforce attention register quantitative limits.

    Per ADR 0018: at most one Primary Work Object. Supporting and total
    active entries have no numeric cap -- active.md is an advisory
    attention view, not a concurrency constraint.

    This is a workspace-level check (takes active_md_path, not a Work
    Object path). The runner passes file_paths as a second argument for
    compatibility with the check registry dispatch convention.
    """
    errors = []

    if not active_md_path or not active_md_path.exists():
        return []  # No register, nothing to enforce

    try:
        content = active_md_path.read_text(encoding="utf-8")
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


def _ts_instant(value: str) -> Optional[datetime]:
    """Parse an RFC-3339 timestamp into a timezone-aware instant.

    Returns None if the value is not parseable. ``datetime.fromisoformat``
    in Python 3.8 does not accept the ``Z`` suffix, so it is normalized to
    ``+00:00`` before parsing.
    """
    try:
        normalized = value.replace("Z", "+00:00") if value.endswith("Z") else value
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


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
        content = file_path.read_text(encoding="utf-8")
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

    # Compare as instants, not strings: mixed timezone offsets such as
    # created 2026-07-15T20:43:15+08:00 (=12:43:15Z) vs updated 12:49:10Z are
    # chronological but lexically inverted. String comparison would be a
    # false positive; instant comparison is the true chronological check.
    created_ts = _ts_instant(created) if created else None
    updated_ts = _ts_instant(updated) if updated else None
    if created_ts is not None and updated_ts is not None and created_ts > updated_ts:
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
        content = file_path.read_text(encoding="utf-8")
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

    True append-only enforcement (no edits to past entries) is handled by the
    append-only check's local-snapshot diff (ws validate append-only). This
    check provides structural validation of History format and order.
    """
    if _predates_cutoff(file_path):
        return []
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
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
        content = file_path.read_text(encoding="utf-8")
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
        content = file_path.read_text(encoding="utf-8")
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
    if _predates_cutoff(file_path):
        return []
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
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
        content = file_path.read_text(encoding="utf-8")
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


def check_dashboard_signals(
    objects_dir: Optional[Path] = None,
) -> Tuple[List[str], List[str]]:
    """Workspace-level advisory check relaying the epistemic-pressure signals.

    Returns ``(warnings, errors)``:
    - ``warnings`` carries each non-zero gauge count (unresolved conflicts,
      claims below support adequacy) so the numbers surface where ``ws
      validate`` already runs. Advisory only — never changes the exit code.
    - ``errors`` carries a fail-closed message when a reader hits a malformed
      ``CONF-``/``CLM-`` heading, matching the readers' ValueError contract.

    The counts are computed by the readers in ``dashboard_signals.py`` (single
    computation source); this check only relays them and does not reimplement
    either count.
    """
    warnings: List[str] = []
    if objects_dir is None or not objects_dir.is_dir():
        return warnings, []
    try:
        conflicts = count_unresolved_conflicts(objects_dir)
        below = count_claims_below_support_adequacy(objects_dir)
    except ValueError as e:
        return warnings, [str(e)]
    if conflicts:
        warnings.append(
            f"epistemic-pressure: {conflicts} unresolved conflict(s) on record"
        )
    if below:
        warnings.append(
            f"epistemic-pressure: {below} claim(s) below support adequacy"
        )
    return warnings, []


# ── Component ledger check ────────────────────────────────────────────────────


_LEDGER_FILENAME = "component-ledger.md"
_LEDGER_NOT_YET_GRILLED = "not-yet-grilled"


def _parse_component_ledger(
    ledger_text: str,
) -> List[Dict[str, str]]:
    """Parse the component ledger Markdown into per-component records.

    Each ``## COMP-NNN — <name>`` section yields a record with the fields
    the ledger's entry schema declares: status, location(s), depends-on,
    depended-on-by, and last-grilled-SHA. Unknown or absent fields are
    empty strings so the caller can classify them explicitly.
    """
    records: List[Dict[str, str]] = []
    for block in re.split(r"\n(?=## COMP-\d+ )", ledger_text):
        header = re.match(r"## (COMP-\d+) — .+", block)
        if not header:
            continue
        cid = header.group(1)
        rec: Dict[str, str] = {"id": cid}
        for key in ("status", "location(s)", "depends-on", "depended-on-by",
                    "last-grilled-SHA"):
            m = re.search(
                r"- \*\*" + re.escape(key) + r":\*\*\s*(.*)", block
            )
            rec[key] = m.group(1).strip() if m else ""
        records.append(rec)
    return records


def _expand_comp_list(value: str) -> List[str]:
    """Expand a declared edge value into concrete COMP-NNN ids.

    Handles ``COMP-002 through COMP-013`` shorthand by expanding against the
    live component ids, plus comma-separated lists and single ids. The
    ``through`` form is expanded to the inclusive numeric range, so a range
    that no longer covers every actual dependent is reported rather than
    silently accepted (Decision 2, tracer bullet).
    """
    ids: List[str] = []
    if not value or value.lower().startswith("none"):
        return ids

    # Expand each ``COMP-A through COMP-B`` run to its inclusive numeric range.
    def _expand_range(m: "re.Match") -> str:
        a = int(m.group(1))
        b = int(m.group(2))
        lo, hi = min(a, b), max(a, b)
        return " ".join(f"COMP-{i:03d}" for i in range(lo, hi + 1))

    expanded = re.sub(r"COMP-(\d+) through COMP-(\d+)", _expand_range, value)
    for cid in re.findall(r"COMP-\d{3}", expanded):
        if cid not in ids:
            ids.append(cid)
    return ids


def _git_commits_since(sha: str, path: str, cwd: Path) -> Optional[int]:
    """Count commits touching ``path`` after ``sha`` in the repo at ``cwd``.

    Returns None when git is unavailable or the query fails, so the caller
    can record the drift as unverified rather than assert no drift.
    """
    try:
        proc = subprocess.run(
            ["git", "rev-list", "--count", f"{sha}..HEAD", "--", path],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
    except (OSError, ValueError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return int(proc.stdout.strip())
    except ValueError:
        return None


def check_ledger(objects_dir: Optional[Path] = None) -> List[str]:
    """Workspace-level check over the component ledger (ADR 0014).

    Read-only and advisory (not in DEFAULT_CHECKS). Reports three defect
    classes as error strings:

    1. Reciprocity (Decision 1, Branch C): every ``depends-on: COMP-X`` in an
       active/settled COMP-N is reported unless active/settled COMP-X's
       ``depended-on-by`` names COMP-N. Retired components are exempt in both
       directions — ``none (downstream deps also deferred)`` is a valid
       terminal state.
    2. Range shorthand (Decision 2): ``COMP-A through COMP-B`` is expanded
       against the live component list, so a range that no longer covers all
       dependents is reported rather than silently accepted.
    3. Grill staleness: a component with a real ``last-grilled-SHA`` whose
       declared ``location(s)`` have commits after that SHA is reported, per
       the ledger's auto-reopen clause. ``not-yet-grilled`` is never reported
       stale.

    The ledger is the canonical artifact owned by ``track-components``; this
    check only reads it and never repairs edges or updates the ledger.
    """
    if objects_dir is None or not objects_dir.is_dir():
        return ["ledger check requires the objects/ directory path"]

    ledger_path = objects_dir.parent / _LEDGER_FILENAME
    if not ledger_path.is_file():
        return [f"ledger check: {_LEDGER_FILENAME} not found at {ledger_path}"]

    records = _parse_component_ledger(ledger_path.read_text(encoding="utf-8"))
    live_ids = [r["id"] for r in records]
    by_id = {r["id"]: r for r in records}

    errors: List[str] = []

    # Precompute each component's forward (depends-on) and reverse
    # (depended-on-by) sets, keeping the raw reverse text for classification.
    forward = {r["id"]: _expand_comp_list(r["depends-on"]) for r in records}
    reverse = {r["id"]: _expand_comp_list(r["depended-on-by"]) for r in records}
    reverse_raw = {r["id"]: r["depended-on-by"] for r in records}

    # 1) Reciprocity + 2) range shorthand (Branch C: retired exempt both ways).
    for src in live_ids:
        src_status = by_id[src]["status"].strip().lower()
        if src_status == "retired":
            continue
        for tgt in forward[src]:
            if tgt not in by_id:
                continue
            tgt_status = by_id[tgt]["status"].strip().lower()
            if tgt_status == "retired":
                continue
            if src in reverse[tgt]:
                continue
            if "through" in reverse_raw[tgt]:
                errors.append(
                    f"ledger range-shorthand: {src} depends-on {tgt} but "
                    f"{tgt}'s depended-on-by range does not include {src}"
                )
            else:
                errors.append(
                    f"ledger plain omission: {src} depends-on {tgt} but "
                    f"{tgt}'s depended-on-by does not include {src}"
                )

    # 3) Grill staleness: only components with a real SHA are eligible;
    #    not-yet-grilled is never stale. Locations are backtick-quoted paths.
    ws_root = objects_dir.parent.parent
    for cid, rec in by_id.items():
        sha = rec["last-grilled-SHA"].strip().strip("`")
        if not sha or sha == _LEDGER_NOT_YET_GRILLED:
            continue
        locations = [
            t.strip("`")
            for t in re.findall(r"`[^`]+`", rec["location(s)"])
            if "/" in t and "." in t.split("/")[-1]
        ]
        stale = False
        for loc in locations:
            count = _git_commits_since(sha, loc, ws_root)
            if count is None:
                errors.append(
                    f"ledger staleness unverified: {cid} git query failed "
                    f"for {loc} — do not assert no drift"
                )
            elif count > 0:
                stale = True
                break
        if stale:
            errors.append(
                f"ledger grill staleness: {cid} last-grilled-SHA {sha} is "
                f"behind HEAD on its declared location(s)"
            )

    return errors


# ── Outcome-review coverage check ────────────────────────────────────────────


# Markers that indicate an object at observe/close has an outcome review
# recorded in its body. Matched case-insensitively.
#
# Precision rule (deviation accepted 2026-08-10, WO 2026-08-10-002): a routing
# mention such as "Route to `alawas-review-outcome-and-adapt` for outcome
# review" or "Transition ... for outcome review" is a plan to review, not
# evidence a review happened. Only real review evidence counts. The corpus
# records reviews in four formats, so classification is structural and
# phrasing-based rather than a bare keyword scan:
#
#   1. an ``## Outcome``/``## Outcome review`` section heading;
#   2. a History heading (``### timestamp — ...``) that records a review
#      outcome (confirmed / complete / recorded / accepted / checkpoint /
#      "Outcome review:"), not a routing transition;
#   3. a History bullet (``- **timestamp** — ...``) that records a review
#      outcome, not a routing/readiness mention; or
#   4. an Evidence-ledger row whose source is ``review-outcome-and-adapt`` or
#      an outcome review.
_OUTCOME_REVIEW_MARKERS = (
    "review-outcome-and-adapt",
    "## outcome",
    "outcome review",
)
# Phrases that record a performed review (as opposed to routing toward one).
_REVIEW_PERFORMED_PATTERNS = (
    r"outcome review\s*:",
    r"outcome review\s+confirmed",
    r"outcome review\s+complete",
    r"outcome review\s+recorded",
    r"outcome review\s+accepted",
    r"outcome review\s+checkpoint",
    r"outcome review\s+direction",
)
# Phrases that name the review as a future route rather than a performed act.
_REVIEW_ROUTING_PATTERNS = (
    r"for outcome review",
    r"to\s+`?review-outcome-and-adapt",
    r"rout(ing|ed)?\s+.*outcome review",
    r"ready for outcome review",
    r"transition.*for outcome review",
)


def _has_real_outcome_review(body: str) -> bool:
    """True when ``body`` carries real review evidence, not a routing mention.

    Routing instructions name the review as a *future* route ("Route to
    ``alawas-review-outcome-and-adapt`` for outcome review", "Transition ...
    for outcome review"); they are not evidence a review happened. Real
    evidence is structural and phrasing-based (see the module comment above):
    an ``## Outcome`` section, a History heading or bullet that records a
    review outcome, or an Evidence-ledger row whose source is the review skill.
    """
    lower = body.lower()
    if re.search(r"^## (outcome|outcome review)\s*$", lower, re.M):
        return True
    # History headings and bullets that record a review outcome.
    for line in re.finditer(r"^(?:#{3,}|- \*\*).*$", lower, re.M):
        text = line.group(0)
        if "outcome review" not in text:
            continue
        if any(re.search(p, text) for p in _REVIEW_ROUTING_PATTERNS):
            continue
        if any(re.search(p, text) for p in _REVIEW_PERFORMED_PATTERNS):
            return True
    # Evidence-ledger row whose source is the review skill / an outcome review.
    if re.search(
        r"\| \[(decision|inference|system|testimony|memory)\] \| "
        r"[^|]*?(review-outcome-and-adapt|outcome review)",
        lower,
    ):
        return True
    return False


def check_outcome_review(objects_dir: Optional[Path] = None) -> List[str]:
    """Workspace-level advisory check over outcome-review coverage (WO 2026-08-10-002).

    Read-only and advisory (not in DEFAULT_CHECKS). Scans every Work Object at
    ``state: observe`` or ``state: close`` and classifies each as reviewed or
    unreviewed from real review evidence in the object body: an ``## Outcome``/
    ``## Outcome review`` section heading, a History entry heading recording an
    outcome review, or an Evidence-ledger row whose source is the review skill
    (precision rule accepted 2026-08-10; routing mentions never count). Objects
    without such evidence are reported, per cohort by ``YYYY-MM`` of
    ``created_at``, with their IDs.

    Mirrors the provenance linter's mechanism: the number moves when a machine
    checks it. This check makes the flat outcome-review rate measurable.
    """
    if objects_dir is None or not objects_dir.is_dir():
        return ["outcome-review check requires the objects/ directory path"]

    # Collect per-cohort counts and the unreviewed IDs per cohort.
    cohorts: Dict[str, List[str]] = {}
    for year_dir in sorted(objects_dir.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for obj_file in sorted(month_dir.iterdir()):
                if obj_file.suffix != ".md":
                    continue
                try:
                    content = obj_file.read_text(encoding="utf-8")
                except Exception:
                    continue
                fm = parse_frontmatter(content)
                state = str(fm.get("state", "")).strip()
                if state not in ("observe", "close"):
                    continue
                created = str(fm.get("created_at", "")).strip()
                cohort = created[:7] if created else "unknown"
                body = _extract_body(content)
                reviewed = _has_real_outcome_review(body)
                if not reviewed:
                    cohorts.setdefault(cohort, []).append(obj_file.stem)

    errors: List[str] = []
    for cohort in sorted(cohorts):
        ids = cohorts[cohort]
        errors.append(
            f"outcome-review: cohort {cohort}: {len(ids)} of "
            f"{_cohort_total(objects_dir, cohort)} object(s) at observe/close "
            f"lack a recorded outcome review"
        )
        for obj_id in ids:
            errors.append(f"outcome-review: {obj_id}: no outcome review recorded")

    return errors


def _cohort_total(objects_dir: Path, cohort: str) -> int:
    """Count Work Objects at observe/close whose created_at falls in ``cohort``."""
    total = 0
    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if obj_file.suffix != ".md":
                    continue
                try:
                    content = obj_file.read_text(encoding="utf-8")
                except Exception:
                    continue
                fm = parse_frontmatter(content)
                if str(fm.get("state", "")).strip() not in ("observe", "close"):
                    continue
                if str(fm.get("created_at", "")).strip()[:7] == cohort:
                    total += 1
    return total


_OUTCOME_VERDICT_PATTERN = re.compile(
    r"\b(disconfirmed|refuted|not confirmed|inconclusive|confirmed)\b", re.I
)


def _extract_outcome_verdict(body: str) -> Optional[str]:
    """Best-effort verdict word from a Work Object's outcome-review lines.

    Scoped to lines mentioning "outcome review" or "outcome assessment" (or the
    ``## Outcome`` / ``## Outcome review`` heading), then searched for a single
    verdict keyword (WO 2026-08-11-013 Decision 1). Returns ``None`` when no
    keyword is found in that scope -- callers must report this as "reviewed,
    verdict not mechanically determined," never as "not reviewed." This is a
    read-only projection with no semantic judgment: it reports a keyword match,
    not a determination of whether the review's conclusion actually held.
    """
    lines = []
    for line in body.splitlines():
        lower = line.lower()
        if (
            "outcome review" in lower
            or "outcome assessment" in lower
            or re.match(r"^## outcome", lower)
        ):
            lines.append(line)
    if not lines:
        return None
    scoped = "\n".join(lines).lower()
    found = {m.lower().strip() for m in _OUTCOME_VERDICT_PATTERN.findall(scoped)}
    if not found:
        return None
    if found & {"disconfirmed", "refuted", "not confirmed"}:
        return "disconfirmed"
    if "inconclusive" in found:
        return "inconclusive"
    if "confirmed" in found:
        return "confirmed"
    return None


def list_outcomes(objects_dir: Path) -> List[str]:
    """Workspace-level advisory report of outcome-review coverage and verdicts
    (WO 2026-08-11-013).

    Read-only projection over existing data, computed fresh at read time --
    no new storage, no stable ``OUT-*`` identifier. Reuses
    ``_has_real_outcome_review`` for presence/absence (reliable: 44/44 on the
    real corpus tested for WO 2026-08-11-013) and ``_extract_outcome_verdict``
    for a best-effort verdict (reliable on 32/44 real cases; the remaining 12
    report "reviewed -- see body" rather than a guessed verdict).
    """
    lines: List[str] = []
    reviewed: List[Tuple[str, Optional[str]]] = []
    unreviewed: List[str] = []
    for year_dir in sorted(objects_dir.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for obj_file in sorted(month_dir.iterdir()):
                if obj_file.suffix != ".md":
                    continue
                try:
                    content = obj_file.read_text(encoding="utf-8")
                except Exception:
                    continue
                fm = parse_frontmatter(content)
                state = str(fm.get("state", "")).strip()
                if state not in ("observe", "close"):
                    continue
                body = _extract_body(content)
                if not _has_real_outcome_review(body):
                    unreviewed.append(obj_file.stem)
                    continue
                verdict = _extract_outcome_verdict(body)
                reviewed.append((obj_file.stem, verdict))

    lines.append(f"outcomes: {len(reviewed)} reviewed, {len(unreviewed)} unreviewed")
    for obj_id, verdict in reviewed:
        label = verdict if verdict else "reviewed — see body"
        lines.append(f"outcomes: {obj_id}: {label}")
    for obj_id in unreviewed:
        lines.append(f"outcomes: {obj_id}: not yet reviewed")
    return lines


# ── next_action / revisit_trigger presence ────────────────────────────────────

FORWARD_MOTION_STATES = ("notice", "explore", "design", "build")


def check_next_action_presence(file_path: Path) -> List[str]:
    """Hard error: forward-motion objects must carry a frontmatter next_action.

    Per WORK-OBJECT.md:20. Promoted to a hard error after the corpus backfill
    (WO 2026-08-10-014, follow-on 2). Objects predating the field were
    backfilled; new objects get it from ws create.
    """
    errors = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return errors
    fm = parse_frontmatter(content)
    state = str(fm.get("state", "")).strip()
    if state in FORWARD_MOTION_STATES and not str(fm.get("next_action", "") or "").strip():
        errors.append(
            f"{file_path}: forward-motion object (state '{state}') has no "
            "frontmatter next_action"
        )
    return errors


def check_revisit_trigger_presence(file_path: Path) -> List[str]:
    """Advisory warning: waiting/paused objects should carry revisit_trigger.

    Per WORK-OBJECT.md:43. Kept advisory (non-blocking) because 4 waiting/paused
    objects still lack the field; promotion is a smaller follow-on (WO
    2026-08-10-014).
    """
    warnings = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return warnings
    fm = parse_frontmatter(content)
    status = str(fm.get("status", "")).strip()
    if status in ("waiting", "paused") and not str(fm.get("revisit_trigger", "") or "").strip():
        warnings.append(
            f"{file_path}: status '{status}' but no frontmatter revisit_trigger"
        )
    return warnings


# ── Contract drift (WO 2026-08-11-019 Decision 1/2, Layer 1) ──────────────────

_CONTRACT_DRIFT_FIELDS: List[Tuple[str, str, frozenset]] = [
    ("type", "VALID_TYPES", VALID_TYPES),
    ("consequence", "VALID_CONSEQUENCES", VALID_CONSEQUENCES),
    ("sensitivity", "VALID_SENSITIVITIES", VALID_SENSITIVITIES),
    ("state", "VALID_STATES", VALID_STATES),
    ("status", "VALID_STATUSES", VALID_STATUSES),
]


def _extract_cli_choices(main_source: str, field: str) -> List[Tuple[int, set]]:
    """Find every ``choices=[...]`` list attached to a ``--<field>`` argument
    in ``__main__.py``'s source text, with its 1-indexed line number.

    Deliberately structural: matches only where an actual ``choices=[...]``
    list follows the argument name -- a same-named argument with no choices
    (e.g. claim inspect's free-text ``--state`` filter) is not matched, no
    semantic judgment involved.
    """
    results = []
    pattern = re.compile(
        r'"--' + re.escape(field) + r'"[^)]*?choices=\[([^\]]*)\]', re.DOTALL
    )
    for m in pattern.finditer(main_source):
        line_no = main_source.count("\n", 0, m.start()) + 1
        raw_items = re.findall(r'"([^"]*)"', m.group(1))
        results.append((line_no, set(raw_items)))
    return results


def check_contract_drift(main_py_path: Optional[Path] = None) -> List[str]:
    """Workspace-level advisory check: do schema.py's VALID_* enums agree
    with __main__.py's argparse choices=[...] lists? (WO 2026-08-11-019
    Decision 1 Layer 1, Decision 2.)

    Direct set-equality per field -- no path resolution, no semantic
    judgment. Structural presence of a ``choices=[...]`` list is the only
    signal; a same-named argument without one (e.g. claim inspect's
    free-text state filter) is not compared.
    """
    if main_py_path is None:
        main_py_path = Path(__file__).parent / "__main__.py"
    if not main_py_path.is_file():
        return ["contract-drift check requires the __main__.py path"]

    try:
        main_source = main_py_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"contract-drift: cannot read {main_py_path}: {e}"]

    errors: List[str] = []
    for field, const_name, valid_set in _CONTRACT_DRIFT_FIELDS:
        for line_no, cli_set in _extract_cli_choices(main_source, field):
            if cli_set != valid_set:
                missing = valid_set - cli_set
                extra = cli_set - valid_set
                detail = []
                if missing:
                    detail.append(f"missing from CLI: {sorted(missing)}")
                if extra:
                    detail.append(f"not in schema: {sorted(extra)}")
                errors.append(
                    f"contract-drift: {main_py_path}:{line_no}: --{field} "
                    f"choices disagree with schema.py {const_name} "
                    f"({'; '.join(detail)})"
                )
    return errors


# ── Check registry ────────────────────────────────────────────────────────────

CHECK_REGISTRY: Dict[str, callable] = {
    "schema": check_schema,
    "sections": check_sections,
    "append-only": check_append_only,
    "attention": None,  # Special: workspace-level check
    "attention-limits": None,  # Special: workspace-level check
    "dashboard-signals": None,  # Special: workspace-level advisory check
    "ledger": None,  # Special: workspace-level advisory check (not in defaults)
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
    "outcome-review": None,  # Special: workspace-level advisory check (not in defaults)
    "evidence-freshness": None,  # Special: workspace-level advisory check (not in defaults)
    "evidence-relations": None,  # Special: workspace-level advisory check (not in defaults)
    "verification-freshness": None,  # Special: workspace-level advisory check (not in defaults)
    "next-action": check_next_action_presence,  # Hard: forward-motion objects need next_action
    "contract-drift": None,  # Special: workspace-level check, no per-object path
}

# Per-check advisory warnings: surfaced explicitly but non-blocking. Run for
# both default and explicit invocations of the named check.
CHECK_WARNING_REGISTRY: Dict[str, callable] = {
    "append-only": check_append_only_baseline,
    "next-action": check_revisit_trigger_presence,  # Advisory: waiting/paused need revisit_trigger
}

DEFAULT_CHECKS = [
    "schema", "sections", "append-only", "next-action", "sensitivity",
    "sensitivity-policy", "lifecycle", "claims", "lanes",
    "authority", "protected-fields", "history-integrity",
    "file-integrity", "incident-routing", "prerequisites",
    "dashboard-signals", "contract-drift",
]

DEFAULT_WARNING_CHECKS = [
    check_campaign_anchor,
    check_consequence_plausibility,
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
    run_default_checks = check_names is None
    if run_default_checks:
        check_names = list(DEFAULT_CHECKS)

    all_errors: List[str] = []
    all_warnings: List[str] = []

    if run_default_checks:
        for warning_check in DEFAULT_WARNING_CHECKS:
            for fp in file_paths:
                all_warnings.extend(warning_check(fp))

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

        if name == "dashboard-signals":
            # Workspace-level advisory check: relay the gauge counts as
            # warnings (non-blocking); fail closed only on malformed headings.
            if objects_dir:
                warnings, errs = check_dashboard_signals(objects_dir)
                all_warnings.extend(warnings)
                all_errors.extend(errs)
            continue

        if name == "ledger":
            # Workspace-level advisory check over the component ledger.
            # Excluded from DEFAULT_CHECKS; run explicitly via `ws validate
            # ledger`. Read-only; reports edge and staleness defects.
            if objects_dir:
                all_errors.extend(check_ledger(objects_dir))
            else:
                all_errors.append(
                    "Ledger check requires the objects/ directory path"
                )
            continue

        if name == "contract-drift":
            # Workspace-level check: schema.py VALID_* enums vs __main__.py
            # argparse choices=[...] lists, direct set-equality. WO
            # 2026-08-11-019 Layer 1/Decision 2. In DEFAULT_CHECKS: verified
            # clean on the real repo and catches a seeded mismatch with no
            # other noise before promotion to blocking.
            all_errors.extend(check_contract_drift())
            continue

        if name == "outcome-review":
            # Workspace-level advisory check over outcome-review coverage.
            # Excluded from DEFAULT_CHECKS; run explicitly via `ws validate
            # outcome-review`. Read-only; reports objects at observe/close
            # without a recorded outcome review, per cohort.
            if objects_dir:
                all_errors.extend(check_outcome_review(objects_dir))
            else:
                all_errors.append(
                    "Outcome-review check requires the objects/ directory path"
                )
            continue

        if name == "evidence-freshness":
            # Workspace-level advisory check over [system] evidence source
            # locators. Excluded from DEFAULT_CHECKS; run explicitly via
            # `ws validate evidence-freshness`. Read-only and warning-only:
            # stale citations mean "re-read", not "validation failed".
            if objects_dir:
                all_warnings.extend(
                    check_evidence_freshness(file_paths, objects_dir)
                )
            else:
                all_errors.append(
                    "Evidence-freshness check requires the objects/ directory path"
                )
            continue

        if name == "evidence-relations":
            # Workspace-level advisory check surfacing candidate supports/
            # counters relations from exact-citation overlap. Excluded from
            # DEFAULT_CHECKS; run explicitly via `ws validate
            # evidence-relations`. Read-only and warning-only: a shared
            # citation is a candidate for human confirmation, not a claim.
            if objects_dir:
                all_warnings.extend(
                    check_evidence_relations(file_paths, objects_dir)
                )
            else:
                all_errors.append(
                    "Evidence-relations check requires the objects/ directory path"
                )
            continue

        if name == "verification-freshness":
            # Workspace-level advisory check re-running re-runnable commands
            # cited in Verification and release evidence bullets. Excluded
            # from DEFAULT_CHECKS; run explicitly via `ws validate
            # verification-freshness`. Read-only intent, but executes the
            # cited command -- only ever a command with a recognized
            # executable prefix (WO 2026-08-11-012 Decision 2).
            if objects_dir:
                all_warnings.extend(
                    check_verification_freshness(file_paths, objects_dir)
                )
            else:
                all_errors.append(
                    "Verification-freshness check requires the objects/ directory path"
                )
            continue

        check_fn = CHECK_REGISTRY[name]
        for fp in file_paths:
            errs = check_fn(fp)
            all_errors.extend(errs)

        warn_fn = CHECK_WARNING_REGISTRY.get(name)
        if warn_fn is not None:
            for fp in file_paths:
                all_warnings.extend(warn_fn(fp))

    for warning in all_warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    for err in all_errors:
        print(err, file=sys.stderr)

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found.", file=sys.stderr)
        return 1

    if run_default_checks:
        print("All default validation checks passed.")
    else:
        print("All named validation checks passed.")
    return 0
