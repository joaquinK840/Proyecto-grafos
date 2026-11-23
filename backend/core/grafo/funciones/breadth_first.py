if __package__.startswith("backend."):
    from ...queue.queue import queue
    from .get_available_neighbors import get_available_neighbors
else:
    from core.queue.queue import queue
    from core.grafo.funciones.get_available_neighbors import get_available_neighbors


def breadth_first(start_vertex) -> list:
    """Breadth-first traversal (BFS) from a vertex.

    Receives:
        start_vertex: vertex (already stored in the graph) to start from.
    Returns:
        list: vertices in the order they were visited.
    How it works:
        Uses the project queue. The start vertex is marked as visited and
        enqueued; then, while the queue is not empty, a vertex is dequeued,
        recorded, and every not-yet-visited neighbor through an AVAILABLE
        edge is marked and enqueued. Complexity O(V + E).
    """
    pending = queue()
    pending.enqueue(start_vertex)
    visited = {start_vertex.get_id()}
    result = []

    while not pending.is_empty():
        current = pending.dequeue()
        result.append(current)
        for _, neighbor in get_available_neighbors(current):
            if neighbor.get_id() not in visited:
                visited.add(neighbor.get_id())
                pending.enqueue(neighbor)
    return result
