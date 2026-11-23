if __package__.startswith("backend."):
    from ..graph_errors import DuplicateVertexError
else:
    from core.grafo.graph_errors import DuplicateVertexError


def add_vertex(vertices: dict, vertex, vertex_type: type) -> None:
    """Store a vertex in the graph vertex table.

    Receives:
        vertices: the graph table {vertex_id: vertex}, modified in place.
        vertex: vertex to add.
        vertex_type: class the vertex must be an instance of (for example
            VertexGE), so a graph cannot mix vertices of the other graph.
    Returns:
        None.
    How it works:
        Checks the type, then checks the identifier is not taken and finally
        inserts it in the dictionary (O(1) average).
    Raises:
        TypeError: if the vertex is not an instance of ``vertex_type``.
        DuplicateVertexError: if the identifier already exists.
    """
    if not isinstance(vertex, vertex_type):
        raise TypeError(f"vertex must be a {vertex_type.__name__}")
    if vertex.get_id() in vertices:
        raise DuplicateVertexError(f"vertex {vertex.get_id()} already exists in the graph")
    vertices[vertex.get_id()] = vertex
