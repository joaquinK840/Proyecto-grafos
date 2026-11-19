from core.arista.edgeMain import EdgeMain
from core.vertice.vertexGM import VertexGM
from core.validaciones.number_validator import validate_positive


class EdgeGM(EdgeMain):
    """Edge of the maze graph GM (a corridor).

    Inherits identifier, endpoints and enabled flag from EdgeMain and adds
    the corridor length and allowed speed, both strictly positive. Every
    corridor starts enabled and is never destroyed; only its cost may
    change (danger is added on top of the travel time by the routing
    service).
    """

    VERTEX_TYPE = VertexGM

    def __init__(self, edge_id: str, v1: VertexGM, v2: VertexGM, length: float, speed: float):
        """Create a GM corridor.

        Receives:
            edge_id: unique identifier inside GM.
            v1, v2: VertexGM endpoints.
            length: corridor length l(e), finite and > 0.
            speed: allowed speed v(e), finite and > 0.
        Returns:
            None.
        How it works:
            Delegates common data to EdgeMain forcing ``enabled=True`` (all
            corridors start enabled) and validates length and speed.
        Raises:
            TypeError / ValueError: if any value breaks the GM rules.
        """
        super().__init__(edge_id, v1, v2, enabled=True)
        self._length = validate_positive(length, "length")
        self._speed = validate_positive(speed, "speed")

    def get_length(self) -> float:
        """Return the corridor length.

        Receives: nothing.
        Returns:
            float: length l(e).
        """
        return self._length

    def get_speed(self) -> float:
        """Return the corridor allowed speed.

        Receives: nothing.
        Returns:
            float: speed v(e).
        """
        return self._speed

    def get_travel_time(self) -> float:
        """Return the base travel time of the corridor.

        Receives: nothing.
        Returns:
            float: t(e) = l(e) / v(e), in seconds.
        """
        return self._length / self._speed

    def get_midpoint(self) -> tuple:
        """Return the midpoint of the corridor.

        Receives: nothing.
        Returns:
            tuple[float, float]: (x, y) halfway between both endpoints. It
            is used for tower coverage and danger estimation.
        """
        x1, y1 = self._v1.get_coordinates()
        x2, y2 = self._v2.get_coordinates()
        return ((x1 + x2) / 2, (y1 + y2) / 2)
