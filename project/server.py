import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

import project.addEntity_service
import project.addService_service
import project.createEntity_service
import project.createRoom_service
import project.createUser_service
import project.deleteEntity_service
import project.deleteRoom_service
import project.deleteService_service
import project.deleteUser_service
import project.getRoomDetails_service
import project.getTests_service
import project.getUser_service
import project.listEntities_service
import project.listEntitiesByRoom_service
import project.listRooms_service
import project.listServices_service
import project.login_service
import project.logout_service
import project.updateEntity_service
import project.updateRoom_service
import project.updateService_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="homemgmt",
    lifespan=lifespan,
    description="use `pip install HomeAssistant-API` to expose the api endpoints to list the services, the entities, and rooms",
)


@app.delete(
    "/entities/{entityId}",
    response_model=project.deleteEntity_service.DeleteEntityResponse,
)
async def api_delete_deleteEntity(
    entityId: int,
) -> project.deleteEntity_service.DeleteEntityResponse | Response:
    """
    Removes an entity from the Home Assistant configuration by entityId. This endpoint will delete the entity from the database and also notify the HomeAssistant API to remove the entity from its active list.
    """
    try:
        res = await project.deleteEntity_service.deleteEntity(entityId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/services/{serviceId}",
    response_model=project.deleteService_service.DeleteServiceResponse,
)
async def api_delete_deleteService(
    serviceId: int, admin_userId: int
) -> project.deleteService_service.DeleteServiceResponse | Response:
    """
    Enables administrators to delete a service by its ID. It requires admin rights, checks the existence of the service in the HomeAssistant-API database, and removes it securely if present.
    """
    try:
        res = project.deleteService_service.deleteService(serviceId, admin_userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/rooms/{roomId}", response_model=project.deleteRoom_service.DeleteRoomResponse
)
async def api_delete_deleteRoom(
    roomId: int,
) -> project.deleteRoom_service.DeleteRoomResponse | Response:
    """
    Removes a room from the system. This action is irreversible and therefore restricted to admin users only to prevent misuse.
    """
    try:
        res = project.deleteRoom_service.deleteRoom(roomId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/services", response_model=project.addService_service.CreateServiceResponse
)
async def api_post_addService(
    service_name: str, installation_cmd: str, admin_id: int
) -> project.addService_service.CreateServiceResponse | Response:
    """
    Allows administrators to add a new service to the database. It takes service details as input, verifies admin privileges, and updates the HomeAssistant-API database accordingly.
    """
    try:
        res = await project.addService_service.addService(
            service_name, installation_cmd, admin_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/rooms", response_model=project.listRooms_service.GetRoomsResponse)
async def api_get_listRooms(
    request: project.listRooms_service.GetRoomsRequest,
) -> project.listRooms_service.GetRoomsResponse | Response:
    """
    Retrieves a list of all rooms. Each room includes details such as name and associated entities. This endpoint will utilize the HomeAssistant-API to gather room data and is protected to ensure only authenticated users access it.
    """
    try:
        res = await project.listRooms_service.listRooms(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/tests", response_model=project.getTests_service.test)
async def api_get_getTests() -> project.getTests_service.test | Response:
    """
    getsallthetests
    """
    try:
        res = await project.getTests_service.getTests()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    username: str, password: str, role: project.createUser_service.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    Creates a new user. Endpoint takes a JSON payload with user details such as username, password, and roles. It returns the user ID upon successful creation. User password is hashed for security.
    """
    try:
        res = await project.createUser_service.createUser(username, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/services/{serviceId}",
    response_model=project.updateService_service.UpdateServiceResponse,
)
async def api_put_updateService(
    serviceId: int, serviceName: Optional[str], installationCmd: Optional[str]
) -> project.updateService_service.UpdateServiceResponse | Response:
    """
    Provides functionality for updating an existing service's details. Only accessible by admins, this endpoint expects a service ID as part of the URL, and updates the specific service data in the HomeAssistant-API.
    """
    try:
        res = await project.updateService_service.updateService(
            serviceId, serviceName, installationCmd
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/entities", response_model=project.listEntities_service.GetEntitiesResponse)
async def api_get_listEntities(
    authorization: str,
) -> project.listEntities_service.GetEntitiesResponse | Response:
    """
    Retrieves a list of all entities managed by Home Assistant. Each entity includes details such as name, type, and status. The 'pip install HomeAssistant-API' is used internally to fetch this data. Authentication is required to ensure only authorized users can access this information.
    """
    try:
        res = await project.listEntities_service.listEntities(authorization)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/logout", response_model=project.logout_service.LogoutResponse)
async def api_post_logout(
    token: str,
) -> project.logout_service.LogoutResponse | Response:
    """
    Logs out a user by invalidating their session token. This helps in maintaining the security by ensuring that the sessions remain active only until the user wishes to keep them.
    """
    try:
        res = await project.logout_service.logout(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: int,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a user from the system by their user ID. It ensures that the right authorization levels are checked before deletion to maintain data integrity.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    username: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Authenticates a user by their username and password. Successful authentication returns a session token, which is necessary for interacting with protected endpoints.
    """
    try:
        res = await project.login_service.login(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/entities/{entityId}",
    response_model=project.updateEntity_service.EntityUpdateResponse,
)
async def api_put_updateEntity(
    entityId: str, name: str, entityType: str
) -> project.updateEntity_service.EntityUpdateResponse | Response:
    """
    Updates an existing entity's details within the Home Assistant framework. Inputs such as name or type can be modified. This operation is protected and leverages the HomeAssistant-API for seamless updates. Only authorized users can perform updates, ensuring system integrity.
    """
    try:
        res = await project.updateEntity_service.updateEntity(
            entityId, name, entityType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/rooms", response_model=project.createRoom_service.CreateRoomResponse)
async def api_post_createRoom(
    room_name: str, entities: List[int], user_role: project.createRoom_service.Role
) -> project.createRoom_service.CreateRoomResponse | Response:
    """
    Allows the creation of a new room by specifying details such as room name and entities. This endpoint modifies the room layout and requires an admin level access.
    """
    try:
        res = await project.createRoom_service.createRoom(
            room_name, entities, user_role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/entities", response_model=project.createEntity_service.CreateEntityResponse)
async def api_post_createEntity(
    entityName: str, entityType: str, roomId: int, attributes: Dict[str, str]
) -> project.createEntity_service.CreateEntityResponse | Response:
    """
    Allows the creation of a new entity in the Home Assistant setup. Requires details like entity ID, initial state, and attributes. This operation updates the database and also informs the HomeAssistant service to include the new entity.
    """
    try:
        res = await project.createEntity_service.createEntity(
            entityName, entityType, roomId, attributes
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/entities", response_model=project.addEntity_service.AddEntityResponse)
async def api_post_addEntity(
    name: str, entityType: str, config: Dict[str, Any], role: str
) -> project.addEntity_service.AddEntityResponse | Response:
    """
    Adds a new entity to the Home Assistant system. This route accepts entity details such as name, type, and configuration specifics. The HomeAssistant-API is utilized to integrate the new entity with the system. Proper authentication checks ensure that only users with administrative rights can add entities.
    """
    try:
        res = await project.addEntity_service.addEntity(name, entityType, config, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/services", response_model=project.listServices_service.GetServicesResponse)
async def api_get_listServices(
    request: project.listServices_service.GetServicesRequest,
) -> project.listServices_service.GetServicesResponse | Response:
    """
    Retrieves a list of all services available in the Home Assistant environment. It returns details like service name, domain, and description. This route queries the HomeAssistant API to fetch the services and responds with a JSON listing each service.
    """
    try:
        res = await project.listServices_service.listServices(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/rooms/{roomId}/entities",
    response_model=project.listEntitiesByRoom_service.GetRoomEntitiesResponse,
)
async def api_get_listEntitiesByRoom(
    roomId: int,
) -> project.listEntitiesByRoom_service.GetRoomEntitiesResponse | Response:
    """
    Lists all entities assigned to a specified room. Useful for both users and admins to overview the equipment or devices in a room. This list is pulled using HomeAssistant-API.
    """
    try:
        res = await project.listEntitiesByRoom_service.listEntitiesByRoom(roomId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}",
    response_model=project.updateUser_service.UpdateUserDetailsResponse,
)
async def api_put_updateUser(
    password: str, userId: str, role: project.updateUser_service.Role
) -> project.updateUser_service.UpdateUserDetailsResponse | Response:
    """
    Updates a user's details such as roles and password, identified by user ID. Enhanced security measures are enforced to protect sensitive data.
    """
    try:
        res = await project.updateUser_service.updateUser(password, userId, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/rooms/{roomId}", response_model=project.getRoomDetails_service.RoomDetailsResponse
)
async def api_get_getRoomDetails(
    roomId: str,
) -> project.getRoomDetails_service.RoomDetailsResponse | Response:
    """
    Fetches detailed information about a specific room, including the entities within the room. This information is fetched using the HomeAssistant-API. Access is restricted to authenticated users.
    """
    try:
        res = await project.getRoomDetails_service.getRoomDetails(roomId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserDetailsResponse)
async def api_get_getUser(
    userId: int,
) -> project.getUser_service.UserDetailsResponse | Response:
    """
    Fetches a specific user's information by user ID. It ensures confidentiality by limiting data exposure to authorized roles.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/rooms/{roomId}",
    response_model=project.updateRoom_service.UpdateRoomDetailsResponse,
)
async def api_put_updateRoom(
    roomId: int, name: Optional[str], entities: List[int]
) -> project.updateRoom_service.UpdateRoomDetailsResponse | Response:
    """
    Updates details of an existing room, such as the name or entities list. Only accessible by admins to ensure security over modifications.
    """
    try:
        res = await project.updateRoom_service.updateRoom(roomId, name, entities)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
