if __package__.startswith("backend."):
    from ..validaciones.number_validator import validate_identifier, validate_finite
else:
    from core.validaciones.number_validator import validate_identifier, validate_finite


class VertexMain:
    """Base vertex shared by both graphs (GE and GM).

    Holds the attributes every vertex must have regardless of the graph it
    belongs to: an immutable identifier, finite 2D coordinates and the list
    of incident edges (adjacency list).

    Subclasses add their own attributes and may tighten the coordinate rule
    by overriding ``_validate_coordinate`` (Open/Closed principle).
    """

    def __init__(self, vertex_id: str, x: float, y: float):
        """Create a vertex.

        Receives:
            vertex_id: unique identifier inside its graph (non-empty str).
            x: horizontal coordinate.
            y: vertical coordinate.
        Returns:
            None.
        How it works:
            Validates the identifier and each coordinate (through the
            overridable ``_validate_coordinate`` hook) and starts with an
            empty list of incident edges.
        Raises:
            TypeError / ValueError: if any value breaks the rules.
        """
        self._id = validate_identifier(vertex_id, "vertex_id")
        self._x = self._validate_coordinate(x, "x")
        self._y = self._validate_coordinate(y, "y")
        self._edges = []

    def _validate_coordinate(self, value, field_name: str) -> float:
        """Validate a single coordinate.

        Receives:
            value: candidate coordinate.
            field_name: "x" or "y", used in the error message.
        Returns:
            float: the validated coordinate.
        How it works:
            The base rule only requires a finite number. Subclasses override
            this method to add stricter rules.
        """
        return validate_finite(value, field_name)

    def get_id(self) -> str:
        """Return the vertex identifier.

        Receives: nothing.
        Returns:
            str: the identifier. There is no setter, so it is immutable.
        """
        return self._id

    def get_x(self) -> float:
        """Return the horizontal coordinate.

        Receives: nothing.
        Returns:
            float: x coordinate.
        """
        return self._x

    def get_y(self) -> float:
        """Return the vertical coordinate.

        Receives: nothing.
        Returns:
            float: y coordinate.
        """
        return self._y

    def get_coordinates(self) -> tuple:
        """Return both coordinates.

        Receives: nothing.
        Returns:
            tuple[float, float]: the pair (x, y).
        """
        return (self._x, self._y)

    def set_coordinates(self, x: float, y: float) -> None:
        """Update the coordinates of the vertex.

        Receives:
            x: new horizontal coordinate.
            y: new vertical coordinate.
        Returns:
            None.
        How it works:
            Validates both values first and only then assigns them, so the
            vertex never ends in a half-updated state.
        """
        new_x = self._validate_coordinate(x, "x")
        new_y = self._validate_coordinate(y, "y")
        self._x, self._y = new_x, new_y

    def get_edges(self) -> list:
        """Return the incident edges of the vertex.

        Receives: nothing.
        Returns:
            list: a copy of the incident edge list, so callers cannot
            modify the adjacency list directly.
        """
        return list(self._edges)

    def add_edge(self, edge) -> None:
        """Register an incident edge in the adjacency list.

        Receives:
            edge: an edge (EdgeMain or subclass) that touches this vertex.
        Returns:
            None.
        How it works:
            Checks the edge actually connects this vertex and that it was
            not already registered, then appends it.
        Raises:
            ValueError: if the edge does not touch this vertex or is
            already registered.
        """
        if not edge.connects(self):
            raise ValueError(f"edge {edge.get_id()} does not touch vertex {self._id}")
        if edge in self._edges:
            raise ValueError(f"edge {edge.get_id()} is already registered in vertex {self._id}")
        self._edges.append(edge)

    def get_neighbors(self) -> list:
        """Return the neighbor vertices reachable through incident edges.

        Receives: nothing.
        Returns:
            list: the vertex at the opposite end of every incident edge,
            no matter whether the edge is currently available.
        How it works:
            Asks each incident edge for the vertex opposite to this one.
        """
        return [edge.get_opposite(self) for edge in self._edges]

    def __repr__(self) -> str:
        """Return a readable representation for debugging.

        Receives: nothing.
        Returns:
            str: class name, identifier and coordinates.
        """
        return f"{type(self).__name__}(id={self._id!r}, x={self._x}, y={self._y})"
