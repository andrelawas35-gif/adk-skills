"""Readers for the bounded epistemic-pressure dashboard tracer."""

import re
from pathlib import Path
from typing import Optional

from .claim import parse_claims
from .sections import get_section


_CONFLICT_HEADING = re.compile(
    r"^  CONF-\d{4}_\d{2}_\d{2}_\d{3}-\d{3}:$", re.MULTILINE
)

_CONFLICT_ID = re.compile(
    r"^  (CONF-\d{4}_\d{2}_\d{2}_\d{3}-\d{3}):$", re.MULTILINE
)

_CONFLICT_RESOLUTION_BLOCK = re.compile(
    r"^  CONFRES-\d{4}_\d{2}_\d{2}_\d{3}-\d{3}:\n(?P<body>(?:    .+(?:\n|$))*)",
    re.MULTILINE,
)

_RESOLVED_CONFLICT_ID = re.compile(
    r"^    conflict_id: (CONF-\d{4}_\d{2}_\d{2}_\d{3}-\d{3})$",
    re.MULTILINE,
)

_CLAIM_HEADING = re.compile(r"^  CLM-[\w]+-\d+:$", re.MULTILINE)

# Common words that never signal content-level provenance for a claim. Used to
# keep the Decision 3 content-reference test from matching incidental prose
# (e.g., "this entry names ... and gives ... a second source").
_STOPWORDS = frozenset({
    "and", "the", "this", "that", "these", "those", "with", "from",
    "into", "onto", "over", "under", "for", "was", "were", "are",
    "has", "have", "had", "not", "but", "its", "they", "them",
    "then", "than", "also", "only", "just", "after", "before",
    "during", "about", "which", "whose", "there", "where", "when",
    "will", "would", "could", "should", "shall", "must", "might",
    "does", "doing", "done", "been", "being", "name", "names",
    "entry", "entries", "source", "sources", "row", "rows",
    "give", "gives", "given", "first", "second", "third",
    "claim", "claims", "note", "notes",
})


def _content_tokens(text: str) -> set:
    """Lowercased substantive tokens (length >= 4) in *text*."""
    tokens = set(re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", text.lower()))
    return {token for token in tokens if token not in _STOPWORDS}


def _entry_references_claim_content(entry: str, claim: dict) -> bool:
    """True when *entry* provides content-level provenance for *claim*.

    Decision 3/4: a ledger row counts as a distinct source for a claim only
    when its Entry shares a substantive content token with the claim's text.
    Registration/tracking rows that name only the claim ID (e.g., "Tracer
    executed: claim CLM-... registered") do not count as sources.
    """
    claim_id = claim.get("id", "")
    entry_tokens = _content_tokens(entry)
    if claim_id:
        entry_tokens.discard(claim_id.lower())
    text_tokens = _content_tokens(claim.get("text", ""))
    return bool(entry_tokens & text_tokens)


def _objects_dir() -> Path:
    """Resolve the current workspace's canonical Work Object directory."""
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        objects = candidate / ".work-studio" / "objects"
        if objects.is_dir():
            return objects
    raise FileNotFoundError(".work-studio/objects not found")


def _resolved_conflict_ids(claims: str) -> set:
    """Conflict IDs named by appended CONFRES- records."""
    resolved = set()
    for resolution in _CONFLICT_RESOLUTION_BLOCK.finditer(claims):
        match = _RESOLVED_CONFLICT_ID.search(resolution.group("body"))
        if match:
            resolved.add(match.group(1))
    return resolved


def count_unresolved_conflicts(objects_dir: Optional[Path] = None) -> int:
    """Count CONF- records that have no matching CONFRES- record.

    ``objects_dir`` overrides the resolved workspace objects directory (used by
    the ``ws validate`` dashboard-signals check, which already holds the path);
    when omitted it resolves from the current directory.
    """
    root = _objects_dir() if objects_dir is None else objects_dir
    conflicts = set()
    resolved_conflicts = set()
    for path in root.rglob("*.md"):
        content = path.read_text()
        body = content[content.find("---", 3) + 3:] if content.startswith("---") else content
        claims = get_section(body, "Claims")
        if claims:
            for line in claims.splitlines():
                heading = line.strip()
                if (
                    heading.startswith("CONF-")
                    and not _CONFLICT_HEADING.fullmatch(line)
                ):
                    raise ValueError(
                        f"{path}: malformed conflict heading: {heading}"
                    )
            conflicts.update(_CONFLICT_ID.findall(claims))
            resolved_conflicts.update(_resolved_conflict_ids(claims))
    return len(conflicts - resolved_conflicts)


def _evidence_ledger_rows(body: str) -> list:
    """Return (Source, Entry) pairs from the Work Object's Evidence ledger."""
    ledger = get_section(body, "Evidence ledger")
    if not ledger:
        return []
    rows = []
    for line in ledger.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3:
            rows.append((cells[1], cells[2]))
    return rows


def count_claims_below_support_adequacy(
    objects_dir: Optional[Path] = None,
) -> int:
    """Count claims with zero or one distinct source reference.

    Support-adequacy signal (Direction 5, combined single-source dependencies
    + unsupported authorizing claims). A claim's distinct sources are
    Evidence-ledger Source cells in the same Work Object whose Entry provides
    content-level provenance for the claim (Decision 3: the Entry must share
    a substantive content token with the claim's text; registration/tracking
    rows naming only the claim ID do not count). A claim's declared ``scope``
    (legacy scalar or structured ``paths``) is a defeater surface, not
    provenance, and never counts as a source. Claims with one or fewer
    distinct sources are counted as below the adequacy line. Malformed
    ``CLM-`` blocks fail closed with a file-specific ValueError rather than
    being silently skipped or counted.

    ``objects_dir`` overrides the resolved workspace objects directory (used by
    the ``ws validate`` dashboard-signals check); when omitted it resolves from
    the current directory.
    """
    count = 0
    root = _objects_dir() if objects_dir is None else objects_dir
    for path in root.rglob("*.md"):
        content = path.read_text()
        body = content[content.find("---", 3) + 3:] if content.startswith("---") else content
        claims_section = get_section(body, "Claims")
        if not claims_section:
            continue

        # Fail closed on malformed CLM- blocks (mirrors the conflicts reader).
        for line in claims_section.splitlines():
            heading = line.strip()
            if heading.startswith("CLM-") and not _CLAIM_HEADING.fullmatch(line):
                raise ValueError(
                    f"{path}: malformed claim heading: {heading}"
                )

        ledger = _evidence_ledger_rows(body)
        for claim in parse_claims(body):
            # A claim's declared scope (legacy scalar or structured `paths`) is
            # a defeater surface, not provenance — it never counts as a source
            # (2026-08-09-005 / answered 2026-07-28-005). Structured (dict)
            # scope is ignored safely rather than reaching `.strip()`.
            sources = set()
            claim_id = claim.get("id", "")
            for source, entry in ledger:
                if (
                    claim_id
                    and claim_id in entry
                    and source
                    and _entry_references_claim_content(entry, claim)
                ):
                    sources.add(source)
            if len(sources) <= 1:
                count += 1
    return count
