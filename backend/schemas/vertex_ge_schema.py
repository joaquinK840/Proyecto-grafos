from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from ..core.vertice.position_type import PositionType
    from ..core.vertice.vertexGE import VertexGE
else:
    from core.vertice.position_type import PositionType
    from core.vertice.vertexGE import VertexGE


class VertexGEInput(BaseModel):
    """Shape of a GE vertex inside the scenario JSON.

    Only checks types; the domain rules (positive coordinates, non-empty
    id...) are enforced by ``VertexGE`` when the graph is built.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    x: float
    y: float
    position_type: PositionType


class VertexGEResponse(BaseModel):
    """API representation of a GE vertex."""

    id: str
    x: float
    y: float
    position_type: PositionType
    neighbors: list[str]

    @classmethod
    def from_entity(cls, vertex: VertexGE) -> "VertexGEResponse":
        """Build the response from a core vertex.

        Receives:
            vertex: VertexGE to represent.
        Returns:
            VertexGEResponse: serializable representation, with neighbors
            given by identifier.
        """
        return cls(
            id=vertex.get_id(),
            x=vertex.get_x(),
            y=vertex.get_y(),
            position_type=vertex.get_position_type(),
            neighbors=[neighbor.get_id() for neighbor in vertex.get_neighbors()],
        )
