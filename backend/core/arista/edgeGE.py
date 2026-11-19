from typing import Optional

if __package__.startswith("backend."):
    from .edgeMain import EdgeMain
    from .connection_type import ConnectionType
    from ..vertice.vertexGE import VertexGE
    from ..validaciones.number_validator import validate_positive, validate_positive_int
else:
    from core.arista.edgeMain import EdgeMain
    from core.arista.connection_type import ConnectionType
    from core.vertice.vertexGE import VertexGE
    from core.validaciones.number_validator import validate_positive, validate_positive_int


class EdgeGE(EdgeMain):
    """Edge of the elevated graph GE (a path or a bridge).

    Inherits identifier, endpoints and enabled flag from EdgeMain and adds:
        - Connection type (PATH or BRIDGE).
        - Travel time on foot and by motorcycle. ``None`` means that
          transport mode is not allowed on this edge; when allowed the time
          must be positive.
        - For bridges only: maximum and current resistance (positive
          integers at creation, current <= maximum).

    A bridge whose current resistance reaches zero is destroyed: it stops
    being available for new crossings but keeps all its data so it can be
    rebuilt later.
    """

    VERTEX_TYPE = VertexGE

    def __init__(self, edge_id: str, v1: VertexGE, v2: VertexGE,
                 connection_type: ConnectionType,
                 foot_time: Optional[float] = None,
                 moto_time: Optional[float] = None,
                 max_resistance: Optional[int] = None,
                 current_resistance: Optional[int] = None,
                 enabled: bool = True):
        """Create a GE edge.

        Receives:
            edge_id: unique, immutable identifier inside GE.
            v1, v2: VertexGE endpoints.
            connection_type: ConnectionType (PATH or BRIDGE).
            foot_time: seconds on foot, or None if walking is not allowed.
            moto_time: seconds by motorcycle, or None if not allowed.
            max_resistance: bridge maximum resistance (bridges only).
            current_resistance: bridge initial resistance (bridges only).
                If omitted for a bridge it starts equal to max_resistance.
            enabled: initial enabled flag, True by default.
        Returns:
            None.
        How it works:
            Delegates common data to EdgeMain, validates the connection
            type, the transport times (at least one mode must be allowed)
            and, depending on the type, the resistance values.
        Raises:
            TypeError / ValueError: if any value breaks the GE rules.
        """
        super().__init__(edge_id, v1, v2, enabled)
        self._connection_type = self._validate_connection_type(connection_type)
        self._foot_time = self._validate_optional_time(foot_time, "foot_time")
        self._moto_time = self._validate_optional_time(moto_time, "moto_time")
        if self._foot_time is None and self._moto_time is None:
            raise ValueError(f"edge {edge_id} must allow at least one transport mode")
        self._max_resistance, self._current_resistance = self._validate_resistances(
            max_resistance, current_resistance
        )

    @staticmethod
    def _validate_connection_type(connection_type) -> ConnectionType:
        """Validate the connection type.

        Receives:
            connection_type: candidate value.
        Returns:
            ConnectionType: the same value once validated.
        Raises:
            TypeError: if it is not a ConnectionType member.
        """
        if not isinstance(connection_type, ConnectionType):
            raise TypeError("connection_type must be a ConnectionType")
        return connection_type

    @staticmethod
    def _validate_optional_time(time_value, field_name: str) -> Optional[float]:
        """Validate a transport time that may be absent.

        Receives:
            time_value: None (mode not allowed) or a candidate time.
            field_name: name of the field, used in the error message.
        Returns:
            Optional[float]: None, or the validated positive time.
        """
        if time_value is None:
            return None
        return validate_positive(time_value, field_name)

    def _validate_resistances(self, max_resistance, current_resistance) -> tuple:
        """Validate resistance values according to the connection type.

        Receives:
            max_resistance: candidate maximum resistance.
            current_resistance: candidate current resistance.
        Returns:
            tuple[Optional[int], Optional[int]]: (max, current). Both are
            None for paths.
        How it works:
            - PATH: both values must be None.
            - BRIDGE: max is required and must be a positive int; current
              defaults to max, must be a positive int and not exceed max.
        Raises:
            TypeError / ValueError: if the values break the rules.
        """
        if not self.is_bridge():
            if max_resistance is not None or current_resistance is not None:
                raise ValueError(f"edge {self._id} is a path and cannot have resistance")
            return None, None

        if max_resistance is None:
            raise ValueError(f"bridge {self._id} requires max_resistance")
        maximum = validate_positive_int(max_resistance, "max_resistance")
        current = maximum if current_resistance is None else validate_positive_int(
            current_resistance, "current_resistance"
        )
        if current > maximum:
            raise ValueError(f"bridge {self._id}: current_resistance cannot exceed max_resistance")
        return maximum, current

    def get_connection_type(self) -> ConnectionType:
        """Return the connection type.

        Receives: nothing.
        Returns:
            ConnectionType: PATH or BRIDGE.
        """
        return self._connection_type

    def is_bridge(self) -> bool:
        """Tell whether the edge is a bridge.

        Receives: nothing.
        Returns:
            bool: True if the connection type is BRIDGE.
        """
        return self._connection_type is ConnectionType.BRIDGE

    def allows_foot(self) -> bool:
        """Tell whether walking is allowed on this edge.

        Receives: nothing.
        Returns:
            bool: True if a foot time was defined.
        """
        return self._foot_time is not None

    def allows_moto(self) -> bool:
        """Tell whether motorcycles are allowed on this edge.

        Receives: nothing.
        Returns:
            bool: True if a motorcycle time was defined.
        """
        return self._moto_time is not None

    def get_foot_time(self) -> Optional[float]:
        """Return the travel time on foot.

        Receives: nothing.
        Returns:
            Optional[float]: seconds on foot, or None if not allowed.
        """
        return self._foot_time

    def get_moto_time(self) -> Optional[float]:
        """Return the travel time by motorcycle.

        Receives: nothing.
        Returns:
            Optional[float]: seconds by motorcycle, or None if not allowed.
        """
        return self._moto_time

    def get_max_resistance(self) -> Optional[int]:
        """Return the bridge maximum resistance.

        Receives: nothing.
        Returns:
            Optional[int]: maximum resistance, or None for paths.
        """
        return self._max_resistance

    def get_current_resistance(self) -> Optional[int]:
        """Return the bridge current resistance.

        Receives: nothing.
        Returns:
            Optional[int]: current resistance, or None for paths.
        """
        return self._current_resistance

    def is_destroyed(self) -> bool:
        """Tell whether the bridge has collapsed.

        Receives: nothing.
        Returns:
            bool: True only for bridges whose current resistance is zero.
            Paths are never destroyed.
        """
        return self.is_bridge() and self._current_resistance == 0

    def wear_down(self) -> None:
        """Reduce the bridge current resistance by one.

        Receives: nothing.
        Returns:
            None.
        How it works:
            Called when a motorcycle finishes crossing the bridge. When the
            resistance reaches zero the bridge becomes destroyed (see
            ``is_destroyed``) but keeps its data.
        Raises:
            ValueError: if the edge is not a bridge or is already destroyed.
        """
        if not self.is_bridge():
            raise ValueError(f"edge {self._id} is not a bridge")
        if self.is_destroyed():
            raise ValueError(f"bridge {self._id} is already destroyed")
        self._current_resistance -= 1

    def rebuild(self) -> None:
        """Restore the bridge to its maximum resistance.

        Receives: nothing.
        Returns:
            None.
        How it works:
            Sets the current resistance back to the maximum. The waiting
            time and the people needed are handled by the simulation, not
            by the edge.
        Raises:
            ValueError: if the edge is not a bridge.
        """
        if not self.is_bridge():
            raise ValueError(f"edge {self._id} is not a bridge")
        self._current_resistance = self._max_resistance

    def is_available(self) -> bool:
        """Tell whether the edge can currently be used by searches.

        Receives: nothing.
        Returns:
            bool: True if the edge is enabled and, for bridges, not
            destroyed (availability depends on type and state).
        """
        return super().is_available() and not self.is_destroyed()
