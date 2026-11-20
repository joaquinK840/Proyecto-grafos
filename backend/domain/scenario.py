from dataclasses import dataclass
from math import isfinite
from typing import Iterable

if __package__.startswith("backend."):
    from ..schemas.scenario_schemas import ScenarioPayload
else:
    from schemas.scenario_schemas import ScenarioPayload


class ScenarioValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ScenarioSummary:
    name: str
    ge_vertex_count: int
    ge_edge_count: int
    gm_vertex_count: int
    gm_edge_count: int
    base_id: str
    entry_id: str
    exit_id: str
    shortest_maze_time: float


def _require_unique_ids(items: Iterable, entity_name: str) -> set[str]:
    ids = set()
    for item in items:
        item_id = item.id
        if item_id in ids:
            raise ScenarioValidationError(
                f"Duplicate {entity_name} identifier: {item_id}"
            )
        ids.add(item_id)
    return ids


def _validate_coordinates(payload: ScenarioPayload) -> None:
    for vertex in payload.ge.vertices:
        if not isfinite(vertex.x) or vertex.x <= 0:
            raise ScenarioValidationError(
                f"GE vertex {vertex.id} must have a positive finite x coordinate"
            )
        if not isfinite(vertex.y) or vertex.y <= 0:
            raise ScenarioValidationError(
                f"GE vertex {vertex.id} must have a positive finite y coordinate"
            )
    for vertex in payload.gm.vertices:
        if not isfinite(vertex.x) or not isfinite(vertex.y):
            raise ScenarioValidationError(
                f"GM vertex {vertex.id} must have finite coordinates"
            )


def _validate_edge_endpoints(
    edges: Iterable,
    vertex_ids: set[str],
    graph_name: str,
) -> None:
    seen_edge_ids = set()
    for edge in edges:
        if edge.id in seen_edge_ids:
            raise ScenarioValidationError(
                f"Duplicate {graph_name} edge identifier: {edge.id}"
            )
        seen_edge_ids.add(edge.id)
        if edge.v1 not in vertex_ids or edge.v2 not in vertex_ids:
            raise ScenarioValidationError(
                f"{graph_name} edge {edge.id} references an unknown vertex"
            )
        if edge.v1 == edge.v2:
            raise ScenarioValidationError(
                f"{graph_name} edge {edge.id} cannot connect a vertex to itself"
            )


def _validate_ge_edges(payload: ScenarioPayload) -> None:
    for edge in payload.ge.edges:
        if edge.connection_type.value == "bridge":
            if edge.max_resistance is None:
                raise ScenarioValidationError(
                    f"GE bridge {edge.id} requires max_resistance"
                )
            if edge.current_resistance is not None:
                if edge.current_resistance > edge.max_resistance:
                    raise ScenarioValidationError(
                        f"GE bridge {edge.id}: current resistance exceeds maximum resistance"
                    )
        elif edge.max_resistance is not None or edge.current_resistance is not None:
            raise ScenarioValidationError(
                f"GE path {edge.id} cannot have resistance"
            )
        if edge.foot_time is None and edge.moto_time is None:
            raise ScenarioValidationError(
                f"GE edge {edge.id} must allow foot or motorcycle travel"
            )


def _shortest_path_time(payload: ScenarioPayload) -> float:
    adjacency = {vertex.id: [] for vertex in payload.gm.vertices}
    for edge in payload.gm.edges:
        travel_time = edge.length / edge.speed
        adjacency[edge.v1].append((edge.v2, travel_time))
        adjacency[edge.v2].append((edge.v1, travel_time))

    best = {payload.entry_id: 0.0}
    pending = [(0.0, payload.entry_id)]
    while pending:
        current_time, vertex_id = min(pending)
        pending.remove((current_time, vertex_id))
        if current_time != best.get(vertex_id):
            continue
        if vertex_id == payload.exit_id:
            return current_time
        for neighbor_id, travel_time in adjacency[vertex_id]:
            next_time = current_time + travel_time
            if next_time < best.get(neighbor_id, float("inf")):
                best[neighbor_id] = next_time
                pending.append((next_time, neighbor_id))
    raise ScenarioValidationError(
        "GM must contain a path from entry to exit"
    )
