if __package__.startswith("backend."):
    from ....core.grafo.graphGE import GraphGE
    from ....core.grafo.graphGM import GraphGM
    from ....domain.scenario_errors import ScenarioValidationError
    from ....schemas.scenario_schema import ScenarioPayload
else:
    from core.grafo.graphGE import GraphGE
    from core.grafo.graphGM import GraphGM
    from domain.scenario_errors import ScenarioValidationError
    from schemas.scenario_schema import ScenarioPayload


def validate_scenario_references(payload: ScenarioPayload, ge: GraphGE, gm: GraphGM) -> None:
    """Check that the JSON references match the special vertices.

    Receives:
        payload: scenario JSON, with ``base_id``, ``entry_id``, ``exit_id``.
        ge: built and validated GE (it already has exactly one base).
        gm: built and validated GM (single entry and exit).
    Returns:
        None.
    How it works:
        This is the only rule that belongs to the scenario and not to a
        graph: the explicit ids in the JSON must point to the vertices
        marked as base / entry / exit. Compares each pair and fails on the
        first mismatch.
    Raises:
        ScenarioValidationError: if a reference does not match.
    """
    references = (
        ("base_id", payload.base_id, ge.get_base().get_id()),
        ("entry_id", payload.entry_id, gm.get_entry().get_id()),
        ("exit_id", payload.exit_id, gm.get_exit().get_id()),
    )
    for field_name, declared, actual in references:
        if declared != actual:
            raise ScenarioValidationError(
                f"{field_name} is '{declared}' but the marked vertex is '{actual}'"
            )
