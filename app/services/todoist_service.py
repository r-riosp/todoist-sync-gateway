from app.core.logging import setup_logging
from app.models.enums import TaskStatus
from app.schemas.task import Task
from app.services.gateway_service import GatewayService

logger = setup_logging()


def complete_task():
    logger.info("Task concluded. Congrats!")


class TodoistService:
    def __init__(self, api_key: str, gateway_service: GatewayService):
        self.api_key = api_key
        self.gateway_service = gateway_service

    def process_webhook(self, event_name: str, event_data: dict):
        match event_name:
            case "item:added":
                content = event_data.get("content")
                description = event_data.get("description")
                status = TaskStatus.RUNNING
                task_id = event_data.get("id")
                td_project_id = event_data.get("project_id")
                labels = event_data.get("labels")

                task = Task(content=content, description=description, status=status, todoist_id=task_id, project_id=td_project_id, tags=labels)

                self.create_task(task)
            case "item:completed":
                complete_task()
                pass

        logger.info("Webhook event processed. Event: %s", event_name)
        return None

    def create_task(self, task: Task):
        logger.info(f"""
             Task created!
             Task: {task.content}
             Description: {task.description}
             Status: {task.status}
             Id: {task.todoist_id}
             Tags: {task.tags}
         """)

        self.gateway_service.create_task(task)
