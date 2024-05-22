import prisma
import prisma.models
from pydantic import BaseModel, ValidationError


class LoginResponse(BaseModel):
    """
    This model represents the response returned upon successful authentication. It includes a session token.
    """

    session_token: str


async def login(username: str, password: str) -> LoginResponse:
    """
    Authenticates a user by their username and password. Successful authentication returns a session token, which is necessary for interacting with protected endpoints.

    Args:
        username (str): The username of the user trying to login.
        password (str): The password for the user trying to login.

    Returns:
        LoginResponse: This model represents the response returned upon successful authentication. It includes a session token.

    Raises:
        ValidationError: If authentication fails due to invalid credentials.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user or user.password != password:
        raise ValidationError("Invalid username or password")
    session = await prisma.models.Session.prisma().create(
        data={"userId": user.id, "valid": True}
    )
    return LoginResponse(session_token=str(session.id))
