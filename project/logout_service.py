import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Provides a confirmation message indicating whether the session token was successfully invalidated.
    """

    status: str
    message: str


async def logout(token: str) -> LogoutResponse:
    """
    Logs out a user by invalidating their session token. This helps in maintaining the security by ensuring that the sessions remain active only until the user wishes to keep them.

    Args:
        token (str): The session token that the user wants to invalidate for logging out.

    Returns:
        LogoutResponse: Provides a confirmation message indicating whether the session token was successfully invalidated.
    """
    session = await prisma.models.Session.prisma().find_unique(where={"id": int(token)})
    if session and session.valid:
        await prisma.models.Session.prisma().update(
            where={"id": int(token)}, data={"valid": False}
        )
        return LogoutResponse(
            status="success", message="Session invalidated successfully."
        )
    else:
        return LogoutResponse(
            status="failure", message="No valid session found or already invalidated."
        )
