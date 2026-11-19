from enum import Enum


class ConnectionType(Enum):
    """Kind of connection a GE edge represents.

    Values:
        PATH: regular path, it never wears out.
        BRIDGE: bridge with max/current resistance that can collapse
            and be rebuilt.
    """

    PATH = "path"
    BRIDGE = "bridge"
