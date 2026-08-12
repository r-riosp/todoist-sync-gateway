import sqlite3
from typing import Callable, List
from app.core.logging import setup_logging
from app.repositories.task_repository import TaskRepositoryInterface
from app.schemas.task import Task
from app.models.enums import SyncStatus

logger = setup_logging()

class SQLiteTaskRepository(TaskRepositoryInterface):
    """
    Implementation of the TaskRepositoryInterface for SQLite.
    Handles all database interactions for the Task entity, including granular sync tracking.
    """

    def __init__(self, connection_factory: Callable[[], sqlite3.Connection]) -> None:
        """
        Initializes the repository with a database connection factory.
        """
        self._connection_factory = connection_factory

    def initialize_database(self) -> None:
        """
        Creates the necessary database tables if they do not exist.
        Should be called only once during application startup.
        """
        query = """
                CREATE TABLE IF NOT EXISTS tasks (
                                                     id INTEGER PRIMARY KEY,
                                                     content text NOT NULL,
                                                     description text,
                                                     status text CHECK(status IN ('RUNNING', 'COMPLETED', 'DELETED', 'UPDATED')) NOT NULL DEFAULT 'RUNNING',
                    anytype_sync_status text CHECK(anytype_sync_status IN ('PENDING', 'SYNCED', 'FAILED', 'SKIPPED')) NOT NULL DEFAULT 'PENDING',
                    linear_sync_status text CHECK(linear_sync_status IN ('PENDING', 'SYNCED', 'FAILED', 'SKIPPED')) NOT NULL DEFAULT 'PENDING',
                    created_at DATE,
                    todoist_id text NOT NULL,
                    anytype_id text,
                    linear_id text,
                    project_id text
                    ); \
                """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.execute("SELECT name FROM sqlite_master")
            logger.info("Database initialized. Existing tables: %s", cursor.fetchall())

    def save(self, task: Task) -> Task:
        """
        Persists a Task. Inserts if it lacks an ID, otherwise updates.
        """
        if task.id is None:
            return self._insert(task)
        return self._update(task)

    def _insert(self, task: Task) -> Task:
        """
        Executes the INSERT query for a new Task.
        """
        query = """
                INSERT INTO tasks (content, description, status, anytype_sync_status, linear_sync_status, created_at, todoist_id, project_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?); \
                """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (
                    task.content,
                    task.description,
                    task.status,
                    task.anytype_sync_status.value,
                    task.linear_sync_status.value,
                    task.created_at,
                    task.todoist_id,
                    task.project_id
                ),
            )
            conn.commit()
            task.id = cursor.lastrowid
            return task

    def _update(self, task: Task) -> Task:
        """
        Executes the UPDATE query for an existing Task.
        Updates both sync statuses for background workers.
        """
        query = """
                UPDATE tasks
                SET anytype_sync_status = ?, linear_sync_status = ?
                WHERE id = ?; \
                """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (task.anytype_sync_status.value, task.linear_sync_status.value, task.id))
            conn.commit()
        return task

    def get_pending_tasks(self) -> List[Task]:
        """
        Retrieves all tasks that are waiting to be synchronized in at least one platform.
        """
        query = """
                SELECT id, content, description, status, anytype_sync_status, linear_sync_status, created_at, todoist_id, project_id
                FROM tasks
                WHERE anytype_sync_status = 'PENDING' OR linear_sync_status = 'PENDING'; \
                """
        tasks = []
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                task = Task(
                    id=row[0],
                    content=row[1],
                    description=row[2],
                    status=row[3],
                    anytype_sync_status=row[4],
                    linear_sync_status=row[5],
                    created_at=row[6],
                    todoist_id=row[7],
                    project_id=row[8]
                )
                tasks.append(task)
        return tasks