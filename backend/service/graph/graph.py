if __package__.startswith("backend."):
    from ...domain.graph_kind import GraphKind
    from ...repository.scenario_repository import ScenarioRepository, scenario_repository
    from .funciones.get_graph import get_graph
    from .funciones.list_vertices import list_vertices
    from .funciones.list_edges import list_edges
    from .funciones.find_vertex import find_vertex
    from .funciones.list_neighbors import list_neighbors
    from .funciones.run_breadth_first import run_breadth_first
    from .funciones.run_depth_first import run_depth_first
else:
    from domain.graph_kind import GraphKind
    from repository.scenario_repository import ScenarioRepository, scenario_repository
    from service.graph.funciones.get_graph import get_graph
    from service.graph.funciones.list_vertices import list_vertices
    from service.graph.funciones.list_edges import list_edges
    from service.graph.funciones.find_vertex import find_vertex
    from service.graph.funciones.list_neighbors import list_neighbors
    from service.graph.funciones.run_breadth_first import run_breadth_first
    from service.graph.funciones.run_depth_first import run_depth_first


class GraphService:
    """Facade for the queries on the graphs of the loaded scenario.

    It contains no logic: each method picks the requested graph (GE or GM)
    and delegates to a function in ``service/graph/funciones``.
    """

    def __init__(self, repository: ScenarioRepository):
        """Create the service.

        Receives:
            repository: storage of the current scenario.
        Returns:
            None.
        """
        self._repository = repository

    def get_vertices(self, kind: GraphKind) -> list:
        """Return every vertex of GE or GM.

        Receives:
            kind: graph to query.
        Returns:
            list: vertices of that graph.
        """
        return list_vertices(get_graph(self._repository, kind))

    def get_edges(self, kind: GraphKind) -> list:
        """Return every edge of GE or GM.

        Receives:
            kind: graph to query.
        Returns:
            list: edges of that graph.
        """
        return list_edges(get_graph(self._repository, kind))

    def get_vertex(self, kind: GraphKind, vertex_id: str):
        """Return one vertex of GE or GM.

        Receives:
            kind: graph to query.
            vertex_id: identifier of the vertex.
        Returns:
            VertexMain: the vertex.
        """
        return find_vertex(get_graph(self._repository, kind), vertex_id)

    def get_neighbors(self, kind: GraphKind, vertex_id: str) -> list:
        """Return the neighbors of a vertex of GE or GM.

        Receives:
            kind: graph to query.
            vertex_id: identifier of the vertex.
        Returns:
            list: neighbor vertices.
        """
        return list_neighbors(get_graph(self._repository, kind), vertex_id)

    def breadth_first(self, kind: GraphKind, start_id: str) -> list:
        """Run BFS on GE or GM.

        Receives:
            kind: graph to traverse.
            start_id: identifier of the start vertex.
        Returns:
            list: vertices in visit order.
        """
        return run_breadth_first(get_graph(self._repository, kind), start_id)

    def depth_first(self, kind: GraphKind, start_id: str) -> list:
        """Run DFS on GE or GM.

        Receives:
            kind: graph to traverse.
            start_id: identifier of the start vertex.
        Returns:
            list: vertices in visit order.
        """
        return run_depth_first(get_graph(self._repository, kind), start_id)


graph_service = GraphService(scenario_repository)
