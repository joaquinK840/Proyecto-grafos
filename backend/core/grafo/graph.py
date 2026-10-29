if __package__.startswith("backend."):
    from ..vertice.vertex import vertex
    from ..arista.edge import edge
else:
    from core.vertice.vertex import vertex
    from core.arista.edge import edge


class VertexNotFoundError(LookupError):
    pass


class DuplicateVertexError(ValueError):
    pass


class graph:
    def __init__(self):
        self.vertices = []

    def vertex_exist(self, vertex: vertex):
        return any(existing.get_name() == vertex.get_name() for existing in self.vertices)

    def add_vertex(self, vertex: vertex):
        if self.vertex_exist(vertex):
            raise DuplicateVertexError(f"el vertice {vertex.get_name()} ya existe en el grafo")
        self.vertices.append(vertex)

    def get_vertex(self, vertex_name):
        for existing in self.vertices:
            if existing.get_name() == vertex_name:
                return existing
        raise VertexNotFoundError(f"el vertice {vertex_name} no existe en el grafo")

    def add_edge(self, edge_to_add: edge):
        v1 = self.get_vertex(edge_to_add.get_v1().get_name())
        v2 = self.get_vertex(edge_to_add.get_v2().get_name())
        graph_edge = edge(v1, v2, edge_to_add.get_weight())
        v1.add_neighbors(graph_edge)
        return graph_edge

    def get_neighbors(self, vertex: vertex):
        stored_vertex = self.get_vertex(vertex.get_name())
        return [neighbor_edge.get_v2() for neighbor_edge in stored_vertex.get_neighbors()]
