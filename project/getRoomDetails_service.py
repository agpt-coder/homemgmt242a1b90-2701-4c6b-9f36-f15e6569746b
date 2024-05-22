from typing import List

import prisma
import prisma.models
from homeassistant_api import Client
from pydantic import BaseModel


class EntityDetail(BaseModel):
    """
    This type describes an entity within the room.
    """

    entityId: str
    entityName: str
    entityType: str


class RoomDetailsResponse(BaseModel):
    """
    This response model encapsulates detailed information about a room, including all associated entities derived from the HomeAssistant-API.
    """

    roomName: str
    entities: List[EntityDetail]


async def getRoomDetails(roomId: str) -> RoomDetailsResponse:
    """
    Fetches detailed information about a specific room, including the entities within the room. This information is fetched using the HomeAssistant-API. Access is restricted to authenticated users.

    Args:
        roomId (str): The unique identifier for the room whose details are being requested.

    Returns:
        RoomDetailsResponse: This response model encapsulates detailed information about a room, including all associated entities derived from the HomeAssistant-API.

    Example:
        room_details = await getRoomDetails("1")
    """
    client = Client(
        url="http://your-homeassistant-url", token="your-long-lived-access-token"
    )
    room = await prisma.models.Room.prisma().find_unique(
        where={"id": int(roomId)}, include={"entities": True}
    )
    if room is None:
        raise ValueError("Room not found")
    entity_details = []
    if room.entities:
        entity_details = [
            EntityDetail(
                entityId=str(entity.id),
                entityName=entity.name,
                entityType=entity.entityType,
            )
            for entity in room.entities
        ]
    return RoomDetailsResponse(roomName=room.name, entities=entity_details)
