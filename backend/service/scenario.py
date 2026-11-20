if __package__.startswith("backend.") or __package__ == "backend.service":
    from ..domain.scenario import (
        ScenarioSummary,
        ScenarioValidationError,
        _require_unique_ids,
        _shortest_path_time,
        _validate_coordinates,
        _validate_edge_endpoints,
        _validate_ge_edges,
    )
    from ..schemas.scenario_schemas import ScenarioPayload
else:
    from domain.scenario import (
        ScenarioSummary,
        ScenarioValidationError,
        _require_unique_ids,
        _shortest_path_time,
        _validate_coordinates,
        _validate_edge_endpoints,
        _validate_ge_edges,
    )
    from schemas.scenario_schemas import ScenarioPayload


class ScenarioService:
    def load(self, payload: ScenarioPayload) -> ScenarioSummary:
        ge_ids = _require_unique_ids(payload.ge.vertices, "GE vertex")
        gm_ids = _require_unique_ids(payload.gm.vertices, "GM vertex")

        if payload.base_id not in ge_ids:
            raise ScenarioValidationError(
                f"Base vertex {payload.base_id} does not exist in GE"
            )
        if payload.entry_id not in gm_ids:
            raise ScenarioValidationError(
                f"Entry vertex {payload.entry_id} does not exist in GM"
            )
        if payload.exit_id not in gm_ids:
            raise ScenarioValidationError(
                f"Exit vertex {payload.exit_id} does not exist in GM"
            )
        if payload.entry_id == payload.exit_id:
            raise ScenarioValidationError(
                "GM entry and exit must be different vertices"
            )

        base_count = sum(
            vertex.position_type.value == "base"
            for vertex in payload.ge.vertices
        )
        if base_count != 1:
            raise ScenarioValidationError(
                "GE must contain exactly one base position"
            )
        if not any(
            vertex.id == payload.base_id
            and vertex.position_type.value == "base"
            for vertex in payload.ge.vertices
        ):
            raise ScenarioValidationError(
                "base_id must identify the GE base position"
            )

        entry_count = sum(
            vertex.role.value == "entry" for vertex in payload.gm.vertices
        )
        exit_count = sum(
            vertex.role.value == "exit" for vertex in payload.gm.vertices
        )
        if entry_count != 1 or exit_count != 1:
            raise ScenarioValidationError(
                "GM must contain exactly one entry and exactly one exit"
            )
        if not any(
            vertex.id == payload.entry_id and vertex.role.value == "entry"
            for vertex in payload.gm.vertices
        ):
            raise ScenarioValidationError(
                "entry_id must identify the GM entry vertex"
            )
        if not any(
            vertex.id == payload.exit_id and vertex.role.value == "exit"
            for vertex in payload.gm.vertices
        ):
            raise ScenarioValidationError(
                "exit_id must identify the GM exit vertex"
            )

        _validate_coordinates(payload)
        _validate_edge_endpoints(payload.ge.edges, ge_ids, "GE")
        _validate_edge_endpoints(payload.gm.edges, gm_ids, "GM")
        _validate_ge_edges(payload)
        shortest_maze_time = _shortest_path_time(payload)

        return ScenarioSummary(
            name=payload.name,
            ge_vertex_count=len(payload.ge.vertices),
            ge_edge_count=len(payload.ge.edges),
            gm_vertex_count=len(payload.gm.vertices),
            gm_edge_count=len(payload.gm.edges),
            base_id=payload.base_id,
            entry_id=payload.entry_id,
            exit_id=payload.exit_id,
            shortest_maze_time=shortest_maze_time,
        )


scenario_service = ScenarioService()
