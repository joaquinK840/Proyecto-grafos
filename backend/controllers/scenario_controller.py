from fastapi import APIRouter

if __package__.startswith("backend."):
    from ..schemas.scenario_schemas import ScenarioLoadResponse, ScenarioPayload
    from ..service.scenario import scenario_service
else:
    from schemas.scenario_schemas import ScenarioLoadResponse, ScenarioPayload
    from service.scenario import scenario_service


router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.post("/load", response_model=ScenarioLoadResponse)
def load_scenario(payload: ScenarioPayload):
    summary = scenario_service.load(payload)
    return ScenarioLoadResponse(
        name=summary.name,
        ge_vertex_count=summary.ge_vertex_count,
        ge_edge_count=summary.ge_edge_count,
        gm_vertex_count=summary.gm_vertex_count,
        gm_edge_count=summary.gm_edge_count,
        base_id=summary.base_id,
        entry_id=summary.entry_id,
        exit_id=summary.exit_id,
        shortest_maze_time=summary.shortest_maze_time,
    )
