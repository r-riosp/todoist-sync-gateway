import httpx
from app.core.logging import setup_logging
from app.schemas.anytype import ObjectPayload
from app.core.config import config

logger = setup_logging()

class AnyTypeService():
    """
    Service responsible for communicating with the AnyType local API.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initializes the service with authentication headers.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Anytype-Version": "2025-11-08"
        }

    def get_spaces(self):
        """
        Fetches all spaces available in AnyType.
        """
        endpoint = f"{self.base_url}/spaces"
        logger.info("Fetching spaces from AnyType API at %s", endpoint)
        try:
            response = httpx.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error occurred while fetching spaces: %s - %s", e.response.status_code, e.response.text)
            raise
        except httpx.RequestError as e:
            logger.error("Request error occurred while fetching spaces: %s", e)
            raise
        except Exception as e:
            logger.exception("Unexpected error occurred")
            raise

    def get_space(self, space_id: str):
        """
        Fetches a specific space by ID.
        """
        endpoint = f"{self.base_url}/spaces/{space_id}"
        logger.info("Fetching space with ID %s from AnyType API at %s", space_id, endpoint)
        pass # To be implemented

    def create_object(self, payload: dict):
        """
        Creates a new object in the specified AnyType space.
        """
        space_id = config.anytype_space_id
        endpoint = f"{self.base_url}/spaces/{space_id}/objects"

        logger.info("Creating AnyType object at %s", endpoint)
        try:
            response = httpx.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error("AnyType returned HTTP %s: %s", e.response.status_code, e.response.text)
            raise
        except httpx.RequestError as e:
            logger.error("Could not connect to AnyType at %s: %s", e.request.url, e)
            raise # CRUCIAL: Must raise so the Gateway marks it as PENDING and not SYNCED
        except Exception:
            logger.exception("Unexpected error occurred while creating object in AnyType")
            raise