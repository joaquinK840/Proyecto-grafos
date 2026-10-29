from pydantic import BaseModel


class VertexCreate(BaseModel):
    name: int


class VertexResponse(BaseModel):
    name: int
    available: bool
    neighbors: list[int]


class EdgeCreate(BaseModel):
    source: int
    target: int
    weight: int


class EdgeResponse(BaseModel):
    source: int
    target: int
    weight: int


class TraversalResponse(BaseModel):
    vertices: list[int]
