from fastapi import APIRouter

if __package__.startswith("backend."):
    from ..schemas.scenario_schema import ScenarioLoadResponse, ScenarioPayload
    from ..service.scenario.scenario import scenario_service
else:
    from schemas.scenario_schema import ScenarioLoadResponse, ScenarioPayload
    from service.scenario.scenario import scenario_service


router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.post("/load", response_model=ScenarioLoadResponse)
def load_scenario(payload: ScenarioPayload):
    """Validate, build and store a scenario.

    Receives:
        payload: scenario JSON (request body).
    Returns:
        ScenarioLoadResponse: summary of the loaded scenario.
    """
    return ScenarioLoadResponse.from_summary(scenario_service.load(payload))


@router.get("/current", response_model=ScenarioLoadResponse)
def get_current_scenario():
    """Return the summary of the scenario currently loaded.

    Receives: nothing.
    Returns:
        ScenarioLoadResponse: summary of the current scenario (409 if none).
    """
    return ScenarioLoadResponse.from_summary(scenario_service.get_summary())
