from enum import Enum

#catalogo de que rol cumple el nodo
class MazeVertexRole(Enum):
    """Role a GM vertex plays inside the maze.

    Values:
        NORMAL: ordinary intersection.
        ENTRY: maze entry, where the convoy starts.
        EXIT: maze exit, the convoy goal.

    The rule "entry and exit must be different vertices" is enforced by the
    maze graph, since a single vertex can only hold one role.
    """

    NORMAL = "normal"
    ENTRY = "entry"
    EXIT = "exit"
