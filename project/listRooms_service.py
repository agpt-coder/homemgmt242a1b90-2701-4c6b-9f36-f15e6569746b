from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetRoomsRequest(BaseModel):
    """
    Request model for fetching all rooms. No body or query parameters are required as this is a simple GET request to list all rooms.
    """

    pass


class EntityBasicInfo(BaseModel):
    """
    Basic information about an entity within a room.
    """

    id: int
    name: str
    entityType: str


class RoomDetailed(BaseModel):
    """
    Detailed information about each room including associated entities.
    """

    id: int
    name: str
    entities: List[EntityBasicInfo]


class GetRoomsResponse(BaseModel):
    """
    Response model representing a list of rooms with their details and associated entities.
    """

    rooms: List[RoomDetailed]


async def listRooms(request: GetRoomsRequest) -> GetRoomsResponse:
    """
    Retrieves a list of all rooms. Each room includes details such as name and associated entities. This endpoint will utilize the HomeAssistant-API to gather room data and is protected to ensure only authenticated users access it.

    Args:
        request (GetRoomsRequest): Request model for fetching all rooms. No body or query parameters are required as this is a simple GET request to list all rooms.

    Returns:
        GetRoomsResponse: Response model representing a list of rooms with their details and associated entities.
    """
    rooms_records = await prisma.models.Room.prisma().find_many(
        include={"entities": True}
    )
    room_details_list = []
    for room_record in rooms_records:
        entity_list = (
            [
                EntityBasicInfo(
                    id=entity.id, name=entity.name, entityType=entity.entityType
                )
                for entity in room_record.entities
            ]
            if room_record.entities
            else []
        )
        room_details = RoomDetailed(
            id=room_record.id, name=room_record.name, entities=entity_list
        )
        room_details_list.append(room_details)
    response = GetRoomsResponse(rooms=room_details_list)
    return response
