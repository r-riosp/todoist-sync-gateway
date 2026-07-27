import sqlite3
import logging

from app.repositories.task_repository import TaskRepositoryInterface
from app.schemas.task import Task

class SQLiteTaskRepository(TaskRepositoryInterface):
    def __init__(self, connection_factory: Callable[[], sqlite3.Connection]) -> None:
        self._connection_factory = connection_factory
        self._create_table()

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY,
              content text NOT NULL,
              description text,
              status text CHECK(status IN ('RUNNING', 'COMPLETED', 'DELETED', 'UPDATED')) NOT NULL DEFAULT 'RUNNING',
              created_at DATE,
              todoist_id text NOT NULL,
              anytype_id text,
              linear_id text,
              project_id
        );
        """

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            result = cursor.execute("SELECT name FROM sqlite_master")
            logging.info(f"Table: {result.fetchone()}")

    def save(self, task: Task) -> Task:
            if task.id is None:
                return self._insert(task)
            return self._update(task)

    def _insert(self, task: Task) -> Task:
        query = """
        INSERT INTO tasks (content, description, status, created_at, todoist_id, project_id)
        VALUES (?, ?, ?, ?, ?, ?);
        """

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (
                    task.content,
                    task.description,
                    task.status,
                    task.created_at,
                    task.todoist_id,  
                    task.project_id
                ),
            )      
            conn.commit()
            task.id = cursor.lastrowid
            return task
