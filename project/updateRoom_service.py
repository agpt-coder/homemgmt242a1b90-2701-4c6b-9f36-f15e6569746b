from typing import List, Optional

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


class Room(BaseModel):
    """
    Details of the room assigned to the user including room name and associated entities.
    """

    id: int
    name: str
    entities: List[Entity]


class UpdateRoomDetailsResponse(BaseModel):
    """
    Response model returning the updated details of the room, reflecting any changes made.
    """

    room: Room


async def updateRoom(
    roomId: int, name: Optional[str], entities: List[int]
) -> UpdateRoomDetailsResponse:
    """
    Updates details of an existing room, such as the name or entities list. Only accessible by admins to ensure security over modifications.

    Args:
        roomId (int): The unique identifier of the room to be updated.
        name (Optional[str]): The new name to update the room with, if None, name isn't changed.
        entities (List[int]): List of entity IDs to update in the room. This includes removing or adding entities.

    Returns:
        UpdateRoomDetailsResponse: Response model returning the updated details of the room, reflecting any changes made.
    """
    room = await prisma.models.Room.prisma().find_unique(
        where={"id": roomId}, include={"entities": True}
    )
    if room is None:
        raise ValueError("Room not found")
    update_data = {"name": name} if name is not None else {}
    current_entity_ids = {entity.id for entity in room.entities}
    await prisma.models.Entity.prisma().delete_many(
        where={"id": {"in": list(current_entity_ids - set(entities))}, "roomId": roomId}
    )
    entities_to_add = [
        {"id": entity_id, "roomId": roomId}
        for entity_id in set(entities) - current_entity_ids
    ]
    if entities_to_add:
        await prisma.models.Entity.prisma().create_many(
            data=entities_to_add, skip_duplicates=True
        )
    if update_data:
        await prisma.models.Room.prisma().update(where={"id": roomId}, data=update_data)
    updated_room = await prisma.models.Room.prisma().find_unique(
        where={"id": roomId}, include={"entities": True}
    )
    if updated_room is None:
        raise Exception("Failed to retrieve updated room information")
    return UpdateRoomDetailsResponse(room=updated_room)
