"""Strict Pydantic envelope for Work Object frontmatter (WO 2026-08-15-006).

Implements Decision 1's accepted boundary: Pydantic v2 is used ONLY in this
runtime contract layer (Python 3.11); `tools/ws` stays dependency-free stdlib;
the envelope's allowed values are generated from `tools/ws/schema.py`'s
`VALID_*` frozensets so the runtime contract and the canonical CLI validator
cannot silently disagree (parent Decision 1 constraint).

The 5 corpus fields declared below (`revisit_trigger`, `responds_to`,
`supersedes`, `superseded_by`, `unblocks`) are the exact unknown fields the
round-trip tracer bullet (2026-08-15-005, Decision 2) proved exist in the live
corpus. Declaring them lets all 133 Work Objects round-trip cleanly while
`extra="forbid"` still rejects any genuinely unknown field.

Run (from repo root, ephemeral 3.11 env managed by uv):
    uv run python -m unittest discover -s runtime/tests -v
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

# Ensure the repo root is importable so tools/ws/schema.py (stdlib-only) can
# serve as the single source of enum truth.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.ws import schema as _ws_schema  # noqa: E402


def _literal(values: frozenset) -> object:
    """Build a Literal type from a frozenset of strings (tools/ws/schema.py)."""
    return Literal[tuple(sorted(values))]


class WorkObjectEnvelope(BaseModel):
    """Strict frontmatter envelope for a Work Object.

    `extra="forbid"` rejects any field not declared here. Enum membership is
    generated from `tools/ws/schema.py`'s `VALID_*` frozensets.
    """

    model_config = ConfigDict(extra="forbid")

    # Canonical fields (tools/ws/schema.py + the created-object template).
    schema_version: int
    id: str
    title: str
    type: _literal(_ws_schema.VALID_TYPES)
    status: _literal(_ws_schema.VALID_STATUSES)
    state: _literal(_ws_schema.VALID_STATES)
    consequence: _literal(_ws_schema.VALID_CONSEQUENCES)
    sensitivity: _literal(_ws_schema.VALID_SENSITIVITIES)
    created_at: datetime
    updated_at: datetime
    next_action: Optional[str] = None
    campaign: Optional[str] = None

    # Declared corpus fields (verified by the 005 round-trip tracer bullet).
    revisit_trigger: Optional[str] = None
    responds_to: Optional[str] = None
    supersedes: Optional[str] = None
    superseded_by: Optional[str] = None
    unblocks: Optional[str] = None


def envelope_json_schema() -> dict:
    """Generate the JSON Schema for the envelope (committed snapshot source)."""
    return WorkObjectEnvelope.model_json_schema()
