import logging

from fastapi import Depends
from app.core.config import config
from app.database.sqlite_task_repository import TaskRepositoryInterface
from app.schemas.anytype import ObjectPayload
from app.schemas.task import Task
from app.services.anytype_service import AnyTypeService

def get_anytype_service() -> AnyTypeService:
    return AnyTypeService(
        base_url=config.anytype_base_url,
        api_key=config.anytype_api_key
    )

class GatewayService:
    # A injeção de dependência é feita no construtor
    def __init__(
        self, 
        repository: TaskRepositoryInterface,
        # anytype_service: AnyTypeService = Depends(get_anytype_service)
    ) -> None:
        self._repository = repository
        self._anytype_service = get_anytype_service()

    def create_task(self, task: Task) -> Task:
        print(f"task: {task}")
        
        teste = Task(
            content=task.content, 
            description=task.description, 
            status=task.status, 
            todoist_id=task.todoist_id, 
            project_id=task.project_id
        )
        
        # O envio do objeto vai funcionar corretamente agora
        self.dispatch_task(teste)
        
        return self._repository.save(task)

    # Adicionado o parâmetro self. Removido o Depends().
    def dispatch_task(self, task: Task):
        print(f"task {task}")
        
        payload = ObjectPayload(
                body=task.description, 
                name=task.content, 
                type_key="task"
            )

        payload_dict = payload.model_dump()
        
        self._anytype_service.create_object(payload_dict)
        
        return ""
