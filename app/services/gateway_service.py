import httpx
from app.core.logging import setup_logging
from app.database.sqlite_task_repository import TaskRepositoryInterface
from app.schemas.anytype import ObjectPayload
from app.schemas.task import Task
from app.services.anytype_service import AnyTypeService
from app.services.linear_service import LinearService
from app.models.enums import SyncStatus

logger = setup_logging()

class GatewayService:
    """
    Orchestrates task synchronization between external platforms with isolated routing.
    """

    def __init__(
            self,
            repository: TaskRepositoryInterface,
            anytype_service: AnyTypeService,
            linear_service: LinearService
    ) -> None:
        """
        Initializes the GatewayService with injected dependencies.
        """
        self._repository = repository
        self._anytype_service = anytype_service
        self._linear_service = linear_service

    def create_task(self, task: Task) -> Task:
        """
        Evaluates task tags for routing and queues the task with appropriate sync statuses.
        If no explicit routing tags are found, defaults to SKIPPED for external platforms.
        """
        tags_lower = [tag.lower() for tag in task.tags] if task.tags else []

        # Routing intelligence based on Todoist tags
        anytype_status = SyncStatus.PENDING if "anytype" in tags_lower else SyncStatus.SKIPPED
        linear_status = SyncStatus.PENDING if "linear" in tags_lower else SyncStatus.SKIPPED

        clean_task = Task(
            content=task.content,
            description=task.description,
            status=task.status,
            todoist_id=task.todoist_id,
            project_id=task.project_id,
            anytype_sync_status=anytype_status,
            linear_sync_status=linear_status,
            tags=task.tags
        )

        saved_task = self._repository.save(clean_task)
        logger.info(
            "Task queued. ID: %s | AnyType: %s | Linear: %s",
            saved_task.id,
            saved_task.anytype_sync_status,
            saved_task.linear_sync_status
        )

        return saved_task

    def process_pending_tasks(self) -> None:
        """
        Iterates over pending tasks and attempts to dispatch them independently.
        Prevents a failure in one platform from blocking the synchronization of the other.
        """
        pending_tasks = self._repository.get_pending_tasks()

        if not pending_tasks:
            return

        for task in pending_tasks:
            has_updates = False

            # Independent AnyType Dispatch
            if task.anytype_sync_status == SyncStatus.PENDING:
                try:
                    self._dispatch_to_anytype(task)
                    task.anytype_sync_status = SyncStatus.SYNCED
                    has_updates = True
                    logger.info("Task %s successfully synchronized to AnyType.", task.id)
                except Exception as e:
                    logger.error("Failed to sync task %s to AnyType: %s", task.id, e)

            # Independent Linear Dispatch
            if task.linear_sync_status == SyncStatus.PENDING:
                try:
                    self._dispatch_to_linear(task)
                    task.linear_sync_status = SyncStatus.SYNCED
                    has_updates = True
                    logger.info("Task %s successfully synchronized to Linear.", task.id)
                except Exception as e:
                    logger.error("Failed to sync task %s to Linear: %s", task.id, e)

            # Only write to the database if a status actually changed
            if has_updates:
                self._repository.save(task)

    def _dispatch_to_anytype(self, task: Task) -> None:
        """
        Builds payload and executes AnyType creation request.
        """
        payload = ObjectPayload(
            body=task.description if task.description else "No description provided",
            name=task.content,
            type_key="task"
        )
        payload_dict = payload.model_dump()
        self._anytype_service.create_object(payload_dict)

    def _dispatch_to_linear(self, task: Task) -> None:
        """
        Triggers the GraphQL mutation for Linear issue creation.
        """
        self._linear_service.create_issue(task)