from enum import Enum

class TaskStatus(str, Enum):
    RUNNING = "RUNNING",
    COMPLETED = "COMPLETED",
    UPDATED = "UPDATED",
    DELETED = "DELETED"
