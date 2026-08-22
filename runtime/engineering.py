"""Engineering operating pipeline graph projection.

Turns ``references/ENGINEERING-OPERATING-PIPELINE.md`` into a deterministic
runtime projection without making that projection canonical truth. The source
document remains the canonical engineering-routing reference; this module gives
the runtime a typed, queryable view for tracer work:

- NetworkX DiGraph of design/engineering/operations/governance route nodes.
- Pydantic handoff envelope for engineering operating-pipeline proposals.
- Frontier router that maps plain-language engineering frontiers to the owning
  skill from the canonical ownership map.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import networkx as nx
from pydantic import BaseModel, ConfigDict, Field, model_validator

from tools.ws.component_governance import governance_domain_for_skill

_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PIPELINE_REFERENCE = (
    _REPO_ROOT / "references" / "ENGINEERING-OPERATING-PIPELINE.md"
)

_SKILL_RE = re.compile(
    r"\b(?:alawas-)?(?:design|engineering|operations|governance)-[a-z0-9-]+\b"
)
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
class EngineeringPipelineSpec:
    """Parsed canonical engineering operating-pipeline reference."""

    route: List[str]
    ownership_map: Dict[str, str]


class EngineeringFrontierRoute(BaseModel):
    """Deterministic route result for a plain-language engineering frontier."""

    model_config = ConfigDict(extra="forbid")

    frontier: str
    owning_skill: str
    matched_frontier: str
    confidence: str
    evidence: str


class EngineeringHandoffEnvelope(BaseModel):
    """Typed runtime proposal for an engineering operating-pipeline handoff.

    This is runtime-plane evidence only. It validates the proposed skill/domain
    pairing, but does not write canonical Work Object state, mutate CI/CD, or
    grant deployment authority.
    """

    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    work_object_id: str
    lifecycle_state: str
    current_frontier: str
    from_skill: str
    to_skill: str
    governance_domain: str
    evidence_resolved: List[str] = Field(default_factory=list)
    next_gap: str
    same_work_object: bool
    authority_boundary: str
    graph_path: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_engineering_handoff(self) -> "EngineeringHandoffEnvelope":
        self.from_skill = normalize_skill_name(self.from_skill)
        self.to_skill = normalize_skill_name(self.to_skill)
        expected = governance_domain_for_skill(self.to_skill)
        if expected != self.governance_domain:
            raise ValueError(
                f"engineering handoff target {self.to_skill} has governance "
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
        raise ValueError("engineering pipeline reference has no parseable route")
    return route


def _parse_ownership_map(text: str) -> Dict[str, str]:
    section = _section_after_heading(text, "Ownership map")
    ownership: Dict[str, str] = {}
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower().startswith("engineering frontier"):
            continue
        frontier = cells[0]
        skills = [normalize_skill_name(s) for s in _SKILL_RE.findall(cells[1])]
        if skills:
            ownership[frontier] = skills[0]
    if not ownership:
        raise ValueError("engineering pipeline reference has no parseable ownership map")
    return ownership


def load_engineering_pipeline_spec(
    reference_path: Path = DEFAULT_PIPELINE_REFERENCE,
) -> EngineeringPipelineSpec:
    """Parse the canonical engineering operating-pipeline reference."""
    text = reference_path.read_text(encoding="utf-8")
    return EngineeringPipelineSpec(
        route=_parse_route(text),
        ownership_map=_parse_ownership_map(text),
    )


def build_engineering_skill_graph(
    spec: Optional[EngineeringPipelineSpec] = None,
) -> nx.DiGraph:
    """Build a deterministic NetworkX graph from the canonical route."""
    spec = spec or load_engineering_pipeline_spec()
    graph = nx.DiGraph()
    for index, skill in enumerate(dict.fromkeys(spec.route)):
        graph.add_node(
            skill,
            order=index,
            governance_domain=governance_domain_for_skill(skill),
        )
    for source, target in zip(spec.route, spec.route[1:]):
        graph.add_edge(source, target, kind="engineering_operating_handoff")
    return graph


def route_engineering_frontier(
    frontier: str,
    spec: Optional[EngineeringPipelineSpec] = None,
) -> EngineeringFrontierRoute:
    """Route a plain-language engineering frontier to the owning skill."""
    spec = spec or load_engineering_pipeline_spec()
    query_tokens = _tokens(frontier)
    best_frontier = ""
    best_skill = "engineering-implement-bounded-change"
    best_score = 0
    for candidate, skill in spec.ownership_map.items():
        score = len(query_tokens & _tokens(candidate))
        if score > best_score:
            best_frontier = candidate
            best_skill = skill
            best_score = score
    if best_score == 0:
        return EngineeringFrontierRoute(
            frontier=frontier,
            owning_skill=best_skill,
            matched_frontier="",
            confidence="low",
            evidence="no ownership-map token overlap; defaulted to bounded implementation",
        )
    confidence = "high" if best_score >= 2 else "medium"
    return EngineeringFrontierRoute(
        frontier=frontier,
        owning_skill=best_skill,
        matched_frontier=best_frontier,
        confidence=confidence,
        evidence=f"matched {best_score} token(s) in ownership map",
    )


def engineering_path(
    source_skill: str,
    target_skill: str,
    graph: Optional[nx.DiGraph] = None,
) -> List[str]:
    """Return the shortest deterministic path through the engineering graph."""
    graph = graph or build_engineering_skill_graph()
    source = normalize_skill_name(source_skill)
    target = normalize_skill_name(target_skill)
    return list(nx.shortest_path(graph, source, target))


def propose_engineering_handoff(
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
    spec: Optional[EngineeringPipelineSpec] = None,
) -> EngineeringHandoffEnvelope:
    """Build a validated runtime proposal for the next engineering skill."""
    spec = spec or load_engineering_pipeline_spec()
    route = route_engineering_frontier(next_gap, spec)
    graph = build_engineering_skill_graph(spec)
    path = engineering_path(from_skill, route.owning_skill, graph)
    return EngineeringHandoffEnvelope(
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
