def list_edges(graph) -> list:
    """Return every edge of a graph.

    Receives:
        graph: Graph (GE or GM).
    Returns:
        list: edges in insertion order (each undirected edge appears once).
    """
    return graph.get_edges()
