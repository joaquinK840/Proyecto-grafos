if __package__.startswith("backend."):
    from ..core.arista.edge import edge
    from ..core.grafo.graph import graph
    from ..core.vertice.vertex import vertex
    from ..core.queue.queue import queue
    from ..core.stack.stack import stack
else:
    from core.arista.edge import edge
    from core.grafo.graph import graph
    from core.vertice.vertex import vertex
    from core.queue.queue import queue
    from core.stack.stack import stack


class GraphService:
    def __init__(self):
        self.graph = graph()

    def add_vertex(self, name: int):
        new_vertex = vertex(name)
        self.graph.add_vertex(new_vertex)
        return new_vertex

    def get_vertices(self):
        return self.graph.vertices

    def get_edges(self):
        return [
            graph_edge
            for current_vertex in self.graph.vertices
            for graph_edge in current_vertex.get_edges()
        ]

    def get_vertex(self, name: int):
        return self.graph.get_vertex(name)

    def add_edge(self, source: int, target: int, weight: int):
        source_vertex = self.graph.get_vertex(source)
        target_vertex = self.graph.get_vertex(target)
        return self.graph.add_edge(edge(source_vertex, target_vertex, weight))

    def get_neighbors(self, name: int):
        return self.graph.get_neighbors(self.graph.get_vertex(name))

    def breadth_first(self, start: int):
        initial_vertex = self.graph.get_vertex(start)
        pending = queue()
        pending.enqueue(initial_vertex)
        visited = {initial_vertex.get_name()}
        result = []

        while not pending.is_empty():
            current = pending.dequeue()
            result.append(current)
            for neighbor in self.graph.get_neighbors(current):
                if neighbor.get_name() not in visited:
                    visited.add(neighbor.get_name())
                    pending.enqueue(neighbor)
        return result

    def depth_first(self, start: int):
        initial_vertex = self.graph.get_vertex(start)
        pending = stack()
        pending.push(initial_vertex)
        visited = set()
        result = []

        while not pending.is_empty():
            current = pending.pop()
            if current.get_name() in visited:
                continue
            visited.add(current.get_name())
            result.append(current)
            neighbors = self.graph.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor.get_name() not in visited:
                    pending.push(neighbor)
        return result


graph_service = GraphService()
