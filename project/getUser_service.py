from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum defining the permissible roles within the system.
    """

    ADMIN: str
    USER: str


class Session(BaseModel):
    """
    Session details including identifiers and timestamps.
    """

    id: int
    createdAt: datetime
    valid: bool


class Entity(BaseModel):
    """
    Specific entities within a room, characterized by type and name.
    """

    id: int
    name: str
    entityType: str


class Room(BaseModel):
    """
    Details of the room assigned to the user including room name and associated entities.
    """

    id: int
    name: str
    entities: List[Entity]


class UserDetailsResponse(BaseModel):
    """
    Response model representing detailed information of a user. Includes sensitive information covered under role-based access.
    """

    id: int
    email: str
    role: Role
    sessions: List[Session]
    rooms: List[Room]


async def getUser(userId: int) -> UserDetailsResponse:
    """
    Fetches a specific user's information by user ID. It ensures confidentiality by limiting data exposure to authorized roles.

    Args:
        userId (int): The unique identifier for the user. It's used to fetch the specific user details from the database.

    Returns:
        UserDetailsResponse: Response model representing detailed information of a user. Includes sensitive information covered under role-based access.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId},
        include={"sessions": True, "rooms": {"include": {"entities": True}}},
    )
    if user is None:
        raise ValueError(f"No user found with ID {userId}")
    user_details = UserDetailsResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        sessions=[
            Session(id=session.id, createdAt=session.createdAt, valid=session.valid)
            for session in user.sessions
        ],
        rooms=[
            Room(
                id=room.id,
                name=room.name,
                entities=[
                    Entity(id=entity.id, name=entity.name, entityType=entity.entityType)
                    for entity in room.entities
                ],
            )
            for room in user.rooms
        ],
    )
    return user_details
