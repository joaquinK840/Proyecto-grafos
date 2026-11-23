from pydantic import BaseModel


class TraversalResponse(BaseModel):
    """Result of a graph traversal (BFS or DFS).

    Attributes:
        vertices: identifiers of the visited vertices, in visit order.
    """

    vertices: list[str]
