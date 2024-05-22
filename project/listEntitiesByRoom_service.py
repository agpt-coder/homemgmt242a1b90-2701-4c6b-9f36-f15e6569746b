from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Entity(BaseModel):
    """
    Specific entities within a room, characterized by type and name.
    """

    id: int
    name: str
    entityType: str


class GetRoomEntitiesResponse(BaseModel):
    """
    Model to handle the output of the entities retrieved from a specific room based on the given room ID. This shows details of each entity.
    """

    entities: List[Entity]


async def listEntitiesByRoom(roomId: int) -> GetRoomEntitiesResponse:
    """
    Lists all entities assigned to a specified room. Useful for both users and admins to overview the equipment or devices in a room.
    This list is pulled using synchronous calls to a Home-Assistant API modeled with prisma.

    Args:
    roomId (int): The unique identifier for a room whose entities are to be listed.

    Returns:
    GetRoomEntitiesResponse: Model to handle the output of entities retrieved from a specific room based on the given room ID. This shows details of each entity.
    """
    entities_data = await prisma.models.Entity.prisma().find_many(
        where={"roomId": roomId}
    )
    entities = [
        Entity(id=e.id, name=e.name, entityType=e.entityType) for e in entities_data
    ]
    return GetRoomEntitiesResponse(entities=entities)
