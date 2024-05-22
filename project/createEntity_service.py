from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class CreateEntityResponse(BaseModel):
    """
    Response model for the creation of an entity. Provides confirmation and any relevant entity details upon successful creation.
    """

    success: bool
    entityId: int
    message: str


async def createEntity(
    entityName: str, entityType: str, roomId: int, attributes: Dict[str, str]
) -> CreateEntityResponse:
    """
    Allows the creation of a new entity in the Home Assistant setup. Requires details like entity ID, initial state, and attributes. This operation updates the database and also informs the HomeAssistant service to include the new entity.

    Args:
        entityName (str): The name of the entity. Must be unique within the specific room.
        entityType (str): The type designation of the entity (e.g., light, sensor, etc.)
        roomId (int): The identifier of the room the entity is associated with. This must correlate with a valid Room stored within the system.
        attributes (Dict[str, str]): A dictionary of attributes that define the entity's settings and characteristics.

    Returns:
        CreateEntityResponse: Response model for the creation of an entity. Provides confirmation and any relevant entity details upon successful creation.
    """
    room = await prisma.models.Room.prisma().find_unique(where={"id": roomId})
    if room is None:
        return CreateEntityResponse(
            success=False, entityId=-1, message=f"No room found with ID {roomId}."
        )
    existing_entity = await prisma.models.Entity.prisma().find_first(
        where={"AND": [{"roomId": roomId}, {"name": entityName}]}
    )
    if existing_entity:
        return CreateEntityResponse(
            success=False,
            entityId=-1,
            message=f"Entity name '{entityName}' already exists in room {roomId}.",
        )
    created_entity = await prisma.models.Entity.prisma().create(
        data={"name": entityName, "entityType": entityType, "roomId": roomId}
    )
    return CreateEntityResponse(
        success=True, entityId=created_entity.id, message="Entity successfully created."
    )
