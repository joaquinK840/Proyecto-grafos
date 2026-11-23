from pydantic import BaseModel, ConfigDict, Field

if __package__.startswith("backend."):
    from .graph_ge_schema import GraphGEInput
    from .graph_gm_schema import GraphGMInput
    from .parameters_schema import ExecutionParametersInput
    from .convoy_schema import ConvoyInput
    from ..domain.scenario_summary import ScenarioSummary
else:
    from schemas.graph_ge_schema import GraphGEInput
    from schemas.graph_gm_schema import GraphGMInput
    from schemas.parameters_schema import ExecutionParametersInput
    from schemas.convoy_schema import ConvoyInput
    from domain.scenario_summary import ScenarioSummary


class ScenarioPayload(BaseModel):
    """Shape of the full scenario JSON.

    Reuses the GE / GM graph schemas, the parameters schema and the convoy
    schema. ``base_id``, ``entry_id`` and ``exit_id`` must match the
    vertices marked as base / entry / exit (checked by the scenario
    service).
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    ge: GraphGEInput
    gm: GraphGMInput
    base_id: str
    entry_id: str
    exit_id: str
    parameters: ExecutionParametersInput = ExecutionParametersInput()
    convoy: ConvoyInput = ConvoyInput()


class ScenarioLoadResponse(BaseModel):
    """API response after loading a scenario."""

    name: str
    ge_vertex_count: int
    ge_edge_count: int
    gm_vertex_count: int
    gm_edge_count: int
    base_id: str
    entry_id: str
    exit_id: str
    shortest_maze_time: float
    shortest_maze_route: list[str]
    shortest_maze_route_edges: list[str]

    @classmethod
    def from_summary(cls, summary: ScenarioSummary) -> "ScenarioLoadResponse":
        """Build the response from the domain summary.

        Receives:
            summary: ScenarioSummary produced by the scenario service.
        Returns:
            ScenarioLoadResponse: serializable representation.
        """
        return cls(
            name=summary.name,
            ge_vertex_count=summary.ge_vertex_count,
            ge_edge_count=summary.ge_edge_count,
            gm_vertex_count=summary.gm_vertex_count,
            gm_edge_count=summary.gm_edge_count,
            base_id=summary.base_id,
            entry_id=summary.entry_id,
            exit_id=summary.exit_id,
            shortest_maze_time=summary.shortest_maze_time,
            shortest_maze_route=list(summary.shortest_maze_route),
            shortest_maze_route_edges=list(summary.shortest_maze_route_edges),
        )
