"""Epistemic lint: validate provenance tag usage across the repository.

Scans non-ledger Markdown files for bracketed tag tokens and validates
them against the canonical taxonomy defined in
``references/epistemic/taxonomy.yaml``.

Usage::

    python3 -m tools.ws epistemic lint [paths ...]

The six base tags (from AGREEMENT-LOOP.md lines 96-111) are always valid
as bare tags.  ``base:subtype`` compound tags are valid only when the pair
is registered in the taxonomy file.

Reports:
    - Undeclared base tags (not in the canonical six).
    - Unregistered ``base:subtype`` pairs (not in the taxonomy).
    - File/line for each finding with a proposed non-destructive disposition.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


# ── Regex for bracketed tag tokens ────────────────────────────────────────────

# Matches:
#   [tag]              — bare base tag (group(2) and group(3) are None)
#   [base:subtype]     — colon-subtype (governed, must be registered)
#   [base/subtype]     — slash-subtype (not governed, reported as undeclared)
_TAG_TOKEN_RE = re.compile(r"\[([a-z][a-z0-9_]*)(?:([:/])([a-z][a-z0-9_]*))?\]")

# ── Default scan paths (relative to workspace root) ──────────────────────────

DEFAULT_SCAN_PATTERNS: List[str] = [
    "skills/core/**/*.md",
    "fixtures/**/*.md",
    "references/**/*.md",
    ".work-studio/objects/**/*.md",
]

# Paths to exclude from linting (generated, non-canonical, etc.)
EXCLUDE_PATTERNS: List[str] = [
    "references/epistemic/taxonomy.yaml",  # taxonomy itself
]

# Default allowlist path (relative to workspace root)
DEFAULT_ALLOWLIST_PATH = "references/epistemic/lint-allowlist.yaml"


# ── Allowlist loading ─────────────────────────────────────────────────────────


def load_allowlist(ws_root: Path) -> Optional[dict]:
    """Load the lint allowlist from ``references/epistemic/lint-allowlist.yaml``.

    Returns the parsed YAML dict, or ``None`` if the file is missing or
    unparsable.
    """
    path = ws_root / DEFAULT_ALLOWLIST_PATH
    if not path.exists():
        return None

    if yaml is not None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return None
    return None


def _build_allowlist_sets(allowlist: dict) -> Tuple[Set[str], List[str]]:
    """Build (ignore_tokens, ignore_file_globs) from allowlist dict.

    - ``ignore_tokens`` — exact bracket tokens to skip (e.g. ``{"[x]", "[tag]"}``)
    - ``ignore_file_globs`` — glob patterns for files to skip entirely
    """
    ignore_tokens: Set[str] = set()
    for t in allowlist.get("ignore_tokens", []):
        if isinstance(t, str):
            ignore_tokens.add(t)

    ignore_file_globs: List[str] = []
    for g in allowlist.get("ignore_files", []):
        if isinstance(g, str):
            ignore_file_globs.append(g)

    return ignore_tokens, ignore_file_globs


def _file_matches_ignore_globs(relative_path: str, globs: List[str]) -> bool:
    """Check if a relative file path matches any of the ignore glob patterns."""
    from fnmatch import fnmatch

    for pattern in globs:
        if fnmatch(relative_path, pattern):
            return True
    return False

# ── Taxonomy loading ─────────────────────────────────────────────────────────


def _find_workspace_root() -> Optional[Path]:
    """Walk upward from CWD to find the workspace root (has .git or .work-studio/)."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".git").is_dir() or (parent / ".work-studio").is_dir():
            return parent
    return None


def load_taxonomy(ws_root: Path) -> Optional[dict]:
    """Load the canonical taxonomy from ``references/epistemic/taxonomy.yaml``.

    Returns the parsed YAML dict, or ``None`` if the file is missing or
    unparsable.
    """
    taxonomy_path = ws_root / "references" / "epistemic" / "taxonomy.yaml"
    if not taxonomy_path.exists():
        return None

    if yaml is None:
        # Fallback: manual parse for the simple structure we need
        return _fallback_parse_taxonomy(taxonomy_path)

    try:
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return _fallback_parse_taxonomy(taxonomy_path)


def _fallback_parse_taxonomy(path: Path) -> Optional[dict]:
    """Minimal YAML parser for our specific taxonomy schema (no PyYAML)."""
    import json

    # Very simple state machine for YAML -> JSON conversion
    result: dict = {"base_tags": [], "subtypes": []}
    current_base: Optional[dict] = None
    current_subtype: Optional[dict] = None

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.rstrip()

                # Top-level keys
                if stripped == "base_tags:":
                    continue
                if stripped == "subtypes:":
                    continue
                if stripped.startswith("schema_version:"):
                    continue

                # Base tag entry
                if stripped.startswith("  - tag:"):
                    current_base = {"tag": stripped.split(":", 1)[1].strip()}
                    current_subtype = None
                    continue
                if current_base is not None and stripped.startswith("    description:"):
                    # Skip description
                    if current_base and current_base not in result.setdefault("base_tags", []):
                        result.setdefault("base_tags", []).append(current_base)
                    current_base = None
                    continue

                # Subtype entry
                if stripped.startswith("  - base:"):
                    current_subtype = {"base": stripped.split(":", 1)[1].strip()}
                    current_base = None
                    continue
                if current_subtype is not None and stripped.startswith("    subtype:"):
                    current_subtype["subtype"] = stripped.split(":", 1)[1].strip()
                    continue
                if current_subtype is not None and stripped.startswith("    description:"):
                    if current_subtype and "subtype" in current_subtype:
                        result.setdefault("subtypes", []).append(current_subtype)
                    current_subtype = None
                    continue
    except Exception:
        return None

    return result


def _build_tag_sets(taxonomy: dict) -> Tuple[Set[str], Set[str]]:
    """Build (canonical_base_tags, registered_subtype_pairs) from taxonomy dict.

    - ``canonical_base_tags`` — e.g. ``{"system", "decision", ...}``
    - ``registered_subtype_pairs`` — e.g. ``{"system:discovery", "system:predecessor", ...}``
    """
    base_tags: Set[str] = set()
    for bt in taxonomy.get("base_tags", []):
        if isinstance(bt, dict) and "tag" in bt:
            base_tags.add(bt["tag"])

    subtype_pairs: Set[str] = set()
    for st in taxonomy.get("subtypes", []):
        if isinstance(st, dict) and "base" in st and "subtype" in st:
            subtype_pairs.add(f"{st['base']}:{st['subtype']}")

    return base_tags, subtype_pairs


# ── File scanning ─────────────────────────────────────────────────────────────


def _gather_files(
    ws_root: Path,
    paths: Optional[List[str]] = None,
) -> List[Path]:
    """Gather all ``.md`` files under the given paths (or default scan paths).

    Excludes files matching ``EXCLUDE_PATTERNS``.
    """
    if not paths:
        paths = DEFAULT_SCAN_PATTERNS

    collected: List[Path] = []
    exclude_set = {ws_root / p for p in EXCLUDE_PATTERNS}

    for pattern in paths:
        full_pattern = str(ws_root / pattern)
        # Use glob or rglob depending on pattern
        if "**" in pattern:
            from glob import glob as glob_glob

            matches = glob_glob(full_pattern, recursive=True)
            for m in matches:
                p = Path(m)
                if p.is_file() and p.suffix == ".md" and p not in exclude_set:
                    collected.append(p)
        else:
            target = ws_root / pattern
            if target.is_dir():
                for p in sorted(target.rglob("*.md")):
                    if p not in exclude_set:
                        collected.append(p)
            elif target.is_file() and target.suffix == ".md":
                if target not in exclude_set:
                    collected.append(target)

    return sorted(set(collected))


def _scan_file_for_tags(
    file_path: Path,
    canonical_base: Set[str],
    registered_pairs: Set[str],
    ignore_tokens: Optional[Set[str]] = None,
    ignore_file_globs: Optional[List[str]] = None,
) -> List[dict]:
    """Scan a single file for tag tokens and return findings.

    Each finding is a dict::

        {
            "file": str(relative path),
            "line": int,
            "token": str (the full bracketed token),
            "base": str,
            "subtype": Optional[str],
            "issue": str  # human-readable description
        }

    If ``ignore_tokens`` is provided, findings for those exact bracket tokens
    are suppressed. If ``ignore_file_globs`` is provided, files matching any
    glob pattern are skipped entirely.
    """
    findings: List[dict] = []

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return findings

    ws_root = _find_workspace_root()
    try:
        relative = str(file_path.relative_to(ws_root)) if ws_root else str(file_path)
    except ValueError:
        relative = str(file_path)

    # Skip files matching ignore globs
    if ignore_file_globs and _file_matches_ignore_globs(relative, ignore_file_globs):
        return findings

    if ignore_tokens is None:
        ignore_tokens = set()

    for line_num, line in enumerate(text.split("\n"), start=1):
        for match in _TAG_TOKEN_RE.finditer(line):
            base = match.group(1)
            connector = match.group(2)  # ':' or '/'
            subtype = match.group(3)
            token = match.group(0)  # full match including brackets

            # Skip allowlisted tokens
            if token in ignore_tokens:
                continue

            # Slash syntax: always reported as undeclared (not a governed pattern)
            if connector == "/":
                findings.append({
                    "file": relative,
                    "line": line_num,
                    "token": token,
                    "base": base,
                    "subtype": subtype,
                    "issue": (
                        f"Slash-syntax token '{token}'. "
                        f"Use governed colon syntax or a bare base tag. "
                        f"Register new subtype pairs in "
                        f"references/epistemic/taxonomy.yaml."
                    ),
                })
                continue

            # Colon syntax: base:subtype compound — must be registered
            if subtype is not None:
                pair = f"{base}:{subtype}"
                if pair not in registered_pairs:
                    findings.append({
                        "file": relative,
                        "line": line_num,
                        "token": token,
                        "base": base,
                        "subtype": subtype,
                        "issue": (
                            f"Unregistered subtype pair '{pair}'. "
                            f"Add to references/epistemic/taxonomy.yaml or "
                            f"use a bare '{base}' tag."
                        ),
                    })
                continue

            # Bare tag (no colon, no slash)
            if base not in canonical_base:
                findings.append({
                    "file": relative,
                    "line": line_num,
                    "token": token,
                    "base": base,
                    "subtype": None,
                    "issue": (
                        f"Undeclared base tag '[{base}]'. "
                        f"Canonical base tags are: "
                        f"{', '.join(sorted(canonical_base))}"
                    ),
                })

    return findings


# ── Lint entry point ──────────────────────────────────────────────────────────


def run_lint(
    ws_root: Path,
    paths: Optional[List[str]] = None,
    quiet: bool = False,
    allowlist_path: Optional[str] = None,
) -> int:
    """Run the epistemic lint and return an exit code.

    Returns 0 if no issues found, 1 if issues were found.
    """
    taxonomy = load_taxonomy(ws_root)
    if taxonomy is None:
        print(
            "Error: Cannot load taxonomy from references/epistemic/taxonomy.yaml. "
            "Create it or check the file format.",
            file=sys.stderr,
        )
        return 2

    canonical_base, registered_pairs = _build_tag_sets(taxonomy)

    if not quiet:
        print(f"Canonical base tags ({len(canonical_base)}): "
              f"{', '.join(sorted(canonical_base))}")
        print(f"Registered subtype pairs ({len(registered_pairs)}): "
              f"{', '.join(sorted(registered_pairs))}")
        print()

    # Load allowlist
    ignore_tokens: Set[str] = set()
    ignore_file_globs: List[str] = []
    if allowlist_path is None:
        # Default: look for allowlist in standard location
        allowlist_data = load_allowlist(ws_root)
    elif allowlist_path.lower() == "none":
        allowlist_data = None
    else:
        # Custom path
        alt_path = ws_root / allowlist_path
        if alt_path.exists():
            if yaml is not None:
                try:
                    with open(alt_path, "r", encoding="utf-8") as f:
                        allowlist_data = yaml.safe_load(f)
                except Exception:
                    allowlist_data = None
            else:
                allowlist_data = None
        else:
            allowlist_data = None

    if allowlist_data is not None:
        ignore_tokens, ignore_file_globs = _build_allowlist_sets(allowlist_data)
        if not quiet:
            print(f"Allowlist loaded: {len(ignore_tokens)} ignored tokens, "
                  f"{len(ignore_file_globs)} ignored file patterns")
            print()

    files = _gather_files(ws_root, paths)
    if not quiet:
        print(f"Scanning {len(files)} file(s)...")
        print()

    all_findings: List[dict] = []
    for file_path in files:
        findings = _scan_file_for_tags(
            file_path, canonical_base, registered_pairs,
            ignore_tokens=ignore_tokens,
            ignore_file_globs=ignore_file_globs,
        )
        all_findings.extend(findings)
        for f in findings:
            print(f"{f['file']}:{f['line']}: {f['issue']}")
            print(f"    Token: {f['token']}")
            print()

    if not all_findings:
        if not quiet:
            print("No issues found.")
        return 0

    summary = (
        f"Found {len(all_findings)} issue(s) across "
        f"{len({f['file'] for f in all_findings})} file(s)."
    )
    print(summary)
    return 1


# ── CLI integration ───────────────────────────────────────────────────────────


def cmd_epistemic_lint(args) -> int:
    """``ws epistemic lint`` command entry point."""
    ws_root = _find_workspace_root()
    if ws_root is None:
        print(
            "Error: Cannot find workspace root (no .git or .work-studio/ found).",
            file=sys.stderr,
        )
        return 1
    allowlist = getattr(args, 'allowlist', None)
    return run_lint(ws_root, paths=args.paths if args.paths else None,
                    allowlist_path=allowlist)
