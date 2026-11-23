if __package__.startswith("backend."):
    from ....core.grafo.graphGM import GraphGM
    from ....core.vertice.vertexGM import VertexGM
    from ....core.arista.edgeGM import EdgeGM
    from ....schemas.graph_gm_schema import GraphGMInput
    from .as_scenario_error import as_scenario_error
else:
    from core.grafo.graphGM import GraphGM
    from core.vertice.vertexGM import VertexGM
    from core.arista.edgeGM import EdgeGM
    from schemas.graph_gm_schema import GraphGMInput
    from service.scenario.funciones.as_scenario_error import as_scenario_error


def build_graph_gm(data: GraphGMInput) -> GraphGM:
    """Build and validate the maze graph GM from the JSON data.

    Receives:
        data: GM section of the scenario JSON (already shape-checked).
    Returns:
        GraphGM: graph with every vertex and corridor, globally validated.
    How it works:
        1. Creates every VertexGM and adds it to the graph.
        2. Creates every EdgeGM using the stored vertices as endpoints.
        3. Runs ``GraphGM.validate`` (single entry, single exit and a path
           between them).
        Each step runs inside ``as_scenario_error`` so a broken rule is
        reported with the element that caused it.
    Raises:
        ScenarioValidationError: if any element or global rule is invalid.
    """
    graph = GraphGM()
    for vertex in data.vertices:
        with as_scenario_error(f"GM vertex {vertex.id}"):
            graph.add_vertex(VertexGM(vertex.id, vertex.x, vertex.y, vertex.role))

    for edge in data.edges:
        with as_scenario_error(f"GM edge {edge.id}"):
            graph.add_edge(EdgeGM(
                edge.id,
                graph.get_vertex(edge.v1),
                graph.get_vertex(edge.v2),
                edge.length,
                edge.speed,
            ))

    with as_scenario_error("GM"):
        graph.validate()
    return graph
