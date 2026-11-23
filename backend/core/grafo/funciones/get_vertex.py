if __package__.startswith("backend."):
    from ..graph_errors import VertexNotFoundError
else:
    from core.grafo.graph_errors import VertexNotFoundError


def get_vertex(vertices: dict, vertex_id: str):
    """Look up a vertex by its identifier.

    Receives:
        vertices: the graph table {vertex_id: vertex}.
        vertex_id: identifier to look for.
    Returns:
        VertexMain: the stored vertex.
    How it works:
        Direct dictionary access (O(1) average).
    Raises:
        VertexNotFoundError: if no vertex has that identifier.
    """
    if vertex_id not in vertices:
        raise VertexNotFoundError(f"vertex {vertex_id} does not exist in the graph")
    return vertices[vertex_id]
