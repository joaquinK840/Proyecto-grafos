from enum import Enum


class GraphKind(str, Enum):
    """Catalog of the graphs that exist in a scenario.

    Values:
        GE: elevated graph (soldiers' paths and bridges).
        GM: maze graph (convoy corridors).

    It inherits from ``str`` so it can be used directly as a URL path value
    ("ge" / "gm").
    """

    GE = "ge"
    GM = "gm"
