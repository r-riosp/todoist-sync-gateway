from abc import ABC, abstractmethod
from typing import List
from app.schemas.task import Task

class TaskRepositoryInterface(ABC):
    """
    Contract for Task data persistence.
    All concrete repositories (SQLite, Postgres, etc.) must implement these methods.
    """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Persists a Task object in repository.
        Updates if it has an id, creates if not.
        """
        pass

    @abstractmethod
    def get_pending_tasks(self) -> List[Task]:
        """
        Retrieves all tasks that are waiting to be synchronized in at least one platform.
        """
        pass