from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetServicesRequest(BaseModel):
    """
    API request model to retrieve all services available in the system. Authentication and role authorization is required to access this endpoint, ensuring that only authenticated users (admins and users) can query for available services.
    """

    pass


class ServiceDescription(BaseModel):
    """
    Describes a single service's essential information, making it easy for users to grasp what the service does and how it can be installed.
    """

    serviceName: str
    installationCmd: str


class GetServicesResponse(BaseModel):
    """
    Provides a user-friendly list of all available services in the system extracted and adapted from HomeAssistant-API. Each service contains essential information necessary for understanding and potentially installing the service.
    """

    services: List[ServiceDescription]


async def listServices(request: GetServicesRequest) -> GetServicesResponse:
    """
    Retrieves a list of all services available in the Home Assistant environment. It returns details like service name, domain, and description. This function queries the internal system database to fetch the services and responds with a structured overview of each service.

    Args:
        request (GetServicesRequest): API request model to retrieve all services available in the system. Authentication and role authorization is required to access this endpoint, ensuring that only authenticated users (admins and users) can query for available services.

    Returns:
        GetServicesResponse: Provides a user-friendly list of all available services in the system extracted and adapted from HomeAssistant-API. Each service contains essential information necessary for understanding and potentially installing the service.
    """
    service_records = await prisma.models.Service.prisma().find_many()
    descriptions = [
        ServiceDescription(
            serviceName=record.serviceName, installationCmd=record.installationCmd
        )
        for record in service_records
    ]
    return GetServicesResponse(services=descriptions)
