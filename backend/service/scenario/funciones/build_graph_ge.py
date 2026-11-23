if __package__.startswith("backend."):
    from ....core.grafo.graphGE import GraphGE
    from ....core.vertice.vertexGE import VertexGE
    from ....core.arista.edgeGE import EdgeGE
    from ....schemas.graph_ge_schema import GraphGEInput
    from .as_scenario_error import as_scenario_error
else:
    from core.grafo.graphGE import GraphGE
    from core.vertice.vertexGE import VertexGE
    from core.arista.edgeGE import EdgeGE
    from schemas.graph_ge_schema import GraphGEInput
    from service.scenario.funciones.as_scenario_error import as_scenario_error


def build_graph_ge(data: GraphGEInput) -> GraphGE:
    """Build and validate the elevated graph GE from the JSON data.

    Receives:
        data: GE section of the scenario JSON (already shape-checked).
    Returns:
        GraphGE: graph with every vertex and edge, globally validated.
    How it works:
        1. Creates every VertexGE and adds it to the graph.
        2. Creates every EdgeGE using the stored vertices as endpoints.
        3. Runs ``GraphGE.validate`` (exactly one base).
        Each step runs inside ``as_scenario_error`` so a broken rule is
        reported with the element that caused it. All the rules come from
        the core classes; nothing is validated twice here.
    Raises:
        ScenarioValidationError: if any element or global rule is invalid.
    """
    graph = GraphGE()
    for vertex in data.vertices:
        with as_scenario_error(f"GE vertex {vertex.id}"):
            graph.add_vertex(VertexGE(vertex.id, vertex.x, vertex.y, vertex.position_type))

    for edge in data.edges:
        with as_scenario_error(f"GE edge {edge.id}"):
            graph.add_edge(EdgeGE(
                edge.id,
                graph.get_vertex(edge.v1),
                graph.get_vertex(edge.v2),
                edge.connection_type,
                foot_time=edge.foot_time,
                moto_time=edge.moto_time,
                max_resistance=edge.max_resistance,
                current_resistance=edge.current_resistance,
                enabled=edge.enabled,
            ))

    with as_scenario_error("GE"):
        graph.validate()
    return graph
