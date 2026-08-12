from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.database.connection import get_db_connection
from app.core.config import config
from app.schemas.task import Task
from app.schemas.todoist import TodoistWebhookPayload
from app.services.todoist_service import TodoistService
from app.database.sqlite_task_repository import SQLiteTaskRepository
from app.services.gateway_service import GatewayService
from app.services.anytype_service import AnyTypeService
from app.services.linear_service import LinearService

router = APIRouter(prefix="/todoist", tags=["Todoist"])

def get_todoist_service() -> TodoistService:
    """
    Dependency function to provide an instance of TodoistService.
    Properly chains the required dependencies for the GatewayService,
    including the new Linear integration.
    """
    repository = SQLiteTaskRepository(connection_factory=get_db_connection)

    anytype_service = AnyTypeService(
        base_url=config.anytype_base_url,
        api_key=config.anytype_api_key
    )

    linear_service = LinearService(
        api_key=config.linear_api_key,
        team_id=config.linear_team_id
    )

    gateway_service = GatewayService(
        repository=repository,
        anytype_service=anytype_service,
        linear_service=linear_service
    )

    return TodoistService(api_key=config.todoist_api_key, gateway_service=gateway_service)

@router.post("/webhook", summary="Receive Todoist Webhook Events and Task Data")
def receive_webhook(payload: TodoistWebhookPayload, service: TodoistService = Depends(get_todoist_service)):
    """
    Endpoint for receiving and processing Todoist webhooks.
    """
    service.process_webhook(
        event_name=payload.event_name,
        event_data=payload.event_data
    )
    return {"status": "success", "message": "Webhook received and processed."}