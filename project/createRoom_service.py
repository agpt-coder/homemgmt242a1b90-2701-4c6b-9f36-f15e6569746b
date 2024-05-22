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


class Entity(BaseModel):
    """
    Specific entities within a room, characterized by type and name.
    """

    id: int
    name: str
    entityType: str


class CreateRoomResponse(BaseModel):
    """
    Response model returning details of the newly created room including any associated entities.
    """

    room_id: int
    room_name: str
    entities: List[Entity]


async def createRoom(
    room_name: str, entities: List[int], user_role: Role
) -> CreateRoomResponse:
    """
    Allows the creation of a new room by specifying details such as room name and entities. This endpoint modifies the room layout and requires an admin level access.

    Args:
        room_name (str): The name of the room to create.
        entities (List[int]): Optional list of entity IDs to associate with the room upon creation.
        user_role (Role): Role of the user making the request, must be 'ADMIN' to proceed.

    Returns:
        CreateRoomResponse: Response model returning details of the newly created room including any associated entities.

    Raises:
        PermissionError: If the user_role is not 'ADMIN'.
        Exception: If room creation fails due to database errors or missing entities.
    """
    if user_role != Role.ADMIN:
        raise PermissionError("Only users with ADMIN role can create rooms.")
    new_room = await prisma.models.Room.prisma().create(data={"name": room_name})
    associated_entities = []
    for entity_id in entities:
        entity = await prisma.models.Entity.prisma().update(
            where={"id": entity_id}, data={"room_id": new_room.id}
        )
        associated_entities.append(entity)
    response = CreateRoomResponse(
        room_id=new_room.id, room_name=new_room.name, entities=associated_entities
    )
    return response
