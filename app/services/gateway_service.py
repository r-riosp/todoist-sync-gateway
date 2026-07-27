import logging

from app.database.sqlite_task_repository import TaskRepositoryInterface
from app.schemas.task import Task

class GatewayService:
    def __init__(self, repository: TaskRepositoryInterface) -> None:
        self._repository = repository

    def create_task(self, task: Task) -> Task:
        return self._repository.save(task)

