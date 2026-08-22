"""Business operating pipeline graph projection.

Turns ``references/BUSINESS-OPERATING-PIPELINE.md`` into a deterministic
runtime projection without making that projection canonical truth. The source
document remains the canonical business-routing reference; this module gives
the runtime a typed, queryable view for tracer work:

- NetworkX DiGraph of business/governance route nodes.
- Pydantic handoff envelope for business-to-business routing proposals.
- Frontier router that maps a plain-language business frontier to the owning
  skill from the canonical ownership map.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, TypedDict

import networkx as nx
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel, ConfigDict, Field, model_validator

from tools.ws.component_governance import governance_domain_for_skill

_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PIPELINE_REFERENCE = _REPO_ROOT / "references" / "BUSINESS-OPERATING-PIPELINE.md"

_SKILL_RE = re.compile(r"\b(?:alawas-)?(?:business|governance)-[a-z0-9-]+\b")
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "as",
        "by",
        "for",
        "from",
        "in",
        "of",
        "or",
        "the",
        "to",
        "when",
        "with",
    }
)


def normalize_skill_name(name: str) -> str:
    """Normalize adapter skill names to core runtime skill names."""
    if name.startswith("alawas-"):
        return name.removeprefix("alawas-")
    return name


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in _STOPWORDS
    }


@dataclass(frozen=True)
class BusinessPipelineSpec:
    """Parsed canonical business pipeline reference."""

    route: List[str]
    ownership_map: Dict[str, str]


class BusinessFrontierRoute(BaseModel):
    """Deterministic route result for a plain-language business frontier."""

    model_config = ConfigDict(extra="forbid")

    frontier: str
    owning_skill: str
    matched_frontier: str
    confidence: str
    evidence: str


class BusinessHandoffEnvelope(BaseModel):
    """Typed runtime proposal for a business operating-pipeline handoff.

    This is runtime-plane evidence only. It validates the proposed skill/domain
    pairing, but does not write canonical Work Object state or grant authority.
    """

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    work_object_id: str
    lifecycle_state: str
    current_frontier: str
    from_skill: str
    to_skill: str
    governance_domain: str = "business"
    evidence_resolved: List[str] = Field(default_factory=list)
    next_gap: str
    same_work_object: bool
    authority_boundary: str
    graph_path: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_business_handoff(self) -> "BusinessHandoffEnvelope":
        self.from_skill = normalize_skill_name(self.from_skill)
        self.to_skill = normalize_skill_name(self.to_skill)
        expected = governance_domain_for_skill(self.to_skill)
        if expected != self.governance_domain:
            raise ValueError(
                f"business handoff target {self.to_skill} has governance "
                f"domain {expected}, not {self.governance_domain}"
            )
        if self.graph_path:
            self.graph_path = [normalize_skill_name(skill) for skill in self.graph_path]
            if self.graph_path[-1] != self.to_skill:
                raise ValueError("graph_path must end at to_skill")
            if self.from_skill not in self.graph_path:
                raise ValueError("graph_path must include from_skill")
        return self


def _section_after_heading(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.index(marker)
    rest = text[start + len(marker):]
    next_heading = rest.find("\n## ")
    return rest if next_heading == -1 else rest[:next_heading]


def _parse_route(text: str) -> List[str]:
    section = _section_after_heading(text, "Canonical route")
    in_block = False
    route: List[str] = []
    for raw in section.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            continue
        match = _SKILL_RE.search(line)
        if match:
            route.append(normalize_skill_name(match.group(0)))
    if len(route) < 2:
        raise ValueError("business pipeline reference has no parseable route")
    return route


def _parse_ownership_map(text: str) -> Dict[str, str]:
    section = _section_after_heading(text, "Ownership map")
    ownership: Dict[str, str] = {}
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower().startswith("business frontier"):
            continue
        frontier = cells[0]
        skills = [normalize_skill_name(s) for s in _SKILL_RE.findall(cells[1])]
        if skills:
            ownership[frontier] = skills[0]
    if not ownership:
        raise ValueError("business pipeline reference has no parseable ownership map")
    return ownership


def load_business_pipeline_spec(
    reference_path: Path = DEFAULT_PIPELINE_REFERENCE,
) -> BusinessPipelineSpec:
    """Parse the canonical business operating-pipeline reference."""
    text = reference_path.read_text(encoding="utf-8")
    return BusinessPipelineSpec(
        route=_parse_route(text),
        ownership_map=_parse_ownership_map(text),
    )


def build_business_skill_graph(
    spec: Optional[BusinessPipelineSpec] = None,
) -> nx.DiGraph:
    """Build a deterministic NetworkX graph from the canonical route."""
    spec = spec or load_business_pipeline_spec()
    graph = nx.DiGraph()
    for index, skill in enumerate(dict.fromkeys(spec.route)):
        graph.add_node(
            skill,
            order=index,
            governance_domain=governance_domain_for_skill(skill),
        )
    for source, target in zip(spec.route, spec.route[1:]):
        graph.add_edge(source, target, kind="business_operating_handoff")
    return graph


def route_business_frontier(
    frontier: str,
    spec: Optional[BusinessPipelineSpec] = None,
) -> BusinessFrontierRoute:
    """Route a plain-language frontier to the owning business skill.

    Missing matches are reported as low confidence instead of invented
    certainty; callers can then route to the conductor or ask for clarification.
    """
    spec = spec or load_business_pipeline_spec()
    query_tokens = _tokens(frontier)
    best_frontier = ""
    best_skill = "business-formulate-strategy"
    best_score = 0
    for candidate, skill in spec.ownership_map.items():
        score = len(query_tokens & _tokens(candidate))
        if score > best_score:
            best_frontier = candidate
            best_skill = skill
            best_score = score
    if best_score == 0:
        return BusinessFrontierRoute(
            frontier=frontier,
            owning_skill=best_skill,
            matched_frontier="",
            confidence="low",
            evidence="no ownership-map token overlap; defaulted to strategy",
        )
    confidence = "high" if best_score >= 2 else "medium"
    return BusinessFrontierRoute(
        frontier=frontier,
        owning_skill=best_skill,
        matched_frontier=best_frontier,
        confidence=confidence,
        evidence=f"matched {best_score} token(s) in ownership map",
    )


def business_path(
    source_skill: str,
    target_skill: str,
    graph: Optional[nx.DiGraph] = None,
) -> List[str]:
    """Return the shortest deterministic path through the business graph."""
    graph = graph or build_business_skill_graph()
    source = normalize_skill_name(source_skill)
    target = normalize_skill_name(target_skill)
    return list(nx.shortest_path(graph, source, target))


def propose_business_handoff(
    *,
    handoff_id: str,
    work_object_id: str,
    lifecycle_state: str,
    current_frontier: str,
    from_skill: str,
    evidence_resolved: Iterable[str],
    next_gap: str,
    same_work_object: bool,
    authority_boundary: str,
    spec: Optional[BusinessPipelineSpec] = None,
) -> BusinessHandoffEnvelope:
    """Build a validated runtime proposal for the next business skill."""
    spec = spec or load_business_pipeline_spec()
    route = route_business_frontier(next_gap, spec)
    graph = build_business_skill_graph(spec)
    path = business_path(from_skill, route.owning_skill, graph)
    return BusinessHandoffEnvelope(
        handoff_id=handoff_id,
        work_object_id=work_object_id,
        lifecycle_state=lifecycle_state,
        current_frontier=current_frontier,
        from_skill=from_skill,
        to_skill=route.owning_skill,
        governance_domain=governance_domain_for_skill(route.owning_skill),
        evidence_resolved=list(evidence_resolved),
        next_gap=next_gap,
        same_work_object=same_work_object,
        authority_boundary=authority_boundary,
        graph_path=path,
    )


class BusinessRouterState(TypedDict, total=False):
    """Checkpointed state for the business operating router."""

    work_object_id: str
    thread_id: str
    lifecycle_state: str
    current_frontier: str
    from_skill: str
    evidence_resolved: List[str]
    next_gap: str
    same_work_object: bool
    authority_boundary: str
    route_result: dict
    graph_path: List[str]
    handoff_envelope: dict
    director_approved: bool


def build_business_checkpoint_serializer() -> JsonPlusSerializer:
    """Build the business-router checkpoint serializer without pickle fallback."""
    return JsonPlusSerializer(
        pickle_fallback=False,
        allowed_msgpack_modules=None,
    )


def recover_business_checkpoint_db(checkpoint_db: Path) -> str:
    """Prepare a runtime-only checkpoint DB for the business router."""
    checkpoint_db.parent.mkdir(parents=True, exist_ok=True)
    if not checkpoint_db.exists():
        return "created_missing"
    try:
        with sqlite3.connect(str(checkpoint_db)) as conn:
            row = conn.execute("PRAGMA quick_check").fetchone()
    except sqlite3.DatabaseError:
        row = None
    if row and row[0] == "ok":
        return "usable"
    quarantine = checkpoint_db.with_name(f"{checkpoint_db.name}.corrupt")
    if quarantine.exists():
        quarantine.unlink()
    checkpoint_db.replace(quarantine)
    return "quarantined_corrupt"


def business_router_classify_frontier(state: BusinessRouterState) -> dict:
    """Classify the next business gap against the canonical ownership map."""
    route = route_business_frontier(state["next_gap"])
    return {"route_result": route.model_dump()}


def business_router_validate_authority(state: BusinessRouterState) -> dict:
    """Validate that this router remains a read-only proposal path."""
    boundary = state.get("authority_boundary", "")
    allowed = {"read-only", "read-only-propose", "governed"}
    if boundary not in allowed:
        raise ValueError(f"unsupported business router authority boundary: {boundary}")
    return {"authority_boundary": boundary}


def business_router_route_skill(state: BusinessRouterState) -> dict:
    """Resolve a graph path from the current skill to the routed skill."""
    route = BusinessFrontierRoute(**state["route_result"])
    path = business_path(state["from_skill"], route.owning_skill)
    return {"graph_path": path}


def business_router_propose_handoff(state: BusinessRouterState) -> dict:
    """Emit the strict runtime business handoff proposal."""
    envelope = propose_business_handoff(
        handoff_id=f"BUSINESS-HANDOFF-{state['work_object_id']}-{state['thread_id']}",
        work_object_id=state["work_object_id"],
        lifecycle_state=state["lifecycle_state"],
        current_frontier=state["current_frontier"],
        from_skill=state["from_skill"],
        evidence_resolved=state.get("evidence_resolved", []),
        next_gap=state["next_gap"],
        same_work_object=state["same_work_object"],
        authority_boundary=state["authority_boundary"],
    )
    return {"handoff_envelope": envelope.model_dump()}


def business_router_director_gate(state: BusinessRouterState) -> dict:
    """Checkpoint and pause for director approval of the proposed handoff."""
    approval = interrupt(
        {
            "reason": "approve business handoff proposal",
            "handoff_envelope": state["handoff_envelope"],
            "ask": "approve this business handoff proposal?",
        }
    )
    return {"director_approved": bool(approval)}


def build_business_router_graph(checkpoint_db: Path):
    """Build the checkpointed LangGraph business operating router."""
    recover_business_checkpoint_db(checkpoint_db)
    builder = StateGraph(BusinessRouterState)
    builder.add_node("classify_frontier", business_router_classify_frontier)
    builder.add_node("validate_authority", business_router_validate_authority)
    builder.add_node("route_skill", business_router_route_skill)
    builder.add_node("propose_handoff", business_router_propose_handoff)
    builder.add_node("director_gate", business_router_director_gate)
    builder.add_edge(START, "classify_frontier")
    builder.add_edge("classify_frontier", "validate_authority")
    builder.add_edge("validate_authority", "route_skill")
    builder.add_edge("route_skill", "propose_handoff")
    builder.add_edge("propose_handoff", "director_gate")
    builder.add_edge("director_gate", END)
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_business_checkpoint_serializer())
    return builder.compile(checkpointer=saver), conn


def _business_router_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def run_business_router(
    *,
    work_object_id: str,
    thread_id: str,
    lifecycle_state: str,
    current_frontier: str,
    from_skill: str,
    evidence_resolved: Iterable[str],
    next_gap: str,
    same_work_object: bool,
    authority_boundary: str,
    checkpoint_db: Path,
    approve: Optional[bool] = None,
) -> dict:
    """Run or resume the checkpointed business router.

    ``approve=None`` starts a fresh proposal and pauses at the director gate.
    ``approve=True`` or ``False`` resumes the paused thread with the director's
    decision. No node writes canonical state or touches live business systems.
    """
    graph, conn = build_business_router_graph(checkpoint_db)
    try:
        if approve is not None:
            return graph.invoke(
                Command(resume=approve),
                config=_business_router_config(thread_id),
            )
        return graph.invoke(
            {
                "work_object_id": work_object_id,
                "thread_id": thread_id,
                "lifecycle_state": lifecycle_state,
                "current_frontier": current_frontier,
                "from_skill": from_skill,
                "evidence_resolved": list(evidence_resolved),
                "next_gap": next_gap,
                "same_work_object": same_work_object,
                "authority_boundary": authority_boundary,
            },
            config=_business_router_config(thread_id),
        )
    finally:
        conn.close()


def inspect_business_router(thread_id: str, checkpoint_db: Path) -> dict:
    """Inspect one business-router thread's checkpoint state."""
    recovery = recover_business_checkpoint_db(checkpoint_db)
    summary = {
        "thread_id": thread_id,
        "checkpoint_db": str(checkpoint_db),
        "recovery": recovery,
        "awaiting_approval": False,
        "has_handoff_envelope": False,
    }
    if recovery not in {"usable", "created_missing"}:
        return summary
    graph, conn = build_business_router_graph(checkpoint_db)
    try:
        snapshot = graph.get_state(_business_router_config(thread_id))
        values = snapshot.values or {}
        summary.update(
            {
                "values": dict(values),
                "next": list(snapshot.next),
                "awaiting_approval": bool(snapshot.interrupts),
                "has_handoff_envelope": bool(values.get("handoff_envelope")),
            }
        )
        return summary
    finally:
        conn.close()


def cleanup_business_router_temp(path: Path) -> None:
    """Best-effort cleanup helper for Windows SQLite-handle tests."""
    shutil.rmtree(path, ignore_errors=True)


def _json_default(value):
    return str(value)


def _print_json(value: dict) -> None:
    print(json.dumps(value, sort_keys=True, default=_json_default))


def _split_evidence(raw: str) -> List[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(";") if part.strip()]


def main(argv: Optional[list[str]] = None) -> int:
    """CLI surface for the checkpointed business router.

    This intentionally lives on ``python -m runtime.business`` for the tracer
    slice. Promoting it into ``runtime.graph``'s broader command surface remains
    a separate integration decision.
    """
    parser = argparse.ArgumentParser(
        description="Run or inspect the checkpointed business operating router."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run-router",
        help="Start or resume a checkpointed business handoff proposal",
    )
    run_parser.add_argument("--work-object-id", required=True)
    run_parser.add_argument("--thread-id", required=True)
    run_parser.add_argument("--checkpoint-db", required=True)
    run_parser.add_argument("--lifecycle-state", default="build")
    run_parser.add_argument("--current-frontier", default="")
    run_parser.add_argument("--from-skill", default="business-formulate-strategy")
    run_parser.add_argument("--evidence-resolved", default="")
    run_parser.add_argument("--next-gap", default="")
    run_parser.add_argument("--linked-work-object", action="store_true")
    run_parser.add_argument("--authority-boundary", default="read-only-propose")
    approval = run_parser.add_mutually_exclusive_group()
    approval.add_argument("--approve", action="store_true")
    approval.add_argument("--reject", action="store_true")

    inspect_parser = subparsers.add_parser(
        "inspect-router",
        help="Inspect one checkpointed business-router thread",
    )
    inspect_parser.add_argument("--thread-id", required=True)
    inspect_parser.add_argument("--checkpoint-db", required=True)

    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.command == "inspect-router":
        _print_json(inspect_business_router(args.thread_id, Path(args.checkpoint_db)))
        return 0

    if args.command == "run-router":
        approve: Optional[bool]
        if args.approve:
            approve = True
        elif args.reject:
            approve = False
        else:
            approve = None
            if not args.next_gap:
                print(
                    "Error: --next-gap is required for a fresh business-router run",
                    file=sys.stderr,
                )
                return 2
        try:
            result = run_business_router(
                work_object_id=args.work_object_id,
                thread_id=args.thread_id,
                lifecycle_state=args.lifecycle_state,
                current_frontier=args.current_frontier,
                from_skill=args.from_skill,
                evidence_resolved=_split_evidence(args.evidence_resolved),
                next_gap=args.next_gap,
                same_work_object=not args.linked_work_object,
                authority_boundary=args.authority_boundary,
                checkpoint_db=Path(args.checkpoint_db),
                approve=approve,
            )
        except Exception as exc:
            print(f"Error: business router failed: {exc}", file=sys.stderr)
            return 1
        _print_json(result)
        return 0

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
