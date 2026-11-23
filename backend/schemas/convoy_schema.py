from pydantic import BaseModel, ConfigDict, Field


class ConvoyInput(BaseModel):
    """Composition of the enemy convoy in the scenario JSON.

    Attributes:
        tank: number of tanks (>= 0).
        truck: number of trucks (>= 0).
        robot: number of robot soldiers (>= 0).
    """

    model_config = ConfigDict(extra="forbid")

    tank: int = Field(default=0, ge=0)
    truck: int = Field(default=0, ge=0)
    robot: int = Field(default=0, ge=0)
