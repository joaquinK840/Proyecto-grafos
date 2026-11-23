import unittest

from backend.core.arista.connection_type import ConnectionType
from backend.core.arista.edgeGE import EdgeGE
from backend.core.arista.edgeGM import EdgeGM
from backend.core.grafo.graphGE import GraphGE
from backend.core.grafo.graphGM import GraphGM
from backend.core.grafo.graph_errors import (
    DuplicateVertexError,
    GraphValidationError,
)
from backend.core.heap.min_heap import MinHeap
from backend.core.vertice.maze_vertex_role import MazeVertexRole
from backend.core.vertice.position_type import PositionType
from backend.core.vertice.vertexGE import VertexGE
from backend.core.vertice.vertexGM import VertexGM


class MinHeapTests(unittest.TestCase):
    """Tests for the project priority queue."""

    def test_pops_in_priority_order_and_fifo_on_ties(self):
        heap = MinHeap()
        for priority, item in [(5, "a"), (1, "b"), (3, "c"), (1, "d")]:
            heap.push(priority, item)
        self.assertEqual([heap.pop()[1] for _ in range(4)], ["b", "d", "c", "a"])
        self.assertTrue(heap.is_empty())


class GraphGETests(unittest.TestCase):
    """Tests for the elevated graph."""

    def setUp(self):
        self.graph = GraphGE()
        self.base = VertexGE("B", 1, 1, PositionType.BASE)
        self.tower = VertexGE("T", 2, 2, PositionType.TOWER_CANDIDATE)
        self.graph.add_vertex(self.base)
        self.graph.add_vertex(self.tower)
        self.bridge = EdgeGE("P", self.base, self.tower, ConnectionType.BRIDGE,
                             moto_time=1, max_resistance=1)
        self.graph.add_edge(self.bridge)

    def test_rejects_duplicate_and_foreign_vertices(self):
        with self.assertRaises(DuplicateVertexError):
            self.graph.add_vertex(VertexGE("B", 5, 5, PositionType.TRANSIT))
        with self.assertRaises(TypeError):
            self.graph.add_vertex(VertexGM("X", 0, 0))

    def test_destroyed_bridge_is_skipped_by_searches(self):
        self.assertEqual(len(self.graph.breadth_first("B")), 2)
        self.bridge.wear_down()
        self.assertEqual(len(self.graph.breadth_first("B")), 1)
        self.assertIsNone(self.graph.shortest_path("B", "T", EdgeGE.get_moto_time))
        self.bridge.rebuild()
        self.assertIsNotNone(self.graph.shortest_path("B", "T", EdgeGE.get_moto_time))

    def test_requires_exactly_one_base(self):
        self.graph.validate()
        self.graph.add_vertex(VertexGE("B2", 3, 3, PositionType.BASE))
        with self.assertRaises(GraphValidationError):
            self.graph.validate()


class GraphGMTests(unittest.TestCase):
    """Tests for the maze graph."""

    def test_fastest_route_uses_travel_time(self):
        graph = GraphGM()
        entry = VertexGM("IN", 0, 0, MazeVertexRole.ENTRY)
        middle = VertexGM("M", 1, 1)
        exit_vertex = VertexGM("OUT", 2, 0, MazeVertexRole.EXIT)
        for vertex in (entry, middle, exit_vertex):
            graph.add_vertex(vertex)
        graph.add_edge(EdgeGM("direct", entry, exit_vertex, length=10, speed=1))
        graph.add_edge(EdgeGM("a", entry, middle, length=3, speed=1))
        graph.add_edge(EdgeGM("b", middle, exit_vertex, length=3, speed=1))

        route = graph.fastest_route()

        self.assertEqual(route.cost, 6)
        self.assertEqual([vertex.get_id() for vertex in route.vertices], ["IN", "M", "OUT"])
        self.assertEqual([edge.get_id() for edge in route.edges], ["a", "b"])

    def test_requires_entry_and_exit(self):
        graph = GraphGM()
        graph.add_vertex(VertexGM("IN", 0, 0, MazeVertexRole.ENTRY))
        with self.assertRaises(GraphValidationError):
            graph.validate()


if __name__ == "__main__":
    unittest.main()
