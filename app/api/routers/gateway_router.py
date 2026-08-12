from fastapi import APIRouter, Depends, Body

from app.schemas.task import Task
from app.services.gateway_service import GatewayService
from app.database.sqlite_task_repository import SQLiteTaskRepository
from app.database.connection import get_db_connection

router = APIRouter(tags=["Gateway"]) 

def get_gateway_service() -> GatewayService:
    repository = SQLiteTaskRepository(connection_factory=get_db_connection)
    return GatewayService(repository=repository)

@router.post("/task")
def create_task(payload: Task = Body(...), service: GatewayService = Depends(get_gateway_service)) -> Task:
    return service.create_task(payload)
