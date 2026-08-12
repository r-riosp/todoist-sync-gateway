import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import config
from app.core.logging import setup_logging
from app.api.routers import anytype_router, todoist_router
import app.database.connection as conn
from app.database.sqlite_task_repository import SQLiteTaskRepository
from app.services.gateway_service import GatewayService
from app.services.anytype_service import AnyTypeService
from app.services.linear_service import LinearService

logger = setup_logging()

async def background_sync_task(gateway_service: GatewayService):
    """
    Background worker that periodically tries to sync pending tasks.
    """
    while True:
        try:
            gateway_service.process_pending_tasks()
        except Exception as e:
            logger.error("Error in background sync loop: %s", e)
        await asyncio.sleep(10)  # Polling interval set to 10 seconds

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles database initialization and spins up the background worker.
    """
    logger.info("Starting up application...")

    # Manually wiring dependencies for the background task
    db_conn = conn.get_db_connection()
    repo = SQLiteTaskRepository(lambda: db_conn)
    repo.initialize_database()

    anytype_service = AnyTypeService(
        base_url=config.anytype_base_url,
        api_key=config.anytype_api_key
    )

    linear_service = LinearService(
        api_key=config.linear_api_key,
        team_id=config.linear_team_id
    )

    # Fixed: Passing all required dependencies to the GatewayService
    gateway_service = GatewayService(
        repository=repo,
        anytype_service=anytype_service,
        linear_service=linear_service
    )

    # Fire and forget the background polling task
    sync_task = asyncio.create_task(background_sync_task(gateway_service))

    yield

    logger.info("Shutting down application...")
    sync_task.cancel()
    db_conn.close()

app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
    debug=config.debug,
    lifespan=lifespan
)

app.include_router(todoist_router.router)
# app.include_router(anytype_router.router)

@app.get("/", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify API status.
    """
    logger.info("Health check endpoint pinged.")
    return {"status": "ok", "message": "Gateway is running smoothly."}