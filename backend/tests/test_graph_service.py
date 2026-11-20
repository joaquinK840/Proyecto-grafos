import unittest

from backend.service.graph import GraphService
from backend.core.grafo.graph import DuplicateVertexError, VertexNotFoundError


class GraphServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = GraphService()

    def test_create_vertices_and_edge(self):
        first = self.service.add_vertex(1)
        second = self.service.add_vertex(2)
        graph_edge = self.service.add_edge(1, 2, 4)

        self.assertEqual(first.get_name(), 1)
        self.assertEqual(second.get_name(), 2)
        self.assertEqual(graph_edge.get_weight(), 4)
        self.assertEqual(self.service.get_neighbors(1)[0].get_name(), 2)

    def test_reject_duplicate_vertex(self):
        self.service.add_vertex(1)
        with self.assertRaises(DuplicateVertexError):
            self.service.add_vertex(1)

    def test_reject_unknown_vertex(self):
        with self.assertRaises(VertexNotFoundError):
            self.service.get_vertex(99)

    def test_breadth_and_depth_first_traversals(self):
        for vertex_id in (1, 2, 3):
            self.service.add_vertex(vertex_id)
        self.service.add_edge(1, 2, 1)
        self.service.add_edge(1, 3, 1)

        breadth_first = self.service.breadth_first(1)
        depth_first = self.service.depth_first(1)

        self.assertEqual([vertex.get_name() for vertex in breadth_first], [1, 2, 3])
        self.assertEqual([vertex.get_name() for vertex in depth_first], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
