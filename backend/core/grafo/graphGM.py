if __package__.startswith("backend."):
    from .graph import Graph
    from .path_result import PathResult
    from ..vertice.vertexGM import VertexGM
    from ..arista.edgeGM import EdgeGM
    from .funciones.find_unique_vertex import find_unique_vertex
    from .funciones.require_path import require_path
else:
    from core.grafo.graph import Graph
    from core.grafo.path_result import PathResult
    from core.vertice.vertexGM import VertexGM
    from core.arista.edgeGM import EdgeGM
    from core.grafo.funciones.find_unique_vertex import find_unique_vertex
    from core.grafo.funciones.require_path import require_path


class GraphGM(Graph):
    """Maze graph GM: intersections joined by corridors.

    Only accepts VertexGM / EdgeGM elements and adds the global rules:
    a single entry, a single exit (different, since a vertex has only one
    role) and an initial path between them.
    """

    VERTEX_TYPE = VertexGM
    EDGE_TYPE = EdgeGM

    def get_entry(self) -> VertexGM:
        """Return the maze entry.

        Receives: nothing.
        Returns:
            VertexGM: the only vertex whose role is ENTRY.
        Raises:
            GraphValidationError: if there is not exactly one entry.
        """
        return find_unique_vertex(self.get_vertices(), VertexGM.is_entry, "entry")

    def get_exit(self) -> VertexGM:
        """Return the maze exit.

        Receives: nothing.
        Returns:
            VertexGM: the only vertex whose role is EXIT.
        Raises:
            GraphValidationError: if there is not exactly one exit.
        """
        return find_unique_vertex(self.get_vertices(), VertexGM.is_exit, "exit")

    def fastest_route(self) -> PathResult:
        """Return the minimum travel time route from entry to exit.

        Receives: nothing.
        Returns:
            PathResult: route whose cost is the sum of t(e) = l(e) / v(e).
        How it works:
            Delegates to ``funciones.require_path`` using
            ``EdgeGM.get_travel_time`` as weight.
        Raises:
            GraphValidationError: if entry/exit are invalid or unreachable.
        """
        return require_path(self.get_entry(), self.get_exit(), EdgeGM.get_travel_time)

    def validate(self) -> None:
        """Check the GM global rules.

        Receives: nothing.
        Returns:
            None.
        How it works:
            ``fastest_route`` already requires a single entry, a single exit
            and a path between them, so it covers every GM global rule.
        Raises:
            GraphValidationError: if a rule is broken.
        """
        self.fastest_route()
