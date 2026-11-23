if __package__.startswith("backend."):
    from ..core.grafo.graph import Graph
    from ..core.grafo.graphGE import GraphGE
    from ..core.grafo.graphGM import GraphGM
    from .graph_kind import GraphKind
else:
    from core.grafo.graph import Graph
    from core.grafo.graphGE import GraphGE
    from core.grafo.graphGM import GraphGM
    from domain.graph_kind import GraphKind


class Scenario:
    """A loaded and validated scenario.

    Groups both graphs (already built with the core classes) together with
    the execution parameters and the convoy composition read from the JSON.
    Parameters and convoy are kept as plain dictionaries until their own
    domain entities (towers, soldiers, convoy...) are implemented.
    """

    def __init__(self, name: str, ge: GraphGE, gm: GraphGM,
                 parameters: dict, convoy: dict):
        """Create a scenario.

        Receives:
            name: scenario name.
            ge: validated elevated graph.
            gm: validated maze graph.
            parameters: execution parameters (K, D0, alpha, beta, ...).
            convoy: amount of each enemy unit type.
        Returns:
            None.
        """
        self._name = name
        self._graphs = {GraphKind.GE: ge, GraphKind.GM: gm}
        self._parameters = dict(parameters)
        self._convoy = dict(convoy)

    def get_name(self) -> str:
        """Return the scenario name.

        Receives: nothing.
        Returns:
            str: the name.
        """
        return self._name

    def get_ge(self) -> GraphGE:
        """Return the elevated graph.

        Receives: nothing.
        Returns:
            GraphGE: graph GE.
        """
        return self._graphs[GraphKind.GE]

    def get_gm(self) -> GraphGM:
        """Return the maze graph.

        Receives: nothing.
        Returns:
            GraphGM: graph GM.
        """
        return self._graphs[GraphKind.GM]

    def get_graph(self, kind: GraphKind) -> Graph:
        """Return one of the graphs by kind.

        Receives:
            kind: GraphKind.GE or GraphKind.GM.
        Returns:
            Graph: the requested graph.
        """
        return self._graphs[kind]

    def get_parameters(self) -> dict:
        """Return a copy of the execution parameters.

        Receives: nothing.
        Returns:
            dict: parameters read from the JSON.
        """
        return dict(self._parameters)

    def get_convoy(self) -> dict:
        """Return a copy of the convoy composition.

        Receives: nothing.
        Returns:
            dict: {unit_type: amount}.
        """
        return dict(self._convoy)
