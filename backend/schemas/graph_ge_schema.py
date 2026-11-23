from pydantic import BaseModel, ConfigDict

if __package__.startswith("backend."):
    from .vertex_ge_schema import VertexGEInput
    from .edge_ge_schema import EdgeGEInput
else:
    from schemas.vertex_ge_schema import VertexGEInput
    from schemas.edge_ge_schema import EdgeGEInput


class GraphGEInput(BaseModel):
    """Shape of the elevated graph GE inside the scenario JSON.

    Reuses the vertex and edge schemas of GE instead of redefining them.
    """

    model_config = ConfigDict(extra="forbid")

    vertices: list[VertexGEInput]
    edges: list[EdgeGEInput]
