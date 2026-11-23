def run_depth_first(graph, start_id: str) -> list:
    """Run a depth-first traversal on a graph.

    Receives:
        graph: Graph (GE or GM).
        start_id: identifier of the start vertex.
    Returns:
        list: vertices in visit order (only through available edges).
    Raises:
        VertexNotFoundError: if the start vertex does not exist.
    """
    return graph.depth_first(start_id)
