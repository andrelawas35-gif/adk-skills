"""Live-web-research contract records and fetch logic (WO 2026-08-17-011).

The runtime's first external-effect node (build plan's own taxonomy:
"external-effect nodes: deployment or external writes only after explicit
authority and with recovery/compensation" -- distinct from every prior
Phase's local-only, read-derive-checkpoint pattern). Bounded to a single
explicit URL, gated by explicit human approval (via LangGraph's `interrupt()`
in `runtime/graph.py`) before any network call. Since a fetch is a read-only
GET, there is no external state to compensate/undo on failure -- only
failure-as-gap applies (Decision 2): a failed fetch is recorded honestly,
never silently treated as a null or successful result.

``ResearchReceipt`` mirrors ``HandoffReceipt``'s shape (runtime/handoff.py)
and is a runtime-plane record only -- fetched content is not a canonical
Evidence Ledger entry until a human or `investigate-live-question` reviews
and records it (WO 2026-08-17-011 Constraints).
"""

from __future__ import annotations

import urllib.error
import urllib.request
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

FETCH_TIMEOUT_SECONDS = 10.0
MAX_RESPONSE_BYTES = 1_000_000  # 1 MB cap


class ResearchReceipt(BaseModel):
    """Completion record from one bounded, human-approved live fetch."""

    model_config = ConfigDict(extra="forbid")

    status: str  # "completed" | "failed"
    source: str
    evidence: str = ""
    confidence: str = "low"
    detail: str = ""
    started_at: datetime
    completed_at: datetime


def fetch_url(
    url: str,
    timeout: float = FETCH_TIMEOUT_SECONDS,
    max_bytes: int = MAX_RESPONSE_BYTES,
) -> tuple[bool, str, str]:
    """Perform one bounded GET. Returns (ok, body_or_empty, detail).

    Pure at the boundary: all bounding (timeout, size cap) happens here so
    callers never need to trust an unbounded response. Never raises -- any
    failure (timeout, HTTP error, connection error, oversized response) is
    reported through the returned tuple, matching Decision 2's "failure
    recorded as a gap, never silently swallowed" requirement.
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        return False, "", f"HTTP error {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return False, "", f"connection error: {exc.reason}"
    except (TimeoutError, OSError) as exc:
        return False, "", f"fetch failed: {exc}"

    if len(body) > max_bytes:
        return False, "", f"response exceeded {max_bytes} byte cap"

    try:
        text = body.decode("utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover -- decode with errors="replace" cannot raise
        return False, "", f"decode failed: {exc}"

    return True, text, ""


def build_receipt(
    url: str,
    started_at: datetime,
    completed_at: datetime,
    ok: bool,
    body: str,
    detail: str,
) -> ResearchReceipt:
    """Assemble a ResearchReceipt from a fetch_url result.

    Pure: no I/O. Confidence is deliberately capped at "low" -- a single
    unreviewed fetch is not attributable evidence until a human or
    investigate-live-question reviews it (WO 2026-08-17-011 Constraints).
    """
    return ResearchReceipt(
        status="completed" if ok else "failed",
        source=url,
        evidence=body if ok else "",
        confidence="low" if ok else "none",
        detail=detail,
        started_at=started_at,
        completed_at=completed_at,
    )
