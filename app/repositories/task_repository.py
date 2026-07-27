from abc import ABC, abstractmethod
from typing import Optional, List
from app.schemas.task import Task 

class TaskRepositoryInterface(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Persists a Task object in repository.

        Updates if it has an id, creates if not.
        """
        pass

   # @abstractmethod
    #def find_by_id(self, task_id: str) -> Optional[Task]:
    #    """
     #   Searches for a task with the specified id.
      #  """
       # pass
    #@abstractmethod
    #@def find_all(self) -> List[Task]:
    #    """
    #    Returns all tasks presented in the repository.
    #    """
    #    pass 

