import unittest

from pydantic import ValidationError

from backend.domain.scenario_errors import ScenarioNotLoadedError, ScenarioValidationError
from backend.repository.scenario_repository import ScenarioRepository
from backend.schemas.scenario_schema import ScenarioPayload
from backend.service.scenario.scenario import ScenarioService
from backend.tests.scenario_fixtures import scenario_copy


class ScenarioServiceTests(unittest.TestCase):
    """Tests for loading scenarios through the scenario facade."""

    def setUp(self):
        """Create a service with its own empty repository."""
        self.repository = ScenarioRepository()
        self.service = ScenarioService(self.repository)

    def _load(self, data: dict):
        """Validate the JSON shape and load it."""
        return self.service.load(ScenarioPayload.model_validate(data))

    def _assert_rejected(self, data: dict, text: str):
        """Check the scenario is rejected with a message containing ``text``."""
        with self.assertRaises(ScenarioValidationError) as context:
            self._load(data)
        self.assertIn(text, str(context.exception))
        self.assertFalse(self.repository.has_scenario())

    def test_load_valid_scenario_builds_core_graphs(self):
        summary = self._load(scenario_copy())

        self.assertEqual(summary.ge_vertex_count, 3)
        self.assertEqual(summary.ge_edge_count, 2)
        self.assertEqual(summary.gm_vertex_count, 4)
        self.assertEqual(summary.gm_edge_count, 4)
        self.assertEqual(summary.shortest_maze_time, 2)
        self.assertEqual(summary.shortest_maze_route, ["IN", "M2", "OUT"])
        self.assertEqual(summary.shortest_maze_route_edges, ["C3", "C4"])
        scenario = self.service.get_current()
        self.assertTrue(scenario.get_ge().get_vertex("B").is_base())
        self.assertEqual(scenario.get_gm().get_entry().get_id(), "IN")

    def test_reject_duplicate_vertex_identifier(self):
        data = scenario_copy()
        data["ge"]["vertices"].append({"id": "B", "x": 3, "y": 3, "position_type": "transit"})
        self._assert_rejected(data, "GE vertex B")

    def test_reject_duplicate_edge_identifier(self):
        data = scenario_copy()
        data["gm"]["edges"].append({"id": "C1", "v1": "M1", "v2": "M2", "length": 1, "speed": 1})
        self._assert_rejected(data, "GM edge C1")

    def test_reject_non_positive_ge_coordinate(self):
        data = scenario_copy()
        data["ge"]["vertices"][1]["x"] = 0
        self._assert_rejected(data, "GE vertex T1")

    def test_reject_two_bases(self):
        data = scenario_copy()
        data["ge"]["vertices"][1]["position_type"] = "base"
        self._assert_rejected(data, "exactly one base")

    def test_reject_edge_to_unknown_vertex(self):
        data = scenario_copy()
        data["ge"]["edges"][0]["v2"] = "ZZ"
        self._assert_rejected(data, "GE edge E1")

    def test_reject_bridge_without_resistance(self):
        data = scenario_copy()
        del data["ge"]["edges"][1]["max_resistance"]
        self._assert_rejected(data, "GE edge E2")

    def test_reject_missing_maze_path(self):
        data = scenario_copy()
        data["gm"]["edges"] = [data["gm"]["edges"][0]]
        self._assert_rejected(data, "no path")

    def test_reject_reference_mismatch(self):
        data = scenario_copy()
        data["exit_id"] = "M1"
        self._assert_rejected(data, "exit_id")

    def test_reject_unknown_enum_value(self):
        data = scenario_copy()
        data["ge"]["vertices"][0]["position_type"] = "unknown"
        with self.assertRaises(ValidationError):
            ScenarioPayload.model_validate(data)

    def test_failed_load_keeps_previous_scenario(self):
        self._load(scenario_copy())
        data = scenario_copy()
        data["name"] = "Otro"
        data["gm"]["edges"] = []
        with self.assertRaises(ScenarioValidationError):
            self._load(data)
        self.assertEqual(self.service.get_current().get_name(), "Escenario de prueba")

    def test_no_scenario_loaded(self):
        with self.assertRaises(ScenarioNotLoadedError):
            self.service.get_current()


if __name__ == "__main__":
    unittest.main()
