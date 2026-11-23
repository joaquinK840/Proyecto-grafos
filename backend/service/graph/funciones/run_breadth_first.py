def run_breadth_first(graph, start_id: str) -> list:
    """Run a breadth-first traversal on a graph.

    Receives:
        graph: Graph (GE or GM).
        start_id: identifier of the start vertex.
    Returns:
        list: vertices in visit order (only through available edges).
    Raises:
        VertexNotFoundError: if the start vertex does not exist.
    """
    return graph.breadth_first(start_id)
