class vertex:
    """Compatibility vertex for the current integer-identifier API."""

    def __init__(self, name: int):
        if isinstance(name, bool) or not isinstance(name, int):
            raise TypeError("name must be an integer")
        self._name = name
        self._available = True
        self._edges = []

    def get_name(self) -> int:
        return self._name

    def get_id(self) -> int:
        return self._name

    def get_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        if not isinstance(available, bool):
            raise TypeError("available must be a bool")
        self._available = available

    def get_edges(self) -> list:
        return list(self._edges)

    def add_edge(self, edge) -> None:
        if edge not in self._edges:
            self._edges.append(edge)

    def get_neighbors(self) -> list:
        return [edge.get_opposite(self) for edge in self._edges]
