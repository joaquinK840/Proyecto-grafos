from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

if __package__.startswith("backend."):
    from ..core.grafo.graph_errors import VertexNotFoundError
    from ..domain.scenario_errors import ScenarioNotLoadedError, ScenarioValidationError
else:
    from core.grafo.graph_errors import VertexNotFoundError
    from domain.scenario_errors import ScenarioNotLoadedError, ScenarioValidationError


# Domain exception -> HTTP status code. Adding a new error only needs a row.
_STATUS_BY_ERROR = {
    VertexNotFoundError: status.HTTP_404_NOT_FOUND,
    ScenarioValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ScenarioNotLoadedError: status.HTTP_409_CONFLICT,
}


def _build_handler(status_code: int):
    """Create an exception handler that answers with a fixed status code.

    Receives:
        status_code: HTTP status to return.
    Returns:
        Callable: async FastAPI handler that responds {"detail": message}.
    """

    async def handler(request: Request, exception: Exception) -> JSONResponse:
        """Turn a domain exception into a JSON HTTP response.

        Receives:
            request: current request (unused).
            exception: the raised domain exception.
        Returns:
            JSONResponse: {"detail": str(exception)} with ``status_code``.
        """
        return JSONResponse(status_code=status_code, content={"detail": str(exception)})

    return handler


def register_exception_handlers(app: FastAPI) -> None:
    """Register every domain exception handler in the app.

    Receives:
        app: FastAPI application.
    Returns:
        None.
    """
    for error_type, status_code in _STATUS_BY_ERROR.items():
        app.add_exception_handler(error_type, _build_handler(status_code))
