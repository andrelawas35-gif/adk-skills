"""ws authority check — query authority grants against History entries.

Read-only command. Parses Authority History entries from a Work Object
and returns GRANTED, DENIED, or AMBIGUOUS for a given action.

Part of Tier 2 row 1 (AuthorityGrant normalization/check).
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .validate import _is_authority_entry, _parse_history_entries


# ── Results ───────────────────────────────────────────────────────────────────

GRANTED = "GRANTED"
DENIED = "DENIED"
AMBIGUOUS = "AMBIGUOUS"


def _try_parse_date(date_str: str) -> Optional[datetime]:
    """Try to parse an ISO date string. Returns None if unparseable."""
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def _check_entry(
    entry: Dict[str, str], action: str
) -> Tuple[str, str]:
    """Check a single Authority entry against an action.

    Returns (result, reason) where result is GRANTED, DENIED, or AMBIGUOUS.
    """
    scope = entry.get("scope", "").strip()
    expiry_str = entry.get("expiry", "").strip()

    # ── Scope check ──────────────────────────────────────────────────────
    if not scope:
        return AMBIGUOUS, "Authority entry has no scope"

    # Split scope by whitespace into individual action tokens
    allowed_actions = scope.split()
    if not allowed_actions:
        return AMBIGUOUS, "Scope is empty"

    # If any token contains wildcard or special chars, it's ambiguous
    for token in allowed_actions:
        if any(c in token for c in "*?[]{}"):
            return AMBIGUOUS, f"Scope contains unparseable token: {token}"

    action_allowed = action in allowed_actions

    # ── Expiry check ─────────────────────────────────────────────────────
    if expiry_str:
        expiry_date = _try_parse_date(expiry_str)
        if expiry_date is None:
            return AMBIGUOUS, f"Unparseable expiry: {expiry_str}"
        now = datetime.now()
        if now > expiry_date:
            return DENIED, f"Grant expired at {expiry_str}"

    # ── Result ───────────────────────────────────────────────────────────
    if action_allowed:
        return GRANTED, f"Action '{action}' is within scope '{scope}'"
    else:
        return DENIED, f"Action '{action}' is not in scope '{scope}'"


def cmd_authority_check(args: argparse.Namespace) -> int:
    """Check whether an active, unexpired grant covers a given action.

    Reads the Work Object's History, finds Authority entries, and returns
    GRANTED, DENIED, or AMBIGUOUS for the action specified with --action.
    """
    file_path = Path(args.id)
    if not file_path.exists():
        # Try to resolve as a Work Object ID
        ws_root = _find_work_studio_root()
        if ws_root is None:
            print(f"Error: File not found: {args.id}", file=sys.stderr)
            return 1
        objects_dir = ws_root / ".work-studio" / "objects"
        try:
            file_path = _resolve_object_file(objects_dir, args.id)
        except FileNotFoundError:
            print(f"Error: Work Object not found: {args.id}", file=sys.stderr)
            return 1

    try:
        content = file_path.read_text()
    except Exception as e:
        print(f"Error: Cannot read {file_path}: {e}", file=sys.stderr)
        return 1

    body = _extract_body(content)
    entries = _parse_history_entries(body)
    authority_entries = [e for e in entries if _is_authority_entry(e)]

    if not authority_entries:
        print(AMBIGUOUS)
        print("No Authority History entries found")
        return 0

    results = []
    for entry in authority_entries:
        result, reason = _check_entry(entry, args.action)
        results.append((result, reason, entry))

    # If any entry GRANTED the action, overall result is GRANTED
    granted = [r for r in results if r[0] == GRANTED]
    if granted:
        print(GRANTED)
        print(granted[0][1])
        return 0

    # If any entry is AMBIGUOUS, overall result is AMBIGUOUS
    ambiguous = [r for r in results if r[0] == AMBIGUOUS]
    if ambiguous:
        print(AMBIGUOUS)
        print(ambiguous[0][1])
        return 0

    # All entries DENIED
    print(DENIED)
    print(results[0][1] if results else "No matching grant")
    return 0


def _find_work_studio_root() -> Optional[Path]:
    """Search upward from cwd for .work-studio/config.md."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio" / "config.md").exists():
            return parent
    return None


def _resolve_object_file(objects_dir: Path, obj_id: str) -> Path:
    """Find a Work Object file by its ID anywhere under objects_dir.

    Raises FileNotFoundError if not found.
    """
    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if obj_file.name.startswith(obj_id) and obj_file.suffix == ".md":
                    return obj_file

    raise FileNotFoundError(f"Work Object not found for ID: {obj_id}")


def _extract_body(content: str) -> str:
    """Extract body content after YAML frontmatter."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return content
