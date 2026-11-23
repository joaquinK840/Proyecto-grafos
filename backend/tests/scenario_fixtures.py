"""Shared test data: a small valid scenario JSON."""
import copy


VALID_SCENARIO = {
    "name": "Escenario de prueba",
    "ge": {
        "vertices": [
            {"id": "B", "x": 1, "y": 1, "position_type": "base"},
            {"id": "T1", "x": 2, "y": 2, "position_type": "tower_candidate"},
            {"id": "H1", "x": 3, "y": 1, "position_type": "heliport"},
        ],
        "edges": [
            {"id": "E1", "v1": "B", "v2": "T1", "connection_type": "path",
             "foot_time": 5, "moto_time": 2},
            {"id": "E2", "v1": "T1", "v2": "H1", "connection_type": "bridge",
             "foot_time": 4, "moto_time": 1, "max_resistance": 3},
        ],
    },
    "gm": {
        "vertices": [
            {"id": "IN", "x": 0, "y": 0, "role": "entry"},
            {"id": "M1", "x": 1, "y": 0},
            {"id": "M2", "x": 1, "y": 5},
            {"id": "OUT", "x": 2, "y": 0, "role": "exit"},
        ],
        "edges": [
            {"id": "C1", "v1": "IN", "v2": "M1", "length": 10, "speed": 2},
            {"id": "C2", "v1": "M1", "v2": "OUT", "length": 10, "speed": 2},
            {"id": "C3", "v1": "IN", "v2": "M2", "length": 4, "speed": 4},
            {"id": "C4", "v1": "M2", "v2": "OUT", "length": 4, "speed": 4},
        ],
    },
    "base_id": "B",
    "entry_id": "IN",
    "exit_id": "OUT",
    "parameters": {"tower_limit": 2, "reference_time": 10},
}


def scenario_copy() -> dict:
    """Return a deep copy of the valid scenario so a test can modify it.

    Receives: nothing.
    Returns:
        dict: independent copy of ``VALID_SCENARIO``.
    """
    return copy.deepcopy(VALID_SCENARIO)
