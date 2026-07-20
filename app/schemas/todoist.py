from pydantic import BaseModel
from typing import Any, Dict

class TodoistWebhookPayload(BaseModel):
    event_name: str
    event_data: Dict[str, Any]