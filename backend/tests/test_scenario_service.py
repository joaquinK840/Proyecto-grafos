import unittest

from pydantic import ValidationError

from backend.domain.scenario import ScenarioValidationError
from backend.schemas.scenario_schemas import ScenarioPayload
from backend.service.scenario import ScenarioService


VALID_SCENARIO = {
    "name": "Escenario de prueba",
    "ge": {
        "vertices": [
            {"id": "B", "x": 1, "y": 1, "position_type": "base"},
            {"id": "T1", "x": 2, "y": 2, "position_type": "tower_candidate"},
        ],
        "edges": [
            {
                "id": "E1",
                "v1": "B",
                "v2": "T1",
                "connection_type": "path",
                "foot_time": 5,
                "moto_time": 2,
            }
        ],
    },
    "gm": {
        "vertices": [
            {"id": "IN", "x": 0, "y": 0, "role": "entry"},
            {"id": "M1", "x": 1, "y": 0, "role": "normal"},
            {"id": "OUT", "x": 2, "y": 0, "role": "exit"},
        ],
        "edges": [
            {"id": "M-E1", "v1": "IN", "v2": "M1", "length": 10, "speed": 2},
            {"id": "M-E2", "v1": "M1", "v2": "OUT", "length": 10, "speed": 2},
        ],
    },
    "base_id": "B",
    "entry_id": "IN",
    "exit_id": "OUT",
    "parameters": {
        "tower_limit": 2,
        "reference_time": 10,
        "danger_alpha": 0.5,
        "height_beta": 0.2,
    },
}


class ScenarioServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = ScenarioService()

    def test_load_valid_scenario_and_find_shortest_maze_time(self):
        payload = ScenarioPayload.model_validate(VALID_SCENARIO)
        summary = self.service.load(payload)

        self.assertEqual(summary.ge_vertex_count, 2)
        self.assertEqual(summary.ge_edge_count, 1)
        self.assertEqual(summary.gm_vertex_count, 3)
        self.assertEqual(summary.gm_edge_count, 2)
        self.assertEqual(summary.shortest_maze_time, 10)

    def test_reject_duplicate_vertex_identifier(self):
        scenario = {
            **VALID_SCENARIO,
            "ge": {
                "vertices": [
                    *VALID_SCENARIO["ge"]["vertices"],
                    {"id": "B", "x": 3, "y": 3, "position_type": "transit"},
                ],
                "edges": VALID_SCENARIO["ge"]["edges"],
            },
        }

        with self.assertRaises(ScenarioValidationError):
            payload = ScenarioPayload.model_validate(scenario)
            self.service.load(payload)

    def test_reject_missing_maze_path(self):
        scenario = {
            **VALID_SCENARIO,
            "gm": {
                "vertices": VALID_SCENARIO["gm"]["vertices"],
                "edges": [
                    {"id": "M-E1", "v1": "IN", "v2": "M1", "length": 10, "speed": 2}
                ],
            },
        }

        with self.assertRaises(ScenarioValidationError):
            payload = ScenarioPayload.model_validate(scenario)
            self.service.load(payload)

    def test_reject_unknown_enum_value(self):
        scenario = {
            **VALID_SCENARIO,
            "ge": {
                "vertices": [
                    {
                        "id": "B",
                        "x": 1,
                        "y": 1,
                        "position_type": "unknown",
                    }
                ],
                "edges": [],
            },
        }

        with self.assertRaises(ValidationError):
            ScenarioPayload.model_validate(scenario)


if __name__ == "__main__":
    unittest.main()
