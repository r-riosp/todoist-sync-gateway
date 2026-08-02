import logging

from app.core.config import config
from app.core.logging import setup_logging
from app.models.enums import TaskStatus
from app.schemas.task import Task
from app.services.gateway_service import GatewayService

setup_logging()

class TodoistService():
    def __init__(self, api_key: str, gateway_service: GatewayService):
        self.api_key = api_key        
        self.gateway_service = gateway_service

    def process_webhook(self, event_name: str, event_data: dict):
        logging.debug(f"Processing webhook event: {event_name}")

        match event_name:
            case "item:added":
                content = event_data.get("content")
                description = event_data.get("description")
                status = TaskStatus.RUNNING
                task_id = event_data.get("id")
                td_project_id = event_data.get("project_id")
                labels = event_data.get("labels")

                task = Task(content=content, description=description, status="RUNNING", todoist_id=task_id, project_id=td_project_id)

                return self.create_task(task)
            case "item:completed":
                self.complete_task()
                pass
       
        logging.debug("Webhook event processed and task created successfully.")

    def create_task(self, task: Task):    
        logging.info(f"A new task in the game!")
        logging.info(f"""
                     Task: {task.content}
                     Description: {task.description}
                     Status: {task.status}
                     Id: {task.todoist_id}  
                     """        )    

        self.gateway_service.create_task(task)

    def complete_task(self):
        logging.info("Task concluded. Congrats!")
