def find_vertex(graph, vertex_id: str):
    """Return one vertex of a graph by identifier.

    Receives:
        graph: Graph (GE or GM).
        vertex_id: identifier to look for.
    Returns:
        VertexMain: the stored vertex.
    Raises:
        VertexNotFoundError: if it does not exist.
    """
    return graph.get_vertex(vertex_id)
