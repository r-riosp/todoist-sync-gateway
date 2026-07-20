import logging

from app.core.config import config
from app.core.logging import setup_logging

setup_logging()

class TodoistService():
    def __init__(self, api_key: str):
        self.api_key = api_key

    def process_webhook(self, event_name: str, event_data: dict):
        logging.info(f"Processing webhook event: {event_name}")

        if not event_name or not event_data:
            logging.warning("Invalid webhook event received.")
            return

        task_id = event_data.get("id")
        task_content = event_data.get("content")
        project_id = event_data.get("project_id")

        logging.info(f"Webhook event processed and task created successfully!")
        logging.info(f"Task ID: {task_id}")
        logging.info(f"Task Content: {task_content}")
        logging.info(f"Project ID: {project_id}")