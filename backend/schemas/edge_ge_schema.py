from typing import Optional

from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from ..core.arista.connection_type import ConnectionType
    from ..core.arista.edgeGE import EdgeGE
else:
    from core.arista.connection_type import ConnectionType
    from core.arista.edgeGE import EdgeGE


class EdgeGEInput(BaseModel):
    """Shape of a GE edge inside the scenario JSON.

    ``v1`` / ``v2`` are vertex identifiers. Only checks types; positive
    times, bridge resistances and "at least one transport mode" are
    enforced by ``EdgeGE`` when the graph is built.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    v1: str
    v2: str
    connection_type: ConnectionType
    foot_time: Optional[float] = None
    moto_time: Optional[float] = None
    max_resistance: Optional[int] = None
    current_resistance: Optional[int] = None
    enabled: bool = True


class EdgeGEResponse(BaseModel):
    """API representation of a GE edge."""

    id: str
    v1: str
    v2: str
    connection_type: ConnectionType
    foot_time: Optional[float]
    moto_time: Optional[float]
    max_resistance: Optional[int]
    current_resistance: Optional[int]
    enabled: bool
    available: bool

    @classmethod
    def from_entity(cls, edge: EdgeGE) -> "EdgeGEResponse":
        """Build the response from a core edge.

        Receives:
            edge: EdgeGE to represent.
        Returns:
            EdgeGEResponse: serializable representation, with endpoints
            given by identifier and the computed availability.
        """
        return cls(
            id=edge.get_id(),
            v1=edge.get_v1().get_id(),
            v2=edge.get_v2().get_id(),
            connection_type=edge.get_connection_type(),
            foot_time=edge.get_foot_time(),
            moto_time=edge.get_moto_time(),
            max_resistance=edge.get_max_resistance(),
            current_resistance=edge.get_current_resistance(),
            enabled=edge.is_enabled(),
            available=edge.is_available(),
        )
