import unittest

from backend.core.grafo.graph_errors import VertexNotFoundError
from backend.domain.graph_kind import GraphKind
from backend.domain.scenario_errors import ScenarioNotLoadedError
from backend.repository.scenario_repository import ScenarioRepository
from backend.schemas.scenario_schema import ScenarioPayload
from backend.service.graph.graph import GraphService
from backend.service.scenario.scenario import ScenarioService
from backend.tests.scenario_fixtures import scenario_copy


def _ids(items) -> list:
    """Return the identifiers of a list of vertices."""
    return [item.get_id() for item in items]


class GraphServiceTests(unittest.TestCase):
    """Tests for the graph facade over the loaded scenario."""

    def setUp(self):
        """Load the shared scenario into a fresh repository."""
        repository = ScenarioRepository()
        self.service = GraphService(repository)
        ScenarioService(repository).load(ScenarioPayload.model_validate(scenario_copy()))

    def test_list_vertices_and_edges_of_each_graph(self):
        self.assertEqual(_ids(self.service.get_vertices(GraphKind.GE)), ["B", "T1", "H1"])
        self.assertEqual(len(self.service.get_edges(GraphKind.GM)), 4)

    def test_neighbors_are_undirected(self):
        self.assertEqual(_ids(self.service.get_neighbors(GraphKind.GE, "T1")), ["B", "H1"])

    def test_breadth_and_depth_first(self):
        self.assertEqual(_ids(self.service.breadth_first(GraphKind.GM, "IN")), ["IN", "M1", "M2", "OUT"])
        self.assertEqual(_ids(self.service.depth_first(GraphKind.GM, "IN")), ["IN", "M1", "OUT", "M2"])

    def test_unknown_vertex(self):
        with self.assertRaises(VertexNotFoundError):
            self.service.get_vertex(GraphKind.GE, "ZZ")

    def test_requires_loaded_scenario(self):
        with self.assertRaises(ScenarioNotLoadedError):
            GraphService(ScenarioRepository()).get_vertices(GraphKind.GE)


if __name__ == "__main__":
    unittest.main()
