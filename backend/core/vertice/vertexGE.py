from core.vertice.vertexMain import VertexMain
from core.vertice.position_type import PositionType
from core.validaciones.number_validator import validate_positive


class VertexGE(VertexMain):
    """Vertex of the elevated graph GE (a terrain position).

    Inherits identifier, coordinates and adjacency list from VertexMain and
    adds:
        - Strictly positive coordinates (GE rule: finite positive values).
        - The position type (base, tower candidate, transit or heliport).
    """

    def __init__(self, vertex_id: str, x: float, y: float, position_type: PositionType):
        """Create a GE vertex.

        Receives:
            vertex_id: unique, immutable identifier inside GE.
            x: horizontal coordinate (finite and > 0).
            y: vertical coordinate (finite and > 0).
            position_type: PositionType of the position.
        Returns:
            None.
        How it works:
            Delegates the common attributes to VertexMain (which calls the
            overridden ``_validate_coordinate``) and then validates and
            stores the position type.
        Raises:
            TypeError / ValueError: if any value breaks the GE rules.
        """
        super().__init__(vertex_id, x, y)
        self._position_type = self._validate_position_type(position_type)

    def _validate_coordinate(self, value, field_name: str) -> float:
        """Validate a coordinate with the GE rule.

        Receives:
            value: candidate coordinate.
            field_name: "x" or "y".
        Returns:
            float: the validated coordinate.
        How it works:
            GE requires finite and strictly positive coordinates, so it uses
            ``validate_positive`` instead of the base finite-only rule.
        """
        return validate_positive(value, field_name)

    @staticmethod
    def _validate_position_type(position_type) -> PositionType:
        """Validate the position type.

        Receives:
            position_type: candidate value.
        Returns:
            PositionType: the same value once validated.
        Raises:
            TypeError: if it is not a PositionType member.
        """
        if not isinstance(position_type, PositionType):
            raise TypeError("position_type must be a PositionType")
        return position_type

    def get_position_type(self) -> PositionType:
        """Return the position type.

        Receives: nothing.
        Returns:
            PositionType: type of this position.
        """
        return self._position_type

    def is_base(self) -> bool:
        """Tell whether this position is the base.

        Receives: nothing.
        Returns:
            bool: True if the position type is BASE.
        """
        return self._position_type is PositionType.BASE

    def is_tower_candidate(self) -> bool:
        """Tell whether a tower may be placed on this position.

        Receives: nothing.
        Returns:
            bool: True if the position type is TOWER_CANDIDATE.
        """
        return self._position_type is PositionType.TOWER_CANDIDATE

    def is_heliport(self) -> bool:
        """Tell whether this position is a heliport.

        Receives: nothing.
        Returns:
            bool: True if the position type is HELIPORT.
        """
        return self._position_type is PositionType.HELIPORT
