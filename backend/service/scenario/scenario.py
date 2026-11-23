if __package__.startswith("backend."):
    from ...domain.scenario import Scenario
    from ...domain.scenario_summary import ScenarioSummary
    from ...repository.scenario_repository import ScenarioRepository, scenario_repository
    from ...schemas.scenario_schema import ScenarioPayload
    from .funciones.build_scenario import build_scenario
    from .funciones.summarize_scenario import summarize_scenario
else:
    from domain.scenario import Scenario
    from domain.scenario_summary import ScenarioSummary
    from repository.scenario_repository import ScenarioRepository, scenario_repository
    from schemas.scenario_schema import ScenarioPayload
    from service.scenario.funciones.build_scenario import build_scenario
    from service.scenario.funciones.summarize_scenario import summarize_scenario


class ScenarioService:
    """Facade for the scenario use cases.

    It contains no logic: each method delegates to a function in
    ``service/scenario/funciones`` and uses the repository to keep the
    current scenario.
    """

    def __init__(self, repository: ScenarioRepository):
        """Create the service.

        Receives:
            repository: storage where the loaded scenario is kept.
        Returns:
            None.
        """
        self._repository = repository

    def load(self, payload: ScenarioPayload) -> ScenarioSummary:
        """Validate, build and store a scenario.

        Receives:
            payload: scenario JSON.
        Returns:
            ScenarioSummary: summary of the loaded scenario.
        How it works:
            build_scenario -> repository.save -> summarize_scenario. If the
            JSON is invalid nothing is saved and the previous scenario stays.
        Raises:
            ScenarioValidationError: if any rule is broken.
        """
        scenario = build_scenario(payload)
        self._repository.save(scenario)
        return summarize_scenario(scenario)

    def get_current(self) -> Scenario:
        """Return the loaded scenario.

        Receives: nothing.
        Returns:
            Scenario: the current scenario.
        Raises:
            ScenarioNotLoadedError: if none was loaded.
        """
        return self._repository.get_current()

    def get_summary(self) -> ScenarioSummary:
        """Return the summary of the loaded scenario.

        Receives: nothing.
        Returns:
            ScenarioSummary: summary of the current scenario.
        Raises:
            ScenarioNotLoadedError: if none was loaded.
        """
        return summarize_scenario(self._repository.get_current())


scenario_service = ScenarioService(scenario_repository)
