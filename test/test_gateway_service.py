import pytest
from unittest.mock import MagicMock
from app.schemas.task import Task
from app.models.enums import TaskStatus, SyncStatus
from app.services.gateway_service import GatewayService
from app.services.anytype_service import AnyTypeService
from app.services.linear_service import LinearService
from app.database.sqlite_task_repository import TaskRepositoryInterface

@pytest.fixture
def mock_repository() -> MagicMock:
    """
    Provides a mocked instance of TaskRepositoryInterface.
    Prevents actual database I/O operations.
    """
    return MagicMock(spec=TaskRepositoryInterface)

@pytest.fixture
def mock_anytype_service() -> MagicMock:
    """
    Provides a mocked instance of AnyTypeService.
    """
    return MagicMock(spec=AnyTypeService)

@pytest.fixture
def mock_linear_service() -> MagicMock:
    """
    Provides a mocked instance of LinearService.
    """
    return MagicMock(spec=LinearService)

@pytest.fixture
def gateway_service(
        mock_repository: MagicMock,
        mock_anytype_service: MagicMock,
        mock_linear_service: MagicMock
) -> GatewayService:
    """
    Instantiates the GatewayService with all dependencies mocked.
    """
    return GatewayService(
        repository=mock_repository,
        anytype_service=mock_anytype_service,
        linear_service=mock_linear_service
    )

def test_create_task_routing_linear_only(
        gateway_service: GatewayService,
        mock_repository: MagicMock
) -> None:
    """
    Verifies that a task with the 'linear' tag is queued for Linear only,
    and SKIPPED for AnyType.
    """
    # Arrange
    input_task = Task(
        content="Test Task Linear",
        tags=["linear", "work"],
        status=TaskStatus.RUNNING,
        todoist_id="td_1",
        project_id="proj_1"
    )

    # Mock repository to just return the saved task back
    mock_repository.save.side_effect = lambda task: task

    # Act
    result_task = gateway_service.create_task(input_task)

    # Assert
    assert result_task.linear_sync_status == SyncStatus.PENDING
    assert result_task.anytype_sync_status == SyncStatus.SKIPPED

def test_process_pending_tasks_independent_dispatch(
        gateway_service: GatewayService,
        mock_repository: MagicMock,
        mock_anytype_service: MagicMock,
        mock_linear_service: MagicMock
) -> None:
    """
    Verifies that during background processing, a failure in one service
    (AnyType) does not prevent the synchronization of the other (Linear).
    """
    # Arrange: A task queued for both platforms
    pending_task = Task(
        id=1,
        content="Sync to both",
        status=TaskStatus.RUNNING,
        anytype_sync_status=SyncStatus.PENDING,
        linear_sync_status=SyncStatus.PENDING,
        todoist_id="td_1",
        project_id="proj_1"
    )

    mock_repository.get_pending_tasks.return_value = [pending_task]

    # Simulate AnyType crashing
    mock_anytype_service.create_object.side_effect = Exception("AnyType is down!")

    # Act
    gateway_service.process_pending_tasks()

    # Assert
    mock_anytype_service.create_object.assert_called_once()
    mock_linear_service.create_issue.assert_called_once()

    # Check if the statuses were updated correctly despite the partial crash
    assert pending_task.anytype_sync_status == SyncStatus.PENDING # Remains pending due to crash
    assert pending_task.linear_sync_status == SyncStatus.SYNCED   # Succeeds independently

    # Ensure the repository saved the updated state at least once
    mock_repository.save.assert_called_with(pending_task)