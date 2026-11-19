from enum import Enum

#catalogo de que posicion cumple cada nodo
class PositionType(Enum):
    """Kind of terrain position a GE vertex represents.

    Values:
        BASE: command base (exactly one per scenario, checked by the graph).
        TOWER_CANDIDATE: position where a tower may be placed.
        TRANSIT: plain transit position.
        HELIPORT: position where helicopters can land.
    """

    BASE = "base"
    TOWER_CANDIDATE = "tower_candidate"
    TRANSIT = "transit"
    HELIPORT = "heliport"
