from typing import Callable

if __package__.startswith("backend."):
    from ..graph_errors import GraphValidationError
    from ..path_result import PathResult
    from .shortest_path import shortest_path
else:
    from core.grafo.graph_errors import GraphValidationError
    from core.grafo.path_result import PathResult
    from core.grafo.funciones.shortest_path import shortest_path


def require_path(origin, destination, weight: Callable) -> PathResult:
    """Return the minimum cost path and fail if it does not exist.

    Receives:
        origin: start vertex.
        destination: target vertex.
        weight: function edge -> non-negative cost.
    Returns:
        PathResult: the minimum cost path.
    How it works:
        Runs ``shortest_path`` and turns a missing path (None) into a graph
        validation error. It is used for the rule "there must initially be
        a path between entry and exit" in GM.
    Raises:
        GraphValidationError: if the destination is unreachable.
    """
    result = shortest_path(origin, destination, weight)
    if result is None:
        raise GraphValidationError(
            f"there is no path from {origin.get_id()} to {destination.get_id()}"
        )
    return result
