class edge:
    """Compatibility undirected edge for the current weighted graph API."""

    def __init__(self, v1, v2, weight: int):
        if isinstance(weight, bool) or not isinstance(weight, int):
            raise TypeError("weight must be an integer")
        self._v1 = v1
        self._v2 = v2
        self._weight = weight
        self._available = True

    def get_v1(self):
        return self._v1

    def get_v2(self):
        return self._v2

    def get_endpoints(self) -> tuple:
        return (self._v1, self._v2)

    def get_weight(self) -> int:
        return self._weight

    def get_available(self) -> bool:
        return self._available

    def connects(self, vertex) -> bool:
        return vertex is self._v1 or vertex is self._v2

    def get_opposite(self, vertex):
        if vertex is self._v1:
            return self._v2
        if vertex is self._v2:
            return self._v1
        raise ValueError("vertex is not an endpoint of this edge")

    def is_available(self) -> bool:
        return self._available
