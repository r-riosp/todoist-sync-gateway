from fastapi import FastAPI
import logging

from app.core.config import config
from app.core.logging import setup_logging

from app.api.routers import anytype_router, todoist_router
import app.database.connection as conn
# from app.api.routers import todoist_router
# from app.api.routers import linear_router

setup_logging()

app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
    debug=config.debug
)

app.include_router(
    #anytype_router.router,
    todoist_router.router
    )

@app.get("/", tags=["Health Check"])
def health_check():
    logging.info("Health check endpoint pinged.")
    conn.get_db_connection()
    return {"status": "ok", "message": "Gateway is running smoothly."}
