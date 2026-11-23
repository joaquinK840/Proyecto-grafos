if __package__.startswith("backend."):
    from ....domain.scenario import Scenario
    from ....schemas.scenario_schema import ScenarioPayload
    from .build_graph_ge import build_graph_ge
    from .build_graph_gm import build_graph_gm
    from .validate_scenario_references import validate_scenario_references
else:
    from domain.scenario import Scenario
    from schemas.scenario_schema import ScenarioPayload
    from service.scenario.funciones.build_graph_ge import build_graph_ge
    from service.scenario.funciones.build_graph_gm import build_graph_gm
    from service.scenario.funciones.validate_scenario_references import (
        validate_scenario_references,
    )


def build_scenario(payload: ScenarioPayload) -> Scenario:
    """Turn the scenario JSON into a validated Scenario entity.

    Receives:
        payload: scenario JSON (already shape-checked by pydantic).
    Returns:
        Scenario: entity with both graphs built from the core classes.
    How it works:
        Builds GE and GM (each one validates itself), checks the explicit
        references of the JSON and wraps everything in a Scenario.
    Raises:
        ScenarioValidationError: if any rule is broken.
    """
    ge = build_graph_ge(payload.ge)
    gm = build_graph_gm(payload.gm)
    validate_scenario_references(payload, ge, gm)
    return Scenario(
        name=payload.name,
        ge=ge,
        gm=gm,
        parameters=payload.parameters.model_dump(),
        convoy=payload.convoy.model_dump(),
    )
