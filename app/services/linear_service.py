from gql import gql, Client
from gql.transport.httpx import HTTPXTransport
from app.core.logging import setup_logging
from app.schemas.task import Task

logger = setup_logging()

class LinearService:
    """
    Service responsible for communicating with the Linear GraphQL API.
    """

    def __init__(self, api_key: str, team_id: str) -> None:
        """
        Initializes the GraphQL client with HTTPX transport and authentication.
        """
        self._team_id = team_id
        transport = HTTPXTransport(
            url="https://api.linear.app/graphql",
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
        )
        self._client = Client(transport=transport, fetch_schema_from_transport=False)

    def create_issue(self, task: Task) -> None:
        """
        Creates a new issue in Linear based on the provided Task.
        Uses a GraphQL mutation to securely send the data.
        """
        logger.info("Dispatching task '%s' to Linear...", task.content)

        mutation = gql(
            """
            mutation IssueCreate($title: String!, $description: String, $teamId: String!) {
              issueCreate(input: {
                title: $title,
                description: $description,
                teamId: $teamId
              }) {
                success
                issue {
                  id
                  title
                }
              }
            }
            """
        )

        variables = {
            "title": task.content,
            "description": task.description if task.description else "No description provided.",
            "teamId": self._team_id
        }

        try:
            result = self._client.execute(mutation, variable_values=variables)

            if result.get("issueCreate", {}).get("success"):
                issue_id = result["issueCreate"]["issue"]["id"]
                logger.info("Successfully created issue in Linear: %s", issue_id)
            else:
                logger.error("Linear API returned a non-success response: %s", result)
                raise Exception("Linear mutation failed.")

        except Exception as e:
            logger.error("Failed to create issue in Linear: %s", e)
            raise