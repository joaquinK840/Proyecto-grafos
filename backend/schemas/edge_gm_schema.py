from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from ..core.arista.edgeGM import EdgeGM
else:
    from core.arista.edgeGM import EdgeGM


class EdgeGMInput(BaseModel):
    """Shape of a GM corridor inside the scenario JSON.

    ``v1`` / ``v2`` are vertex identifiers. Only checks types; positive
    length and speed are enforced by ``EdgeGM`` when the graph is built.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    v1: str
    v2: str
    length: float
    speed: float


class EdgeGMResponse(BaseModel):
    """API representation of a GM corridor."""

    id: str
    v1: str
    v2: str
    length: float
    speed: float
    travel_time: float
    enabled: bool
    available: bool

    @classmethod
    def from_entity(cls, edge: EdgeGM) -> "EdgeGMResponse":
        """Build the response from a core edge.

        Receives:
            edge: EdgeGM to represent.
        Returns:
            EdgeGMResponse: serializable representation, including the
            travel time t(e) = l(e) / v(e).
        """
        return cls(
            id=edge.get_id(),
            v1=edge.get_v1().get_id(),
            v2=edge.get_v2().get_id(),
            length=edge.get_length(),
            speed=edge.get_speed(),
            travel_time=edge.get_travel_time(),
            enabled=edge.is_enabled(),
            available=edge.is_available(),
        )
