if __package__.startswith("backend."):
    from ..vertice.vertexMain import VertexMain
    from ..arista.edgeMain import EdgeMain
else:
    from core.vertice.vertexMain import VertexMain
    from core.arista.edgeMain import EdgeMain


class VertexNotFoundError(LookupError):
    """Raised when a vertex identifier does not exist in the graph."""


class DuplicateVertexError(ValueError):
    """Raised when adding a vertex whose identifier already exists."""


class graph:
    """Generic undirected graph stored as an adjacency list.

    Works with any VertexMain / EdgeMain subclass, so it can hold either GE
    or GM elements.
    """

    def __init__(self):
        """Create an empty graph.

        Receives: nothing.
        Returns:
            None.
        """
        self.vertices = []

    def vertex_exist(self, vertex: VertexMain) -> bool:
        """Tell whether a vertex with the same identifier is in the graph.

        Receives:
            vertex: vertex to look for.
        Returns:
            bool: True if some stored vertex has the same identifier.
        """
        return any(existing.get_id() == vertex.get_id() for existing in self.vertices)

    def add_vertex(self, vertex: VertexMain) -> None:
        """Add a vertex to the graph.

        Receives:
            vertex: vertex to add.
        Returns:
            None.
        Raises:
            DuplicateVertexError: if the identifier already exists.
        """
        if self.vertex_exist(vertex):
            raise DuplicateVertexError(f"el vertice {vertex.get_id()} ya existe en el grafo")
        self.vertices.append(vertex)

    def get_vertex(self, vertex_id: str) -> VertexMain:
        """Return the stored vertex with the given identifier.

        Receives:
            vertex_id: identifier to look for.
        Returns:
            VertexMain: the stored vertex.
        Raises:
            VertexNotFoundError: if no vertex has that identifier.
        """
        for existing in self.vertices:
            if existing.get_id() == vertex_id:
                return existing
        raise VertexNotFoundError(f"el vertice {vertex_id} no existe en el grafo")

    def add_edge(self, edge_to_add: EdgeMain) -> EdgeMain:
        """Add an undirected edge between two existing vertices.

        Receives:
            edge_to_add: edge whose endpoints must be vertices stored in
                this graph.
        Returns:
            EdgeMain: the same edge, now registered.
        How it works:
            Checks both endpoints are the stored instances and registers the
            edge in both adjacency lists (undirected graph).
        Raises:
            VertexNotFoundError: if an endpoint is not in the graph.
        """
        for endpoint in edge_to_add.get_endpoints():
            if self.get_vertex(endpoint.get_id()) is not endpoint:
                raise VertexNotFoundError(f"el vertice {endpoint.get_id()} no pertenece a este grafo")
        edge_to_add.get_v1().add_edge(edge_to_add)
        edge_to_add.get_v2().add_edge(edge_to_add)
        return edge_to_add

    def get_neighbors(self, vertex: VertexMain) -> list:
        """Return the neighbors of a stored vertex.

        Receives:
            vertex: vertex whose neighbors are requested.
        Returns:
            list: vertices at the other end of each incident edge.
        """
        return self.get_vertex(vertex.get_id()).get_neighbors()
