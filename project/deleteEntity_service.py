import prisma
import prisma.models
from pydantic import BaseModel


class DeleteEntityResponse(BaseModel):
    """
    This model provides a confirmation message indicating the result of the deletion operation.
    """

    message: str
    deletedEntityId: int


async def deleteEntity(entityId: int) -> DeleteEntityResponse:
    """
    Removes an entity from the Home Assistant configuration by entityId. This endpoint will delete the entity from the database.

    Args:
        entityId (int): The unique identifier of the entity to be deleted.

    Returns:
        DeleteEntityResponse: This model provides a confirmation message indicating the result of the deletion operation.
    """
    entity = await prisma.models.Entity.prisma().find_unique(where={"id": entityId})
    if entity is None:
        return DeleteEntityResponse(
            message="Entity not found.", deletedEntityId=entityId
        )
    await prisma.models.Entity.prisma().delete(where={"id": entityId})
    return DeleteEntityResponse(
        message="Entity successfully deleted.", deletedEntityId=entityId
    )
