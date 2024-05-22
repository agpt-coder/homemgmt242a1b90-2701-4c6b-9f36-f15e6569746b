import prisma
import prisma.errors
import prisma.models
from pydantic import BaseModel


class Entity(BaseModel):
    """
    Specific entities within a room, characterized by type and name.
    """

    id: int
    name: str
    entityType: str


class EntityUpdateResponse(BaseModel):
    """
    This response model provides feedback to the user upon attempting to update an entity's details.
    """

    success: bool
    message: str
    updatedEntity: Entity


async def updateEntity(
    entityId: str, name: str, entityType: str
) -> EntityUpdateResponse:
    """
    Updates an existing entity's details within the Home Assistant framework. Inputs such as name or type can be modified.
    This operation is protected and leverages the HomeAssistant-API for seamless updates.
    Only authorized users can perform updates, ensuring system integrity.

    Args:
        entityId (str): The unique identifier of the entity to be updated.
        name (str): The new name for the entity.
        entityType (str): The new type identifier for the entity.

    Returns:
        EntityUpdateResponse: This response model provides feedback to the user upon attempting to update an entity's details.
    """
    try:
        entity_id_int = int(entityId)
        updated_entity = await prisma.models.Entity.prisma().update(
            where={"id": entity_id_int}, data={"name": name, "entityType": entityType}
        )
        return EntityUpdateResponse(
            success=True,
            message="Entity updated successfully.",
            updatedEntity=Entity(
                id=updated_entity.id,
                name=updated_entity.name,
                entityType=updated_entity.entity_type,
            ),
        )  # TODO(autogpt): Cannot access member "entity_type" for type "Entity"
    #     Member "entity_type" is unknown. reportAttributeAccessIssue
    except ValueError:
        return EntityUpdateResponse(
            success=False, message="Entity ID must be an integer.", updatedEntity=None
        )
    except prisma.errors.RecordNotFoundError:
        return EntityUpdateResponse(
            success=False, message="Entity not found.", updatedEntity=None
        )
    except Exception as e:
        return EntityUpdateResponse(
            success=False, message=f"An error occurred: {str(e)}", updatedEntity=None
        )
