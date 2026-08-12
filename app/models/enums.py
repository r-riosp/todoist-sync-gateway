from enum import Enum

class TaskStatus(str, Enum):
    """
    Represents the lifecycle status of a task.
    """
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"

class SyncStatus(str, Enum):
    """
    Represents the synchronization state with external platforms.
    """
    PENDING = "PENDING"
    SYNCED = "SYNCED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"