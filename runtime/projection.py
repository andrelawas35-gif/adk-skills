"""Deterministic edge projection from Work Object envelopes (WO 2026-08-17-007).

Phase 5, bounded slices (WO 2026-08-17-007): build an in-memory NetworkX DiGraph
of Work Object edges extracted deterministically from the 4 envelope edge
fields (``responds_to`` / ``supersedes`` / ``superseded_by`` / ``unblocks``)
and run the graph-checker invariants. Slice 1 (Decision 2): #1 (dangling
endpoints), #3 (reciprocal agreement), #7 (byte-stable rebuild). Slice 2
(Decision 3): #4 (acyclic supersession, with supersedes/superseded_by direction
normalization) plus an advisory-only cycle report for responds_to/unblocks. Slice 3
(Decision 4): #8 (stale locators) -- each edge carries ``target_identity``, the
SHA-256 of the target object file's bytes at projection time, and
``check_stale_locators`` reports recorded-vs-current identity mismatches. Slice 4
(Decision 5): the Phase 5 queries -- ``explanation_paths`` (deterministic edge-chain
explanations between two WO ids) and ``loop_state`` (the loop reducer: deterministic
enumeration of every simple cycle in the full graph). Slice 5 (Decision 6): invariant
#9 -- sensitive-body exclusion; extraction is frontmatter-only (``parse_frontmatter``,
never bodies), so sensitive source bodies, prompts, and hidden reasoning are excluded
by construction and the property is guarded by tests. Slice 6 (Decision 7):
completion -- #2 declared edge source/target-kind pairs, #5 per-edge extraction rule,
#6 missing-coverage reporting, #10 conformance-not-adequacy disclaimer.

Read-only by construction (ADR 0025): walks canonical ``.work-studio/objects/``
markdown files only (``.bak-*`` siblings are not ``.md`` so never matched) and
never writes canonical state. ``tools/ws`` stays stdlib; this runtime module
may use libraries (networkx). Extraction reuses the single-source
``tools/ws/schema.py`` frontmatter parser (same pattern as
``runtime/envelope.py``).

Run (from repo root, uv-managed Python 3.11):
    uv run python -m unittest runtime.tests.test_projection -v
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

import networkx as nx

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.ws.schema import parse_frontmatter  # noqa: E402

_WO_ID_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}-\d{3})\b")
EDGE_FIELDS = ("responds_to", "supersedes", "superseded_by", "unblocks")

# Invariant #2: every edge type declares its source and target kinds. With
# WO-only extraction all endpoints are Work Objects ("wo"); the meaningful
# non-WO cases are deferred until such nodes exist (open question 2).
EDGE_KIND_PAIRS: Dict[str, Tuple[str, str]] = {
    "responds_to": ("wo", "wo"),
    "supersedes": ("wo", "wo"),
    "superseded_by": ("wo", "wo"),
    "unblocks": ("wo", "wo"),
}

# Invariant #10: conformance reports graph mechanics only, never adequacy.
CONFORMANCE_DISCLAIMER = (
    "# conformance reports graph mechanics only; it does not assert evidence "
    "adequacy, correctness, safety, readiness, or authority (invariant #10)"
)


@dataclass(frozen=True)
class Edge:
    """A typed directed edge between Work Object ids.

    Carries ``target_identity`` (invariant #8): the SHA-256 hex digest of the
    target object file's bytes at projection time, or ``None`` for missing or
    external (dangling) targets.
    """

    source: str
    target: str
    kind: str
    target_identity: Optional[str] = None
    extraction_rule: Optional[str] = None


def _extract_wo_id(value: str) -> str | None:
    """Extract the leading Work Object id from an edge-field value.

    Field values may carry trailing prose (e.g. ``2026-07-22-003 (diagnosis
    session -- backtick-wrapped tag fix)``); the leading ``YYYY-MM-DD-NNN``
    is the edge endpoint.
    """
    m = _WO_ID_RE.search(value)
    return m.group(1) if m else None


def iter_object_files(objects_dir: Path) -> Iterable[Path]:
    """Yield canonical Work Object files in deterministic (sorted) order.

    ``.bak-<ts>`` snapshot siblings are excluded defensively so extraction
    never invents phantom nodes from stale copies (they end in ``.bak-*``,
    not ``.md``, so the ``*.md`` glob already excludes them).
    """
    for p in sorted(objects_dir.rglob("*.md")):
        if ".bak-" in p.name:
            continue
        yield p


def _index_objects(objects_dir: Path) -> Dict[str, Tuple[dict, Path]]:
    """Parse canonical object frontmatter once; return {id: (fm, path)}."""
    index: Dict[str, Tuple[dict, Path]] = {}
    for path in iter_object_files(objects_dir):
        try:
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        wid = fm.get("id")
        if wid:
            index[str(wid)] = (fm, path)
    return index


def _parse_objects(objects_dir: Path) -> Dict[str, dict]:
    """Parse canonical object frontmatter once; return {id: frontmatter}."""
    return {wid: fm for wid, (fm, _path) in _index_objects(objects_dir).items()}


def _content_identity(
    index: Dict[str, Tuple[dict, Path]], target: str
) -> str | None:
    """Full SHA-256 hex digest of the target object file's bytes (invariant #8).

    ``None`` for a target that is not present as a canonical object (dangling
    or external endpoint) -- there is no content identity to record.
    """
    entry = index.get(target)
    if entry is None:
        return None
    try:
        return hashlib.sha256(entry[1].read_bytes()).hexdigest()
    except OSError:
        return None


def extract_edges(objects_dir: Path) -> List[Edge]:
    """Deterministically extract typed edges from canonical object frontmatter."""
    return _extract_edges_from_parsed(_parse_objects(objects_dir))


def _extract_edges_from_parsed(parsed: Dict[str, dict]) -> List[Edge]:
    edges: List[Edge] = []
    for wid, fm in parsed.items():
        for field in EDGE_FIELDS:
            raw = fm.get(field)
            if not raw:
                continue
            target = _extract_wo_id(str(raw))
            if target:
                edges.append(
                    Edge(
                        source=wid,
                        target=target,
                        kind=field,
                        extraction_rule=f"frontmatter.{field}",
                    )
                )
    # Deterministic ordering for byte-stable rebuild (invariant #7).
    edges.sort(key=lambda e: (e.source, e.kind, e.target))
    return edges


def build_projection(
    objects_dir: Path,
) -> Tuple[nx.DiGraph, List[Edge], Set[str]]:
    """Build the in-memory DiGraph from canonical objects + extracted edges.

    Returns ``(graph, edges, known_ids)`` where ``known_ids`` is the set of
    WO ids present as canonical object files -- the reference set for
    invariant #1 (an edge endpoint that is not in ``known_ids`` is dangling).
    Each edge carries ``target_identity`` (invariant #8): the SHA-256 of the
    target object file's bytes, or ``None`` for missing/external targets.
    """
    index = _index_objects(objects_dir)
    known_ids = set(index)
    edges: List[Edge] = []
    for wid in sorted(index):
        fm, _path = index[wid]
        for field in EDGE_FIELDS:
            raw = fm.get(field)
            if not raw:
                continue
            target = _extract_wo_id(str(raw))
            if target:
                edges.append(
                    Edge(
                        source=wid,
                        target=target,
                        kind=field,
                        target_identity=_content_identity(index, target),
                        extraction_rule=f"frontmatter.{field}",
                    )
                )
    edges.sort(key=lambda e: (e.source, e.kind, e.target))

    g = nx.DiGraph()
    for wid in sorted(known_ids):
        g.add_node(wid)
    for e in edges:
        g.add_edge(e.source, e.target, kind=e.kind)
    return g, edges, known_ids


def check_dangling_endpoints(edges: List[Edge], known_ids: Set[str]) -> List[str]:
    """Invariant #1: every edge endpoint resolves or is explicitly external."""
    problems: List[str] = []
    for e in sorted(edges, key=lambda e: (e.source, e.kind, e.target)):
        if e.source not in known_ids:
            problems.append(f"dangling source: {e.source} (via {e.kind} -> {e.target})")
        if e.target not in known_ids:
            problems.append(f"dangling target: {e.target} (via {e.kind} from {e.source})")
    return problems


def check_reciprocal_agreement(edges: List[Edge]) -> List[str]:
    """Invariant #3: reciprocal fields agree.

    A ``supersedes`` edge a->b must have a matching ``superseded_by`` edge
    b->a, and vice versa.
    """
    problems: List[str] = []
    supersedes = {(e.source, e.target) for e in edges if e.kind == "supersedes"}
    superseded_by = {
        (e.source, e.target) for e in edges if e.kind == "superseded_by"
    }
    for a, b in sorted(supersedes):
        if (b, a) not in superseded_by:
            problems.append(
                f"supersedes {a}->{b} lacks reciprocal superseded_by {b}->{a}"
            )
    for b, a in sorted(superseded_by):
        if (a, b) not in supersedes:
            problems.append(
                f"superseded_by {b}->{a} lacks reciprocal supersedes {a}->{b}"
            )
    return problems


def supersession_edges(edges: List[Edge]) -> List[Edge]:
    """Normalize supersession edges to a single newer->older direction.

    ``supersedes`` A->B is kept as-is; ``superseded_by`` A->B (A is superseded
    by B) is reversed to B->A. Invariant #3 agreement guarantees these describe
    the same relation, so normalizing cannot flip a genuine cycle direction.
    """
    norm: List[Edge] = []
    for e in edges:
        if e.kind == "supersedes":
            norm.append(e)
        elif e.kind == "superseded_by":
            norm.append(Edge(source=e.target, target=e.source, kind="supersedes"))
    norm.sort(key=lambda e: (e.source, e.kind, e.target))
    return norm


def check_forbidden_cycles(edges: List[Edge]) -> List[str]:
    """Invariant #4: supersession must be acyclic.

    Cycles in the normalized supersession subgraph (and any self-loop) are
    hard problems. ``responds_to``/``unblocks`` are excluded here -- see
    ``check_advisory_cycles`` (their cycle-legality is a deferred question).
    """
    problems: List[str] = []
    norm = supersession_edges(edges)
    sub = nx.DiGraph()
    for e in norm:
        if e.source == e.target:
            problems.append(f"self-loop supersession: {e.source} supersedes itself")
        else:
            sub.add_edge(e.source, e.target, kind=e.kind)
    for cycle in nx.simple_cycles(sub):
        problems.append("supersession cycle: " + " -> ".join(cycle))
    return problems


def check_advisory_cycles(edges: List[Edge]) -> List[str]:
    """Advisory cycle report for responds_to/unblocks (invariant #4 open question).

    Cycle-legality for these kinds is a deferred design question, so cycles
    here are advisory only -- never hard errors.
    """
    advisory: List[str] = []
    for kind in ("responds_to", "unblocks"):
        sub = nx.DiGraph()
        for e in edges:
            if e.kind == kind:
                sub.add_edge(e.source, e.target, kind=kind)
        for cycle in nx.simple_cycles(sub):
            advisory.append(f"{kind} cycle (advisory): " + " -> ".join(cycle))
    return advisory


def check_edge_kind_pairs(edges: List[Edge]) -> List[str]:
    """Invariant #2: every edge type has declared source and target kinds.

    With WO-only extraction every endpoint is a Work Object ("wo"), so the
    declared table is satisfied by construction; the check still fires on an
    undeclared kind (open question 2: exercised by a direct-Edge fixture now,
    meaningful non-WO enforcement deferred until such nodes exist).
    """
    problems: List[str] = []
    for e in sorted(edges, key=lambda e: (e.source, e.kind, e.target)):
        kinds = EDGE_KIND_PAIRS.get(e.kind)
        if kinds is None:
            problems.append(f"undeclared edge kind: {e.source} {e.kind} {e.target}")
        elif kinds != ("wo", "wo"):
            problems.append(
                f"illegal edge pair: {e.kind} {kinds[0]}->{kinds[1]} "
                f"({e.source}->{e.target})"
            )
    return problems


def coverage_report(
    edges: List[Edge], known_ids: Set[str], requested: List[Tuple[str, str]]
) -> List[str]:
    """Invariant #6: a missing edge is missing coverage, never a negative finding.

    For each requested (source, target) pair with no edge in the projection,
    report it as missing coverage -- never as a semantic negative.
    """
    present = {(e.source, e.target) for e in edges}
    report: List[str] = []
    for src, tgt in requested:
        if (src, tgt) not in present:
            report.append(
                f"missing coverage: {src} --?-> {tgt} (no edge; not a negative finding)"
            )
    return report


def check_stale_locators(recorded: List[Edge], current: List[Edge]) -> List[str]:
    """Invariant #8: report edges whose recorded target content identity is stale.

    Matches edges present in both projections (by source+kind+target) and
    reports those whose recorded ``target_identity`` differs from the current
    one. New or removed edges are missing coverage (invariant #6), not stale
    locators; a ``None`` recorded identity (dangling/external at record time)
    has nothing to go stale.
    """
    problems: List[str] = []
    current_by_key = {(e.source, e.kind, e.target): e for e in current}
    for e in sorted(recorded, key=lambda e: (e.source, e.kind, e.target)):
        cur = current_by_key.get((e.source, e.kind, e.target))
        if cur is None:
            continue
        if (
            e.target_identity is not None
            and e.target_identity != cur.target_identity
        ):
            problems.append(
                f"stale locator: {e.source} {e.kind} {e.target} "
                f"(recorded {e.target_identity} != current {cur.target_identity})"
            )
    return problems


def _edge_kinds_between(edges: List[Edge], u: str, v: str) -> List[str]:
    """Kinds of edges from u to v, deterministic (sorted)."""
    return sorted(e.kind for e in edges if e.source == u and e.target == v)


def explanation_paths(
    g: nx.DiGraph, edges: List[Edge], source: str, target: str, limit: int = 10
) -> List[str]:
    """Deterministic explanation paths between two WO ids (invariant #6-friendly).

    Simple paths from ``source`` to ``target``, sorted by length then node
    order, each rendered with the edge kinds per hop (from the ``edges`` list,
    so parallel edges are preserved). ``limit`` caps the number of paths. A
    missing path is reported as such -- missing coverage, never a negative
    semantic finding (invariant #6).
    """
    report: List[str] = []
    if source not in g or target not in g:
        report.append(f"no path: {source} -> {target} (endpoint not in graph)")
        return report
    if not nx.has_path(g, source, target):
        report.append(f"no path: {source} -> {target} (missing coverage)")
        return report
    paths = list(nx.all_simple_paths(g, source, target))
    paths.sort(key=lambda p: (len(p), p))
    for p in paths[:limit]:
        hops = []
        for i in range(len(p) - 1):
            u, v = p[i], p[i + 1]
            kinds = _edge_kinds_between(edges, u, v)
            hops.append(f"{u} -> {v} [{','.join(kinds)}]")
        report.append("path " + " ; ".join(hops))
    return report


def _canonical_cycle(cycle: List[str]) -> List[str]:
    """Rotate a cycle to its lexicographically smallest starting node."""
    if not cycle:
        return cycle
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def loop_state(g: nx.DiGraph, edges: List[Edge]) -> List[str]:
    """Loop reducer: deterministic enumeration of every simple cycle.

    Reports each cycle in the full graph as a kind-labeled chain (facts, per
    invariant #10). Cycles are canonicalized (lexicographically smallest start)
    and sorted. This is the raw-graph view: the agreed reciprocal pair appears
    as a 2-cycle, distinct from #4's normalized-supersession acyclicity.
    """
    report: List[str] = []
    cycles = [_canonical_cycle(list(c)) for c in nx.simple_cycles(g)]
    cycles.sort()
    for c in cycles:
        hops = []
        for i in range(len(c)):
            u, v = c[i], c[(i + 1) % len(c)]
            kinds = _edge_kinds_between(edges, u, v)
            hops.append(f"{u} -> {v} [{','.join(kinds)}]")
        report.append("loop " + " ; ".join(hops))
    return report


def render_projection(g: nx.DiGraph, edges: List[Edge]) -> str:
    """Deterministic sorted text rendering (invariant #7 byte-stable rebuild).

    Frontmatter-only by construction (invariant #9): extraction uses
    ``parse_frontmatter`` and never reads object bodies, so sensitive source
    bodies, prompts, and hidden reasoning are excluded from every projection
    output (guarded by TestSensitiveBodyExclusion). Each edge records its
    extraction rule (invariant #5). The output carries the invariant #10
    disclaimer: conformance asserts graph mechanics only.
    """
    lines = [CONFORMANCE_DISCLAIMER, f"# nodes ({g.number_of_nodes()})"]
    for n in sorted(g.nodes()):
        lines.append(f"node {n}")
    lines.append(f"# edges ({len(edges)})")
    for e in sorted(edges, key=lambda e: (e.source, e.kind, e.target)):
        lines.append(
            f"edge {e.source} {e.target} {e.kind} {e.target_identity or '-'} "
            f"{e.extraction_rule or '-'}"
        )
    return "\n".join(lines) + "\n"
