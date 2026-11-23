from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from ..core.vertice.maze_vertex_role import MazeVertexRole
    from ..core.vertice.vertexGM import VertexGM
else:
    from core.vertice.maze_vertex_role import MazeVertexRole
    from core.vertice.vertexGM import VertexGM


class VertexGMInput(BaseModel):
    """Shape of a GM vertex inside the scenario JSON.

    Only checks types; the domain rules are enforced by ``VertexGM``.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    x: float
    y: float
    role: MazeVertexRole = MazeVertexRole.NORMAL


class VertexGMResponse(BaseModel):
    """API representation of a GM vertex."""

    id: str
    x: float
    y: float
    role: MazeVertexRole
    neighbors: list[str]

    @classmethod
    def from_entity(cls, vertex: VertexGM) -> "VertexGMResponse":
        """Build the response from a core vertex.

        Receives:
            vertex: VertexGM to represent.
        Returns:
            VertexGMResponse: serializable representation, with neighbors
            given by identifier.
        """
        return cls(
            id=vertex.get_id(),
            x=vertex.get_x(),
            y=vertex.get_y(),
            role=vertex.get_role(),
            neighbors=[neighbor.get_id() for neighbor in vertex.get_neighbors()],
        )
