from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PositionTypeSchema(str, Enum):
    BASE = "base"
    TOWER_CANDIDATE = "tower_candidate"
    TRANSIT = "transit"
    HELIPORT = "heliport"


class MazeVertexRoleSchema(str, Enum):
    NORMAL = "normal"
    ENTRY = "entry"
    EXIT = "exit"


class ConnectionTypeSchema(str, Enum):
    PATH = "path"
    BRIDGE = "bridge"


class GEVertexSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    x: float
    y: float
    position_type: PositionTypeSchema


class GEEdgeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    v1: str = Field(min_length=1)
    v2: str = Field(min_length=1)
    connection_type: ConnectionTypeSchema
    foot_time: Optional[float] = Field(default=None, gt=0)
    moto_time: Optional[float] = Field(default=None, gt=0)
    max_resistance: Optional[int] = Field(default=None, gt=0)
    current_resistance: Optional[int] = Field(default=None, gt=0)
    enabled: bool = True


class GMVertexSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    x: float
    y: float
    role: MazeVertexRoleSchema = MazeVertexRoleSchema.NORMAL


class GMEdgeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    v1: str = Field(min_length=1)
    v2: str = Field(min_length=1)
    length: float = Field(gt=0)
    speed: float = Field(gt=0)


class ElevatedGraphSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vertices: list[GEVertexSchema]
    edges: list[GEEdgeSchema]


class MazeGraphSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vertices: list[GMVertexSchema]
    edges: list[GMEdgeSchema]


class ExecutionParametersSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tower_limit: int = Field(default=3, gt=0)
    reference_time: float = Field(default=1, gt=0)
    danger_alpha: float = Field(default=0, ge=0)
    height_beta: float = Field(default=0, ge=0)
    bridge_rebuild_time: float = Field(default=10, ge=0)
    bridge_rebuild_people: int = Field(default=1, gt=0)
    initial_budget: int = Field(default=0, ge=0)
    time_limit: float = Field(default=300, gt=0)


class ConvoyUnitQuantitySchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tank: int = Field(default=0, ge=0)
    truck: int = Field(default=0, ge=0)
    robot: int = Field(default=0, ge=0)


class ScenarioPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    ge: ElevatedGraphSchema
    gm: MazeGraphSchema
    base_id: str = Field(min_length=1)
    entry_id: str = Field(min_length=1)
    exit_id: str = Field(min_length=1)
    parameters: ExecutionParametersSchema = ExecutionParametersSchema()
    convoy: ConvoyUnitQuantitySchema = ConvoyUnitQuantitySchema()


class ScenarioLoadResponse(BaseModel):
    name: str
    ge_vertex_count: int
    ge_edge_count: int
    gm_vertex_count: int
    gm_edge_count: int
    base_id: str
    entry_id: str
    exit_id: str
    shortest_maze_time: float
