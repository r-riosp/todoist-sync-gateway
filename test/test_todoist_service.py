import pytest
from unittest.mock import MagicMock
from app.services.todoist_service import TodoistService
from app.services.gateway_service import GatewayService
from app.schemas.task import Task
from app.models.enums import TaskStatus

@pytest.fixture
def mock_gateway_service() -> MagicMock:
    """
    Provides a mocked instance of GatewayService.
    Isolates the TodoistService from downstream task processing and external API calls.
    """
    return MagicMock(spec=GatewayService)

@pytest.fixture
def todoist_service(mock_gateway_service: MagicMock) -> TodoistService:
    """
    Instantiates the TodoistService with the mocked GatewayService injected.
    """
    return TodoistService(api_key="fake-todoist-api-key", gateway_service=mock_gateway_service)

def test_process_webhook_item_added(
        todoist_service: TodoistService,
        mock_gateway_service: MagicMock
) -> None:
    """
    Tests the webhook processing for the 'item:added' event.
    Ensures the external payload is correctly parsed into the internal Task schema
    and dispatched to the GatewayService.
    """
    event_name = "item:added"
    event_data = {
        "content": "Review Pull Request",
        "description": "Check the new authentication flow.",
        "id": "td_98765",
        "project_id": "proj_12345",
        "labels": ["work", "review"]
    }

    todoist_service.process_webhook(event_name, event_data)

    mock_gateway_service.create_task.assert_called_once()

    created_task = mock_gateway_service.create_task.call_args[0][0]

    assert isinstance(created_task, Task)
    assert created_task.content == "Review Pull Request"
    assert created_task.description == "Check the new authentication flow."
    assert created_task.todoist_id == "td_98765"
    assert created_task.project_id == "proj_12345"
    assert created_task.tags == ["work", "review"]
    assert created_task.status == TaskStatus.RUNNING

def test_process_webhook_item_completed(
        todoist_service: TodoistService,
        mock_gateway_service: MagicMock
) -> None:
    """
    Tests the webhook processing for the 'item:completed' event.
    Ensures that task creation is not triggered for completion events.
    """
    event_name = "item:completed"
    event_data = {"id": "td_98765"}

    result = todoist_service.process_webhook(event_name, event_data)

    assert result is None
    mock_gateway_service.create_task.assert_not_called()

def test_process_webhook_unknown_event(
        todoist_service: TodoistService,
        mock_gateway_service: MagicMock
) -> None:
    """
    Tests the fallback behavior when an unknown event is received.
    The service should safely ignore it without side effects.
    """
    event_name = "item:deleted"
    event_data = {"id": "td_98765"}

    result = todoist_service.process_webhook(event_name, event_data)

    assert result is None
    mock_gateway_service.create_task.assert_not_called()