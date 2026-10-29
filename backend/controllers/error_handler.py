from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

if __package__.startswith("backend."):
    from ..core.grafo.graph import DuplicateVertexError, VertexNotFoundError
else:
    from core.grafo.graph import DuplicateVertexError, VertexNotFoundError


async def duplicate_vertex_handler(
    request: Request,
    exception: DuplicateVertexError,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exception)},
    )


async def vertex_not_found_handler(
    request: Request,
    exception: VertexNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exception)},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateVertexError, duplicate_vertex_handler)
    app.add_exception_handler(VertexNotFoundError, vertex_not_found_handler)
