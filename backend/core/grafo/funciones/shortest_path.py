from typing import Callable, Optional

if __package__.startswith("backend."):
    from ...heap.min_heap import MinHeap
    from ..path_result import PathResult
    from .get_available_neighbors import get_available_neighbors
else:
    from core.heap.min_heap import MinHeap
    from core.grafo.path_result import PathResult
    from core.grafo.funciones.get_available_neighbors import get_available_neighbors


def shortest_path(origin, destination, weight: Callable) -> Optional[PathResult]:
    """Find the minimum cost path between two vertices (Dijkstra).

    Receives:
        origin: start vertex (stored in the graph).
        destination: target vertex (stored in the graph).
        weight: function edge -> non-negative number giving the cost of
            crossing that edge. Passing the function keeps the algorithm
            reusable: t(e) = l/v in GM, w(e) = t(e) + alpha * P(e) later,
            or the foot/motorcycle time in GE.
    Returns:
        Optional[PathResult]: the path and its cost, or None if the
        destination cannot be reached through available edges.
    How it works:
        Classic Dijkstra with the project MinHeap as priority queue and lazy
        deletion: every improvement pushes a new entry and outdated entries
        are skipped when popped. ``previous`` stores, for every reached
        vertex, the (edge, vertex) it was reached from, and is used at the
        end to rebuild the path backwards. Only available edges are used.
        Complexity O((V + E) log V).
    Raises:
        ValueError: if the weight function returns a negative value.
    """
    best = {origin.get_id(): 0.0}
    previous = {}
    pending = MinHeap()
    pending.push(0.0, origin)

    while not pending.is_empty():
        current_cost, current = pending.pop()
        if current_cost > best[current.get_id()]:
            continue
        if current is destination:
            return _build_path(origin, destination, previous, current_cost)
        for edge, neighbor in get_available_neighbors(current):
            edge_cost = weight(edge)
            if edge_cost < 0:
                raise ValueError(f"edge {edge.get_id()} has a negative cost")
            next_cost = current_cost + edge_cost
            if next_cost < best.get(neighbor.get_id(), float("inf")):
                best[neighbor.get_id()] = next_cost
                previous[neighbor.get_id()] = (edge, current)
                pending.push(next_cost, neighbor)
    return None


def _build_path(origin, destination, previous: dict, cost: float) -> PathResult:
    """Rebuild the path found by Dijkstra.

    Receives:
        origin: start vertex.
        destination: target vertex.
        previous: {vertex_id: (edge, previous_vertex)} filled by Dijkstra.
        cost: total cost of the path.
    Returns:
        PathResult: vertices and edges in order from origin to destination.
    How it works:
        Walks ``previous`` from the destination back to the origin and then
        reverses both lists.
    """
    vertices = [destination]
    edges = []
    current = destination
    while current is not origin:
        edge, current = previous[current.get_id()]
        edges.append(edge)
        vertices.append(current)
    vertices.reverse()
    edges.reverse()
    return PathResult(vertices=vertices, edges=edges, cost=cost)
