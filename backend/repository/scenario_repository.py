from typing import Optional

if __package__.startswith("backend."):
    from ..domain.scenario import Scenario
    from ..domain.scenario_errors import ScenarioNotLoadedError
else:
    from domain.scenario import Scenario
    from domain.scenario_errors import ScenarioNotLoadedError


class ScenarioRepository:
    """In-memory storage of the current scenario.

    Its only responsibility is to keep the loaded scenario so every service
    (scenario, graph, and future ones) works on the same instance. Services
    receive it through their constructor (dependency inversion), so it can
    be replaced later by another storage without touching them.
    """

    def __init__(self):
        """Create an empty repository.

        Receives: nothing.
        Returns:
            None.
        """
        self._current: Optional[Scenario] = None

    def save(self, scenario: Scenario) -> None:
        """Store a scenario as the current one, replacing the previous.

        Receives:
            scenario: validated scenario.
        Returns:
            None.
        """
        self._current = scenario

    def get_current(self) -> Scenario:
        """Return the current scenario.

        Receives: nothing.
        Returns:
            Scenario: the last saved scenario.
        Raises:
            ScenarioNotLoadedError: if no scenario has been loaded yet.
        """
        if self._current is None:
            raise ScenarioNotLoadedError("no scenario has been loaded yet")
        return self._current

    def has_scenario(self) -> bool:
        """Tell whether a scenario is loaded.

        Receives: nothing.
        Returns:
            bool: True if ``save`` was called at least once.
        """
        return self._current is not None


scenario_repository = ScenarioRepository()
