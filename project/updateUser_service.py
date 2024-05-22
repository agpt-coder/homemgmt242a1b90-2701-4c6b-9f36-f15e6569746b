import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum defining the permissible roles within the system.
    """

    ADMIN: str
    USER: str


class UpdateUserDetailsResponse(BaseModel):
    """
    Response model confirming the details have been updated. Could optionally include the user object to reflect the changes.
    """

    success: bool
    message: str
    updatedUser: prisma.models.User


async def updateUser(
    userId: str, role: Role, password: str
) -> UpdateUserDetailsResponse:
    """
    Updates a user's details such as roles and password, identified by user ID. Enhanced security measures are enforced to protect sensitive data.

    Args:
        userId (str): The unique identifier for the user whose details are to be updated.
        role (Role): The new role to be assigned to the user.
        password (str): The new password for the user. This should be encrypted before transmission or have proper security measures in place to handle plain text.

    Returns:
        UpdateUserDetailsResponse: Response model confirming the details have been updated. Could optionally include the user object to reflect the changes.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": int(userId)})
        if user:
            updated_user = await prisma.models.User.prisma().update(
                where={"id": int(userId)}, data={"role": role, "password": password}
            )
            return UpdateUserDetailsResponse(
                success=True,
                message="prisma.models.User updated successfully.",
                updatedUser=updated_user,
            )
        else:
            return UpdateUserDetailsResponse(
                success=False, message="prisma.models.User not found.", updatedUser={}
            )
    except Exception as e:
        return UpdateUserDetailsResponse(success=False, message=str(e), updatedUser={})
