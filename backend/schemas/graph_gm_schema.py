from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from .vertex_gm_schema import VertexGMInput
    from .edge_gm_schema import EdgeGMInput
else:
    from schemas.vertex_gm_schema import VertexGMInput
    from schemas.edge_gm_schema import EdgeGMInput


class GraphGMInput(BaseModel):
    """Shape of the maze graph GM inside the scenario JSON.

    Reuses the vertex and edge schemas of GM instead of redefining them.
    """

    model_config = ConfigDict(extra="forbid")

    vertices: list[VertexGMInput]
    edges: list[EdgeGMInput]
