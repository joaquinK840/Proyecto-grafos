if __package__.startswith("backend."):
    from ....core.grafo.graph import Graph
    from ....domain.graph_kind import GraphKind
    from ....repository.scenario_repository import ScenarioRepository
else:
    from core.grafo.graph import Graph
    from domain.graph_kind import GraphKind
    from repository.scenario_repository import ScenarioRepository


def get_graph(repository: ScenarioRepository, kind: GraphKind) -> Graph:
    """Return GE or GM from the loaded scenario.

    Receives:
        repository: storage of the current scenario.
        kind: which graph is requested (GE or GM).
    Returns:
        Graph: the requested graph.
    Raises:
        ScenarioNotLoadedError: if no scenario has been loaded.
    """
    return repository.get_current().get_graph(kind)
