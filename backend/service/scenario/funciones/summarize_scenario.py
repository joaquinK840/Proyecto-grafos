if __package__.startswith("backend."):
    from ....domain.scenario import Scenario
    from ....domain.scenario_summary import ScenarioSummary
else:
    from domain.scenario import Scenario
    from domain.scenario_summary import ScenarioSummary


def summarize_scenario(scenario: Scenario) -> ScenarioSummary:
    """Build the summary of a loaded scenario.

    Receives:
        scenario: validated scenario.
    Returns:
        ScenarioSummary: sizes of both graphs, special vertices and the
        fastest GM route from entry to exit.
    How it works:
        Reads the data from the graphs and asks GM for its fastest route
        (Dijkstra with t(e) = l(e) / v(e)).
    """
    ge = scenario.get_ge()
    gm = scenario.get_gm()
    route = gm.fastest_route()
    return ScenarioSummary(
        name=scenario.get_name(),
        ge_vertex_count=len(ge.get_vertices()),
        ge_edge_count=len(ge.get_edges()),
        gm_vertex_count=len(gm.get_vertices()),
        gm_edge_count=len(gm.get_edges()),
        base_id=ge.get_base().get_id(),
        entry_id=gm.get_entry().get_id(),
        exit_id=gm.get_exit().get_id(),
        shortest_maze_time=route.cost,
        shortest_maze_route=[vertex.get_id() for vertex in route.vertices],
        shortest_maze_route_edges=[edge.get_id() for edge in route.edges],
    )
