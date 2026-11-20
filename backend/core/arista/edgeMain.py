if __package__.startswith("backend."):
    from ..vertice.vertexMain import VertexMain
    from ..validaciones.number_validator import validate_identifier
else:
    from core.vertice.vertexMain import VertexMain
    from core.validaciones.number_validator import validate_identifier


class EdgeMain:
    """Base undirected edge shared by both graphs (GE and GM).

    Holds what every edge needs regardless of its graph: an immutable
    identifier (edges keep their identity during the simulation), its two
    endpoint vertices and an enabled/disabled flag.

    Subclasses set ``VERTEX_TYPE`` to restrict which vertex class they can
    join, so a GE edge can never link GM vertices and vice versa.
    """

    VERTEX_TYPE = VertexMain

    def __init__(self, edge_id: str, v1: VertexMain, v2: VertexMain, enabled: bool = True):
        """Create an undirected edge.

        Receives:
            edge_id: unique identifier inside its graph (non-empty str).
            v1: one endpoint vertex.
            v2: the other endpoint vertex.
            enabled: initial availability, True by default.
        Returns:
            None.
        How it works:
            Validates the identifier, checks both endpoints are instances of
            ``VERTEX_TYPE`` and different from each other (no self loops),
            and stores everything. It does NOT register itself in the
            vertices: that is the graph's job.
        Raises:
            TypeError / ValueError: if any value breaks the rules.
        """
        self._id = validate_identifier(edge_id, "edge_id")
        self._v1 = self._validate_vertex(v1, "v1")
        self._v2 = self._validate_vertex(v2, "v2")
        if self._v1 is self._v2 or self._v1.get_id() == self._v2.get_id():
            raise ValueError(f"edge {edge_id} cannot connect a vertex with itself")
        self._enabled = self._validate_enabled(enabled)

    @classmethod
    def _validate_vertex(cls, vertex, field_name: str):
        """Validate that an endpoint has the vertex type this edge accepts.

        Receives:
            vertex: candidate endpoint.
            field_name: "v1" or "v2", used in the error message.
        Returns:
            VertexMain: the same vertex once validated.
        Raises:
            TypeError: if it is not an instance of ``VERTEX_TYPE``.
        """
        if not isinstance(vertex, cls.VERTEX_TYPE):
            raise TypeError(f"{field_name} must be a {cls.VERTEX_TYPE.__name__}")
        return vertex

    @staticmethod
    def _validate_enabled(enabled) -> bool:
        """Validate the enabled flag.

        Receives:
            enabled: candidate value.
        Returns:
            bool: the same value once validated.
        Raises:
            TypeError: if it is not a bool.
        """
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a bool")
        return enabled

    def get_id(self) -> str:
        """Return the edge identifier.

        Receives: nothing.
        Returns:
            str: the identifier. There is no setter, so it is immutable.
        """
        return self._id

    def get_v1(self) -> VertexMain:
        """Return the first endpoint.

        Receives: nothing.
        Returns:
            VertexMain: first endpoint vertex.
        """
        return self._v1

    def get_v2(self) -> VertexMain:
        """Return the second endpoint.

        Receives: nothing.
        Returns:
            VertexMain: second endpoint vertex.
        """
        return self._v2

    def get_endpoints(self) -> tuple:
        """Return both endpoints.

        Receives: nothing.
        Returns:
            tuple[VertexMain, VertexMain]: the pair (v1, v2).
        """
        return (self._v1, self._v2)

    def connects(self, vertex: VertexMain) -> bool:
        """Tell whether a vertex is one of the endpoints.

        Receives:
            vertex: vertex to look for.
        Returns:
            bool: True if ``vertex`` is v1 or v2 (compared by identity).
        """
        return vertex is self._v1 or vertex is self._v2

    def get_opposite(self, vertex: VertexMain) -> VertexMain:
        """Return the endpoint at the other side of the edge.

        Receives:
            vertex: one of the endpoints.
        Returns:
            VertexMain: the other endpoint. Since the edge is undirected it
            can be traversed from either side.
        Raises:
            ValueError: if ``vertex`` is not an endpoint of this edge.
        """
        if vertex is self._v1:
            return self._v2
        if vertex is self._v2:
            return self._v1
        raise ValueError(f"vertex {vertex.get_id()} is not an endpoint of edge {self._id}")

    def is_enabled(self) -> bool:
        """Return the raw enabled flag.

        Receives: nothing.
        Returns:
            bool: True if the edge has not been manually disabled.
        """
        return self._enabled

    def enable(self) -> None:
        """Enable the edge.

        Receives: nothing.
        Returns:
            None.
        """
        self._enabled = True

    def disable(self) -> None:
        """Disable the edge without removing it (it keeps its identity and data).

        Receives: nothing.
        Returns:
            None.
        """
        self._enabled = False

    def is_available(self) -> bool:
        """Tell whether the edge can currently be used by searches.

        Receives: nothing.
        Returns:
            bool: in the base class it equals ``is_enabled``. Subclasses
            extend it with their own state (for example destroyed bridges).
        """
        return self._enabled

    def __repr__(self) -> str:
        """Return a readable representation for debugging.

        Receives: nothing.
        Returns:
            str: class name, identifier and endpoint identifiers.
        """
        return f"{type(self).__name__}(id={self._id!r}, {self._v1.get_id()!r}<->{self._v2.get_id()!r})"
