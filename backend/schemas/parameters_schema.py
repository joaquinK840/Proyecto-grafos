from pydantic import BaseModel, ConfigDict, Field


class ExecutionParametersInput(BaseModel):
    """Execution parameters of a scenario.

    The range constraints live here for now because no core entity owns
    these values yet; when towers, budget, etc. exist they should move to
    their own classes.

    Attributes:
        tower_limit: K, maximum number of towers (> 0).
        reference_time: D0, reference time for the tower score (> 0).
        danger_alpha: alpha, danger to time penalty coefficient (>= 0).
        height_beta: beta, tower height range factor (>= 0).
        bridge_rebuild_time: seconds to rebuild a bridge (>= 0).
        bridge_rebuild_people: people busy while rebuilding (> 0).
        initial_budget: starting budget (>= 0).
        time_limit: seconds until victory by resistance (> 0).
    """

    model_config = ConfigDict(extra="forbid")

    tower_limit: int = Field(default=3, gt=0)
    reference_time: float = Field(default=1, gt=0)
    danger_alpha: float = Field(default=0, ge=0)
    height_beta: float = Field(default=0, ge=0)
    bridge_rebuild_time: float = Field(default=10, ge=0)
    bridge_rebuild_people: int = Field(default=1, gt=0)
    initial_budget: int = Field(default=0, ge=0)
    time_limit: float = Field(default=300, gt=0)
