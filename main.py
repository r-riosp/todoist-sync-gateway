from fastapi import FastAPI
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from os import getenv
import httpx

app = FastAPI(
        title="Integrador Todoist Linear e AnyType",
        description="Gateway que sincroniza tarefas e projetos entre os três apps: Todoist, Linear e AnyType",
        version="0.1.0"
        )

load_dotenv()

# api_key = os.getenv("API_KEY")
todoist_api_key = getenv("TEST_TOKEN")
anytype_api_key = getenv("ANYTYPE_API_KEY")

anytype_base_url = getenv("ANYTYPE_BASE_URL")

api = TodoistAPI(todoist_api_key)

class Task(BaseModel):
    id: str
    content: str
    project_id: Optional[str]
    section_id: Optional[str]
    description: str

@app.get("/tasks/{task_id}")
def show_task(task_id: str | None = None):
    response = api.get_task(task_id)
    task = Task(id=response.id, content=response.content, project_id=response.project_id, section_id=response.section_id, description=response.description)
    print(f"Task: {task.content}")
    print(f"Conteúdo: {task.description}")
    print(f"ID da Task: {task.id}")

@app.webhooks.post("item-added")
def receive_task_added(body: Task):
    print(body.content)
    return "Tarefa nova na área!"

@app.post("/webhook-todoist")
def receive_task_news():
    print("DEU BOM")

headers = {"Authorization": f"Bearer {anytype_api_key}"}

@app.get("/anytype/spaces")
def show_spaces():
    response = httpx.get(f"{anytype_base_url}/spaces", headers=headers)   
    print(response.status_code)
    return response.json()

@app.get("/anytype/spaces/{space_id}/objects/{object_id}")
def show_objects(space_id: str, object_id: str | None = None):
    response = httpx.get(f"{anytype_base_url}/spaces/{space_id}/objects/{object_id}", headers=headers)
    print(response.status_code)
    return response.json()
