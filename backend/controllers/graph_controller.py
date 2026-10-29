from fastapi import APIRouter, status

if __package__.startswith("backend."):
    from ..schemas.graph_schemas import (
        EdgeCreate,
        EdgeResponse,
        TraversalResponse,
        VertexCreate,
        VertexResponse,
    )
    from ..service.graph import graph_service
else:
    from schemas.graph_schemas import (
        EdgeCreate,
        EdgeResponse,
        TraversalResponse,
        VertexCreate,
        VertexResponse,
    )
    from service.graph import graph_service


router = APIRouter(prefix="/api")


def _vertex_response(vertex) -> VertexResponse:
    return VertexResponse(
        name=vertex.get_name(),
        available=vertex.get_available(),
        neighbors=[edge.get_v2().get_name() for edge in vertex.get_neighbors()],
    )


@router.post(
    "/vertices",
    response_model=VertexResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vertex(payload: VertexCreate):
    return _vertex_response(graph_service.add_vertex(payload.name))


@router.get("/vertices", response_model=list[VertexResponse])
def list_vertices():
    return [_vertex_response(vertex) for vertex in graph_service.get_vertices()]


@router.get("/edges", response_model=list[EdgeResponse])
def list_edges():
    return [
        EdgeResponse(
            source=edge.get_v1().get_name(),
            target=edge.get_v2().get_name(),
            weight=edge.get_weight(),
        )
        for edge in graph_service.get_edges()
    ]


@router.get("/vertices/{vertex_id}", response_model=VertexResponse)
def get_vertex(vertex_id: int):
    return _vertex_response(graph_service.get_vertex(vertex_id))


@router.post(
    "/edges",
    response_model=EdgeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_edge(payload: EdgeCreate):
    graph_edge = graph_service.add_edge(
        payload.source,
        payload.target,
        payload.weight,
    )
    return EdgeResponse(
        source=graph_edge.get_v1().get_name(),
        target=graph_edge.get_v2().get_name(),
        weight=graph_edge.get_weight(),
    )


@router.get(
    "/vertices/{vertex_id}/neighbors",
    response_model=list[int],
)
def list_neighbors(vertex_id: int):
    return [
        neighbor.get_name()
        for neighbor in graph_service.get_neighbors(vertex_id)
    ]


@router.get(
    "/traversals/breadth-first",
    response_model=TraversalResponse,
)
def breadth_first(start: int):
    return TraversalResponse(
        vertices=[
            vertex.get_name()
            for vertex in graph_service.breadth_first(start)
        ]
    )


@router.get(
    "/traversals/depth-first",
    response_model=TraversalResponse,
)
def depth_first(start: int):
    return TraversalResponse(
        vertices=[
            vertex.get_name()
            for vertex in graph_service.depth_first(start)
        ]
    )
