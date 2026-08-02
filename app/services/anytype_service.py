import httpx
import logging
from app.schemas.anytype import ObjectPayload

from app.core.config import config

class AnyTypeService():
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Anytype-Version": "2025-11-08"
        }

    def get_spaces(self):
        endpoint = f"{self.base_url}/spaces"
        
        logging.info(f"Fetching spaces from AnyType API at {endpoint}")

        try:
            response = httpx.get(endpoint, headers=self.headers)
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred while fetching spaces: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logging.error(f"Request error occurred while fetching spaces: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            raise
        return response
    
    def get_space(self, space_id: str):
        endpoint = f"{self.base_url}/spaces/{space_id}"
        logging.info(f"Fetching space with ID {space_id} from AnyType API at {endpoint}")

    # def create_space():

    def create_object(self, payload: ObjectPayload):
        space_id = "bafyreiczj2uki4b5wubo6pi6x6k3eikkodikdbe4qpptmbyx32ktjopzzm.1xs69v7ruddp9"
        endpoint = f"{self.base_url}/spaces/{space_id}/objects"

        logging.info(endpoint)

        try:
            response = httpx.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            response_data = response.json()
        except Exception as e:
            raise e
        pass

    # def update_space():

    # def show_objects():
