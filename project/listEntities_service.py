from typing import List

import httpx
from pydantic import BaseModel


class EntityDetails(BaseModel):
    """
    Detailed information about each entity.
    """

    name: str
    type: str
    status: str


class GetEntitiesResponse(BaseModel):
    """
    Response model returning a list of all entities managed by Home Assistant, each with details such as name, type, and status.
    """

    entities: List[EntityDetails]


async def listEntities(authorization: str) -> GetEntitiesResponse:
    """
    Retrieves a list of all entities managed by Home Assistant. Each entity includes details such as name, type, and status.
    An HTTP client is used to fetch this data from Home Assistant API. Authentication is required to ensure only authorized users can access this information.

    Args:
        authorization (str): Authorization token to verify if the user has the necessary permissions to access this data.

    Returns:
        GetEntitiesResponse: Response model returning a list of all entities managed by Home Assistant, each with details such as name, type, and status.
    """
    url = "https://your-homeassistant-api-domain.com/api/entities"
    headers = {"Authorization": f"Bearer {authorization}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        entities_data = response.json()
    entities = [
        EntityDetails(
            name=entity["name"],
            type=entity["type"],
            status=entity.get("status", "unknown"),
        )
        for entity in entities_data
    ]
    return GetEntitiesResponse(entities=entities)
