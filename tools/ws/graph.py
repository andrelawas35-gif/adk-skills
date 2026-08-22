"""Read-only Relationship-edge trace across the Work Object corpus.

Tracer bullet for WO 2026-08-22-026, Decision 1. Deliberately the smallest
possible projection: parse each Work Object's ``## Relationships`` section
(written by ``ws relation add``) and print the edges touching one reference.
No NetworkX, no in-memory graph, no invariant checks beyond what a missing
edge already implies -- see WO 2026-08-22-026 Decision 1 non-goals.

Per the evidence model (``references/EVIDENCE-MODEL.md``) and graph
invariant #6 (architecture section 3.4): an edge not found here means
"not recorded", never "false". This command never asserts an edge's
absence proves anything beyond its own coverage.

One CLI command:
    - ``ws graph trace <ref> [--direction upstream|downstream]``
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

from .relation import parse_relationships, normalize_ref


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ directory."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _collect_all_edges(objects_dir: Path) -> List[Dict[str, str]]:
    """Scan the full corpus and return every parsed Relationship edge.

    Deterministic: sorted file order, matching validate.py's established
    full-corpus scan idiom (``objects_dir.rglob("*.md")``, sorted). A file
    that cannot be read or parsed is skipped, not fatal -- consistent with
    the rest of the CLI's advisory/read-only projections.
    """
    edges: List[Dict[str, str]] = []
    for obj_file in sorted(objects_dir.rglob("*.md")):
        try:
            content = obj_file.read_text(encoding="utf-8")
        except Exception:
            continue
        body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content
        for edge in parse_relationships(body):
            edge["_source_file"] = str(obj_file.relative_to(objects_dir.parent.parent))
            edges.append(edge)
    return edges


# ═══════════════════════════════════════════════════════════════════════════════
# ws graph trace
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_graph_trace(args: argparse.Namespace) -> int:
    """Print Relationship edges touching one ref, from the full corpus."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    target_ref = normalize_ref(args.ref)
    if target_ref is None:
        print(
            f"Error: '{args.ref}' does not resolve. "
            "Use a Work Object ID (YYYY-MM-DD-NNN, with or without a 'wo:' "
            "prefix) or an explicit 'external:<locator>' reference.",
            file=sys.stderr,
        )
        return 1

    direction = getattr(args, "direction", None) or "both"
    if direction not in ("upstream", "downstream", "both"):
        print(
            f"Error: Invalid --direction '{direction}'. "
            "Must be one of: upstream, downstream, both.",
            file=sys.stderr,
        )
        return 1

    all_edges = _collect_all_edges(objects_dir)

    downstream = [e for e in all_edges if e.get("from") == target_ref]
    upstream = [e for e in all_edges if e.get("to") == target_ref]

    show_downstream = direction in ("downstream", "both")
    show_upstream = direction in ("upstream", "both")

    total = (len(downstream) if show_downstream else 0) + (len(upstream) if show_upstream else 0)

    if total == 0:
        print(
            f"No edges found touching {target_ref}. "
            "This means not recorded, not necessarily absent -- the graph is "
            "a projection over what has been written with 'ws relation add'."
        )
        return 0

    print(f"Edges touching {target_ref} ({total} total):")
    print()

    if show_downstream and downstream:
        print(f"  Downstream (from {target_ref}):")
        for e in downstream:
            print(f"    {e.get('id', '?')}  --[{e.get('type', '?')}]-->  {e.get('to', '?')}")
            basis = e.get("basis")
            if basis:
                print(f"      basis: {basis}")
            print(f"      source: {e.get('_source_file', '?')}")
        print()

    if show_upstream and upstream:
        print(f"  Upstream (into {target_ref}):")
        for e in upstream:
            print(f"    {e.get('id', '?')}  {e.get('from', '?')}  --[{e.get('type', '?')}]-->")
            basis = e.get("basis")
            if basis:
                print(f"      basis: {basis}")
            print(f"      source: {e.get('_source_file', '?')}")
        print()

    return 0
