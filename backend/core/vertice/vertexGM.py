from core.vertice.vertexMain import VertexMain
from core.vertice.maze_vertex_role import MazeVertexRole


class VertexGM(VertexMain):
    """Vertex of the maze graph GM (a maze intersection).

    Inherits identifier, finite coordinates and adjacency list from
    VertexMain (GM only requires finite coordinates, so the base rule is
    kept) and adds the special role of the vertex: normal, entry or exit.
    """

    def __init__(self, vertex_id: str, x: float, y: float,
                 role: MazeVertexRole = MazeVertexRole.NORMAL):
        """Create a GM vertex.

        Receives:
            vertex_id: unique identifier inside GM.
            x: horizontal coordinate (finite).
            y: vertical coordinate (finite).
            role: MazeVertexRole of the vertex, NORMAL by default.
        Returns:
            None.
        How it works:
            Delegates the common attributes to VertexMain and then validates
            and stores the role.
        Raises:
            TypeError / ValueError: if any value breaks the GM rules.
        """
        super().__init__(vertex_id, x, y)
        self._role = self._validate_role(role)

    @staticmethod
    def _validate_role(role) -> MazeVertexRole:
        """Validate the vertex role.

        Receives:
            role: candidate value.
        Returns:
            MazeVertexRole: the same value once validated.
        Raises:
            TypeError: if it is not a MazeVertexRole member.
        """
        if not isinstance(role, MazeVertexRole):
            raise TypeError("role must be a MazeVertexRole")
        return role

    def get_role(self) -> MazeVertexRole:
        """Return the role of the vertex.

        Receives: nothing.
        Returns:
            MazeVertexRole: role of this vertex.
        """
        return self._role

    def is_entry(self) -> bool:
        """Tell whether this vertex is the maze entry.

        Receives: nothing.
        Returns:
            bool: True if the role is ENTRY.
        """
        return self._role is MazeVertexRole.ENTRY

    def is_exit(self) -> bool:
        """Tell whether this vertex is the maze exit.

        Receives: nothing.
        Returns:
            bool: True if the role is EXIT.
        """
        return self._role is MazeVertexRole.EXIT
