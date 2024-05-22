import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum defining the permissible roles within the system.
    """

    ADMIN: str
    USER: str


class CreateUserResponse(BaseModel):
    """
    Output model for creating a new user. Returns the new user's unique ID.
    """

    user_id: int


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


async def createUser(username: str, password: str, role: Role) -> CreateUserResponse:
    """
    Creates a new user. Endpoint takes a JSON payload with user details such as username, password, and roles.
    It returns the user ID upon successful creation. User password is hashed for security.

    Args:
        username (str): The username for the new user account. It should be unique.
        password (str): The password for the new user account. It will be hashed before storage.
        role (Role): The role assigned to the new user, which must be an existing role in the Role enum.

    Returns:
        CreateUserResponse: Output model for creating a new user. Returns the new user's unique ID.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": username}
    )
    if existing_user:
        raise ValueError("Username already exists, please choose another username.")
    hashed_password = hash_password(password)
    new_user = await prisma.models.User.prisma().create(
        data={"email": username, "password": hashed_password, "role": role}
    )
    return CreateUserResponse(user_id=new_user.id)
