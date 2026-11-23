from dataclasses import dataclass


@dataclass(frozen=True)
class PathResult:
    """Immutable result of a shortest path search.

    Attributes:
        vertices: ordered list of vertices from origin to destination.
        edges: ordered list of the edges traversed (len = len(vertices) - 1).
        cost: total cost of the path according to the weight function used.
    """

    vertices: list
    edges: list
    cost: float
