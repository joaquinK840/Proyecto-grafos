from typing import Callable, Optional

if __package__.startswith("backend."):
    from ..vertice.vertexMain import VertexMain
    from ..arista.edgeMain import EdgeMain
    from .path_result import PathResult
    from .funciones.add_vertex import add_vertex
    from .funciones.add_edge import add_edge
    from .funciones.get_vertex import get_vertex
    from .funciones.breadth_first import breadth_first
    from .funciones.depth_first import depth_first
    from .funciones.shortest_path import shortest_path
else:
    from core.vertice.vertexMain import VertexMain
    from core.arista.edgeMain import EdgeMain
    from core.grafo.path_result import PathResult
    from core.grafo.funciones.add_vertex import add_vertex
    from core.grafo.funciones.add_edge import add_edge
    from core.grafo.funciones.get_vertex import get_vertex
    from core.grafo.funciones.breadth_first import breadth_first
    from core.grafo.funciones.depth_first import depth_first
    from core.grafo.funciones.shortest_path import shortest_path


class Graph:
    """Base undirected graph shared by GE and GM.

    Representation: adjacency list. The graph keeps two dictionaries,
    {vertex_id: vertex} and {edge_id: edge}, for O(1) lookups, and every
    vertex keeps its own list of incident edges.

    This class only stores the data and delegates every operation to the
    functions in ``core/grafo/funciones`` (one file per function).
    Subclasses set ``VERTEX_TYPE`` / ``EDGE_TYPE`` so a graph only accepts
    its own kind of elements, and override ``validate`` to add their rules.
    """

    VERTEX_TYPE = VertexMain
    EDGE_TYPE = EdgeMain

    def __init__(self):
        """Create an empty graph.

        Receives: nothing.
        Returns:
            None.
        """
        self._vertices = {}
        self._edges = {}

    def add_vertex(self, vertex: VertexMain) -> None:
        """Add a vertex.

        Receives:
            vertex: instance of ``VERTEX_TYPE``.
        Returns:
            None.
        How it works:
            Delegates to ``funciones.add_vertex``.
        Raises:
            TypeError, DuplicateVertexError.
        """
        add_vertex(self._vertices, vertex, self.VERTEX_TYPE)

    def add_edge(self, edge: EdgeMain) -> None:
        """Add an undirected edge between two stored vertices.

        Receives:
            edge: instance of ``EDGE_TYPE``.
        Returns:
            None.
        How it works:
            Delegates to ``funciones.add_edge``.
        Raises:
            TypeError, DuplicateEdgeError, VertexNotFoundError.
        """
        add_edge(self._vertices, self._edges, edge, self.EDGE_TYPE)

    def get_vertex(self, vertex_id: str) -> VertexMain:
        """Return a stored vertex by identifier.

        Receives:
            vertex_id: identifier to look for.
        Returns:
            VertexMain: the stored vertex.
        Raises:
            VertexNotFoundError: if it does not exist.
        """
        return get_vertex(self._vertices, vertex_id)

    def has_vertex(self, vertex_id: str) -> bool:
        """Tell whether a vertex identifier exists.

        Receives:
            vertex_id: identifier to look for.
        Returns:
            bool: True if it is stored.
        """
        return vertex_id in self._vertices

    def get_vertices(self) -> list:
        """Return every vertex in insertion order.

        Receives: nothing.
        Returns:
            list: the stored vertices.
        """
        return list(self._vertices.values())

    def get_edges(self) -> list:
        """Return every edge in insertion order.

        Receives: nothing.
        Returns:
            list: the stored edges.
        """
        return list(self._edges.values())

    def get_neighbors(self, vertex_id: str) -> list:
        """Return the neighbors of a vertex (through any edge).

        Receives:
            vertex_id: identifier of the vertex.
        Returns:
            list: vertices at the other end of each incident edge.
        """
        return self.get_vertex(vertex_id).get_neighbors()

    def breadth_first(self, start_id: str) -> list:
        """Breadth-first traversal through available edges.

        Receives:
            start_id: identifier of the start vertex.
        Returns:
            list: vertices in visit order.
        How it works:
            Delegates to ``funciones.breadth_first``.
        """
        return breadth_first(self.get_vertex(start_id))

    def depth_first(self, start_id: str) -> list:
        """Depth-first traversal through available edges.

        Receives:
            start_id: identifier of the start vertex.
        Returns:
            list: vertices in visit order.
        How it works:
            Delegates to ``funciones.depth_first``.
        """
        return depth_first(self.get_vertex(start_id))

    def shortest_path(self, origin_id: str, destination_id: str,
                      weight: Callable) -> Optional[PathResult]:
        """Minimum cost path through available edges (Dijkstra).

        Receives:
            origin_id: identifier of the start vertex.
            destination_id: identifier of the target vertex.
            weight: function edge -> non-negative cost.
        Returns:
            Optional[PathResult]: the path, or None if unreachable.
        How it works:
            Delegates to ``funciones.shortest_path``.
        """
        return shortest_path(self.get_vertex(origin_id), self.get_vertex(destination_id), weight)

    def validate(self) -> None:
        """Check the invariants of the whole graph.

        Receives: nothing.
        Returns:
            None.
        How it works:
            The base graph has no global rules; GE and GM override it.
        """
