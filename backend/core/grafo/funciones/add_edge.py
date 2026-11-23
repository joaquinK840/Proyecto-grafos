if __package__.startswith("backend."):
    from ..graph_errors import DuplicateEdgeError, VertexNotFoundError
    from .get_vertex import get_vertex
else:
    from core.grafo.graph_errors import DuplicateEdgeError, VertexNotFoundError
    from core.grafo.funciones.get_vertex import get_vertex


def add_edge(vertices: dict, edges: dict, edge, edge_type: type) -> None:
    """Store an undirected edge between two vertices of the graph.

    Receives:
        vertices: the graph table {vertex_id: vertex}.
        edges: the graph table {edge_id: edge}, modified in place.
        edge: edge to add.
        edge_type: class the edge must be an instance of (for example
            EdgeGE), so a graph cannot mix edges of the other graph.
    Returns:
        None.
    How it works:
        1. Checks the edge type and that its identifier is not taken.
        2. Checks both endpoints are the very instances stored in the graph
           (not just vertices with the same id), so the adjacency lists stay
           consistent.
        3. Registers the edge in the edge table and in the adjacency list of
           BOTH endpoints, because the graphs are undirected.
    Raises:
        TypeError: if the edge is not an instance of ``edge_type``.
        DuplicateEdgeError: if the edge identifier already exists.
        VertexNotFoundError: if an endpoint does not belong to the graph.
    """
    if not isinstance(edge, edge_type):
        raise TypeError(f"edge must be a {edge_type.__name__}")
    if edge.get_id() in edges:
        raise DuplicateEdgeError(f"edge {edge.get_id()} already exists in the graph")
    for endpoint in edge.get_endpoints():
        if get_vertex(vertices, endpoint.get_id()) is not endpoint:
            raise VertexNotFoundError(f"vertex {endpoint.get_id()} does not belong to this graph")
    edges[edge.get_id()] = edge
    edge.get_v1().add_edge(edge)
    edge.get_v2().add_edge(edge)
