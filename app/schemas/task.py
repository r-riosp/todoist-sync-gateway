from pydantic import BaseModel, Field
from typing import Optional
from app.models.enums import TaskStatus
from datetime import datetime


class Task(BaseModel):
    id: Optional[str] = None
    content: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.RUNNING
    tags: Optional[list] = None

    todoist_id: str
    anytype_id: Optional[str] = None
    linear_id: Optional[str] = None

    project_id: str
    # todoist_project_id: str
    # anytype_project_id:Optional[str]
    # linear_project_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now);
