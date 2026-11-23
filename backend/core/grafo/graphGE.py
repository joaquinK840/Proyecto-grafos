if __package__.startswith("backend."):
    from .graph import Graph
    from ..vertice.vertexGE import VertexGE
    from ..arista.edgeGE import EdgeGE
    from .funciones.find_unique_vertex import find_unique_vertex
else:
    from core.grafo.graph import Graph
    from core.vertice.vertexGE import VertexGE
    from core.arista.edgeGE import EdgeGE
    from core.grafo.funciones.find_unique_vertex import find_unique_vertex


class GraphGE(Graph):
    """Elevated graph GE: terrain positions joined by paths and bridges.

    Only accepts VertexGE / EdgeGE elements and adds the global rule
    "each scenario has exactly one base".
    """

    VERTEX_TYPE = VertexGE
    EDGE_TYPE = EdgeGE

    def get_base(self) -> VertexGE:
        """Return the base position.

        Receives: nothing.
        Returns:
            VertexGE: the only vertex whose type is BASE.
        How it works:
            Delegates to ``funciones.find_unique_vertex`` with
            ``VertexGE.is_base`` as condition.
        Raises:
            GraphValidationError: if there is not exactly one base.
        """
        return find_unique_vertex(self.get_vertices(), VertexGE.is_base, "base")

    def validate(self) -> None:
        """Check the GE global rules.

        Receives: nothing.
        Returns:
            None.
        How it works:
            Requires exactly one base (through ``get_base``). Per-vertex and
            per-edge rules were already checked by their constructors.
        Raises:
            GraphValidationError: if a rule is broken.
        """
        self.get_base()
