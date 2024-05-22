import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model indicating the result of the deleteUser operation. It will either confirm successful deletion or provide an error explaining why the deletion could not be performed.
    """

    status: str
    message: str


async def deleteUser(userId: int) -> DeleteUserResponse:
    """
    Deletes a user from the system by their user ID. It ensures that the right authorization levels are checked before deletion to maintain data integrity.

    Args:
    userId (int): The unique identifier of the user to be deleted.

    Returns:
    DeleteUserResponse: Response model indicating the result of the deleteUser operation. It will either confirm successful deletion or provide an error explaining why the deletion could not be performed.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"sessions": True, "rooms": True}
    )
    if user is None:
        return DeleteUserResponse(
            status="Error", message="prisma.models.User not found."
        )
    if len(user.sessions) > 0:
        return DeleteUserResponse(
            status="Error",
            message="prisma.models.User cannot be deleted because there are active sessions.",
        )
    if len(user.rooms) > 0:
        return DeleteUserResponse(
            status="Error",
            message="prisma.models.User cannot be deleted because there are rooms associated with them.",
        )
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponse(
        status="Success", message="prisma.models.User deleted successfully."
    )
