class VertexNotFoundError(LookupError):
    """Raised when a vertex identifier does not exist in the graph."""


class DuplicateVertexError(ValueError):
    """Raised when adding a vertex whose identifier already exists in the graph."""


class DuplicateEdgeError(ValueError):
    """Raised when adding an edge whose identifier already exists in the graph."""


class GraphValidationError(ValueError):
    """Raised when the graph as a whole breaks one of its invariants.

    Examples: GE without exactly one base, GM without a single entry or
    exit, or GM without a path from entry to exit.
    """
