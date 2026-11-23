def get_available_neighbors(vertex) -> list:
    """Return the neighbors reachable right now from a vertex.

    Receives:
        vertex: vertex whose incident edges are inspected.
    Returns:
        list[tuple[EdgeMain, VertexMain]]: (edge, neighbor) pairs, in the
        order the edges were added, only for edges whose ``is_available()``
        is True (for example, destroyed bridges are skipped).
    How it works:
        Walks the incident edges of the vertex and, for each available one,
        asks for the vertex at the opposite end.
    """
    return [
        (edge, edge.get_opposite(vertex))
        for edge in vertex.get_edges()
        if edge.is_available()
    ]
