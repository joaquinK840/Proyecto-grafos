from typing import Callable

if __package__.startswith("backend."):
    from ..graph_errors import GraphValidationError
else:
    from core.grafo.graph_errors import GraphValidationError


def find_unique_vertex(vertices, predicate: Callable, description: str):
    """Return the only vertex that satisfies a condition.

    Receives:
        vertices: iterable of vertices to inspect.
        predicate: function vertex -> bool (for example ``VertexGE.is_base``).
        description: human readable name of what is searched ("base",
            "entry", "exit"), used in error messages.
    Returns:
        VertexMain: the single matching vertex.
    How it works:
        Collects every vertex for which the predicate is True and requires
        exactly one. It is used for rules such as "exactly one base in GE"
        or "a single entry and a single exit in GM".
    Raises:
        GraphValidationError: if there are zero or several matches.
    """
    matches = [vertex for vertex in vertices if predicate(vertex)]
    if len(matches) != 1:
        found = ", ".join(vertex.get_id() for vertex in matches) or "none"
        raise GraphValidationError(
            f"the graph must contain exactly one {description} (found: {found})"
        )
    return matches[0]
