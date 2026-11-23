def list_neighbors(graph, vertex_id: str) -> list:
    """Return the neighbors of a vertex.

    Receives:
        graph: Graph (GE or GM).
        vertex_id: identifier of the vertex.
    Returns:
        list: vertices at the other end of each incident edge.
    Raises:
        VertexNotFoundError: if the vertex does not exist.
    """
    return graph.get_neighbors(vertex_id)
