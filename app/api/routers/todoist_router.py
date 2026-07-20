from fastapi import APIRouter, Depends

from app.core.config import config
from app.schemas.todoist import TodoistWebhookPayload
from app.services.todoist_service import TodoistService

router = APIRouter(prefix="/todoist", tags=["Todoist"])

def get_todoist_service() -> TodoistService:
    """
    Dependency function to provide an instance of TodoistService.
    This allows for easier testing and potential future enhancements.
    """
    return TodoistService(api_key=config.todoist_api_key)

@router.post("/webhook", summary="Receive Todoist Webhook Events and Task Data")
def receive_webhook(payload: TodoistWebhookPayload, service: TodoistService = Depends(get_todoist_service)):
    service.process_webhook(
        event_name=payload.event_name,
        event_data=payload.event_data
    )
    return {"status": "success", "message": "Webhook received and processed."}