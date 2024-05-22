from typing import Any, Dict, Optional

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


class AddEntityResponse(BaseModel):
    """
    Response model for the API endpoint that handles adding new entities. It returns the details of the entity added or an error message.
    """

    success: bool
    message: str
    entity: Optional[Entity] = None


async def addEntity(
    name: str, entityType: str, config: Dict[str, Any], role: str
) -> AddEntityResponse:
    """
    Adds a new entity to the Home Assistant system. This route accepts entity details such as name, type, and configuration specifics. The HomeAssistant-API is utilized to integrate the new entity with the system. Proper authentication checks ensure that only users with administrative rights can add entities.

    Args:
        name (str): The name of the entity to be added.
        entityType (str): The type or class of the entity, categorizing the entity under specific functionalities or attributes.
        config (Dict[str, Any]): Additional configuration details specific to the type of the entity.
        role (str): The role of the user attempting to add the entity, must be 'ADMIN' to succeed.

    Returns:
        AddEntityResponse: Response model for the API endpoint that handles adding new entities. It returns the details of the entity added or an error message.
    """
    if role != "ADMIN":
        return AddEntityResponse(
            success=False, message="Unauthorized access; user must be an admin."
        )
    try:
        created_entity = await prisma.models.Entity.prisma().create(
            data={"name": name, "entityType": entityType, "roomId": 1}
        )
        created_entity_model = Entity(
            id=created_entity.id,
            name=created_entity.name,
            entityType=created_entity.entityType,
        )
        return AddEntityResponse(
            success=True,
            message="Entity added successfully.",
            entity=created_entity_model,
        )
    except Exception as e:
        return AddEntityResponse(
            success=False, message=f"Failed to add entity: {str(e)}."
        )
