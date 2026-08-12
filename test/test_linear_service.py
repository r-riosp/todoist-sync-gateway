import pytest
from unittest.mock import MagicMock, patch
from app.services.linear_service import LinearService
from app.schemas.task import Task
from app.models.enums import TaskStatus

@pytest.fixture
def mock_gql_client() -> MagicMock:
    """
    Mocks the GraphQL Client used within the LinearService.
    Intercepts the Client instantiation to prevent actual HTTP requests.
    """
    with patch("app.services.linear_service.Client") as mock_client_class:
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def linear_service(mock_gql_client: MagicMock) -> LinearService:
    """
    Instantiates the LinearService with dummy credentials.
    The internal GraphQL client is mocked via the mock_gql_client fixture.
    """
    return LinearService(api_key="fake-linear-key", team_id="fake-team-id")

def test_create_issue_success(linear_service: LinearService, mock_gql_client: MagicMock) -> None:
    """
    Verifies that a successful GraphQL mutation extracts the issue ID correctly
    and does not raise any exceptions.
    """
    # Arrange
    input_task = Task(
        content="Fix API bug",
        description="The endpoint is returning 500.",
        status=TaskStatus.RUNNING,
        todoist_id="td_123",
        project_id="proj_123"
    )

    # Simulating a successful GraphQL response from Linear
    mock_gql_client.execute.return_value = {
        "issueCreate": {
            "success": True,
            "issue": {
                "id": "lin_789",
                "title": "Fix API bug"
            }
        }
    }

    # Act
    linear_service.create_issue(input_task)

    # Assert
    mock_gql_client.execute.assert_called_once()

    # Verify if variables were mapped correctly in the mutation
    called_args = mock_gql_client.execute.call_args
    variables = called_args.kwargs.get("variable_values")

    assert variables is not None
    assert variables["title"] == "Fix API bug"
    assert variables["description"] == "The endpoint is returning 500."
    assert variables["teamId"] == "fake-team-id"

def test_create_issue_failure_response(linear_service: LinearService, mock_gql_client: MagicMock) -> None:
    """
    Verifies that if the Linear API returns success: false, the service raises an exception.
    """
    # Arrange
    input_task = Task(
        content="Fail Task",
        status=TaskStatus.RUNNING,
        todoist_id="td_123",
        project_id="proj_123"
    )

    # Simulating a rejected GraphQL response
    mock_gql_client.execute.return_value = {
        "issueCreate": {
            "success": False
        }
    }

    # Act & Assert
    with pytest.raises(Exception, match="Linear mutation failed."):
        linear_service.create_issue(input_task)