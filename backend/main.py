from fastapi import FastAPI

if __package__:
    from .controllers.error_handler import register_exception_handlers
    from .controllers.graph_controller import router
    from .controllers.scenario_controller import router as scenario_router
else:
    from controllers.error_handler import register_exception_handlers
    from controllers.graph_controller import router
    from controllers.scenario_controller import router as scenario_router


app = FastAPI(
    title="API de grafos",
    description="API en memoria para administrar grafos dirigidos.",
    version="1.0.0",
)

register_exception_handlers(app)
app.include_router(router)
app.include_router(scenario_router)
