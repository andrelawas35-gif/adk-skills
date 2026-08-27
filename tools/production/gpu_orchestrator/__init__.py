"""File-backed GPU claim registry tracer for COMP-041."""

from .registry import (
    ClaimResult,
    GPU_STATES,
    OWNER_TO_STATE,
    claim,
    query,
    release,
)

__all__ = [
    "ClaimResult",
    "GPU_STATES",
    "OWNER_TO_STATE",
    "claim",
    "query",
    "release",
]
