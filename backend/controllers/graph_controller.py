from typing import Union

from fastapi import APIRouter

if __package__.startswith("backend."):
    from ..domain.graph_kind import GraphKind
    from ..schemas.vertex_ge_schema import VertexGEResponse
    from ..schemas.vertex_gm_schema import VertexGMResponse
    from ..schemas.edge_ge_schema import EdgeGEResponse
    from ..schemas.edge_gm_schema import EdgeGMResponse
    from ..schemas.traversal_schema import TraversalResponse
    from ..service.graph.graph import graph_service
else:
    from domain.graph_kind import GraphKind
    from schemas.vertex_ge_schema import VertexGEResponse
    from schemas.vertex_gm_schema import VertexGMResponse
    from schemas.edge_ge_schema import EdgeGEResponse
    from schemas.edge_gm_schema import EdgeGMResponse
    from schemas.traversal_schema import TraversalResponse
    from service.graph.graph import graph_service


router = APIRouter(prefix="/api/graphs/{kind}", tags=["graphs"])

VertexResponse = Union[VertexGEResponse, VertexGMResponse]
EdgeResponse = Union[EdgeGEResponse, EdgeGMResponse]

# Response schema to use for each graph, so no isinstance checks are needed.
_VERTEX_RESPONSES = {GraphKind.GE: VertexGEResponse, GraphKind.GM: VertexGMResponse}
_EDGE_RESPONSES = {GraphKind.GE: EdgeGEResponse, GraphKind.GM: EdgeGMResponse}


@router.get("/vertices", response_model=list[VertexResponse])
def list_vertices(kind: GraphKind):
    """List the vertices of GE or GM.

    Receives:
        kind: "ge" or "gm" (URL path).
    Returns:
        list[VertexGEResponse | VertexGMResponse]: vertices of that graph.
    """
    to_response = _VERTEX_RESPONSES[kind].from_entity
    return [to_response(vertex) for vertex in graph_service.get_vertices(kind)]


@router.get("/edges", response_model=list[EdgeResponse])
def list_edges(kind: GraphKind):
    """List the edges of GE or GM.

    Receives:
        kind: "ge" or "gm" (URL path).
    Returns:
        list[EdgeGEResponse | EdgeGMResponse]: edges of that graph.
    """
    to_response = _EDGE_RESPONSES[kind].from_entity
    return [to_response(edge) for edge in graph_service.get_edges(kind)]


@router.get("/vertices/{vertex_id}", response_model=VertexResponse)
def get_vertex(kind: GraphKind, vertex_id: str):
    """Return one vertex of GE or GM.

    Receives:
        kind: "ge" or "gm" (URL path).
        vertex_id: identifier of the vertex (URL path).
    Returns:
        VertexGEResponse | VertexGMResponse: the vertex.
    """
    return _VERTEX_RESPONSES[kind].from_entity(graph_service.get_vertex(kind, vertex_id))


@router.get("/vertices/{vertex_id}/neighbors", response_model=list[str])
def list_neighbors(kind: GraphKind, vertex_id: str):
    """List the neighbor identifiers of a vertex.

    Receives:
        kind: "ge" or "gm" (URL path).
        vertex_id: identifier of the vertex (URL path).
    Returns:
        list[str]: identifiers of the neighbors.
    """
    return [neighbor.get_id() for neighbor in graph_service.get_neighbors(kind, vertex_id)]


@router.get("/traversals/breadth-first", response_model=TraversalResponse)
def breadth_first(kind: GraphKind, start: str):
    """Run BFS on GE or GM.

    Receives:
        kind: "ge" or "gm" (URL path).
        start: identifier of the start vertex (query string).
    Returns:
        TraversalResponse: identifiers in visit order.
    """
    visited = graph_service.breadth_first(kind, start)
    return TraversalResponse(vertices=[vertex.get_id() for vertex in visited])


@router.get("/traversals/depth-first", response_model=TraversalResponse)
def depth_first(kind: GraphKind, start: str):
    """Run DFS on GE or GM.

    Receives:
        kind: "ge" or "gm" (URL path).
        start: identifier of the start vertex (query string).
    Returns:
        TraversalResponse: identifiers in visit order.
    """
    visited = graph_service.depth_first(kind, start)
    return TraversalResponse(vertices=[vertex.get_id() for vertex in visited])
