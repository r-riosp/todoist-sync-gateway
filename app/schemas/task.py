from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.enums import TaskStatus, SyncStatus
from datetime import datetime

class Task(BaseModel):
    """
    Data transfer object representing a Task across the system.
    Tracks synchronization status individually for each target platform.
    """
    id: Optional[int] = None
    content: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.RUNNING

    # Independent synchronization tracking
    anytype_sync_status: SyncStatus = SyncStatus.PENDING
    linear_sync_status: SyncStatus = SyncStatus.PENDING

    tags: Optional[List[str]] = Field(default_factory=list)
    todoist_id: str
    anytype_id: Optional[str] = None
    linear_id: Optional[str] = None
    project_id: str
    created_at: datetime = Field(default_factory=datetime.now)