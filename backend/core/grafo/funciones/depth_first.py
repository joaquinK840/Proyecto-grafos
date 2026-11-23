if __package__.startswith("backend."):
    from ...stack.stack import stack
    from .get_available_neighbors import get_available_neighbors
else:
    from core.stack.stack import stack
    from core.grafo.funciones.get_available_neighbors import get_available_neighbors


def depth_first(start_vertex) -> list:
    """Depth-first traversal (DFS) from a vertex.

    Receives:
        start_vertex: vertex (already stored in the graph) to start from.
    Returns:
        list: vertices in the order they were visited.
    How it works:
        Iterative version with the project stack. A vertex is popped; if it
        was not visited it is recorded and its neighbors through AVAILABLE
        edges are pushed in reverse order, so they are explored in the same
        order the edges were added. Complexity O(V + E).
    """
    pending = stack()
    pending.push(start_vertex)
    visited = set()
    result = []

    while not pending.is_empty():
        current = pending.pop()
        if current.get_id() in visited:
            continue
        visited.add(current.get_id())
        result.append(current)
        neighbors = get_available_neighbors(current)
        for _, neighbor in reversed(neighbors):
            if neighbor.get_id() not in visited:
                pending.push(neighbor)
    return result
