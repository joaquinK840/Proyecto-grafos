from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioSummary:
    """Immutable summary of a loaded scenario.

    Attributes:
        name: scenario name.
        ge_vertex_count / ge_edge_count: size of GE.
        gm_vertex_count / gm_edge_count: size of GM.
        base_id: identifier of the GE base.
        entry_id / exit_id: identifiers of the GM entry and exit.
        shortest_maze_time: minimum travel time from entry to exit.
        shortest_maze_route: vertex identifiers of that route, in order.
        shortest_maze_route_edges: edge identifiers of that route, in order.
    """

    name: str
    ge_vertex_count: int
    ge_edge_count: int
    gm_vertex_count: int
    gm_edge_count: int
    base_id: str
    entry_id: str
    exit_id: str
    shortest_maze_time: float
    shortest_maze_route: list
    shortest_maze_route_edges: list
