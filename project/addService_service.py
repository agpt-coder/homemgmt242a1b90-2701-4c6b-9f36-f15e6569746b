from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateServiceResponse(BaseModel):
    """
    This model provides feedback on the success or failure of the service addition process.
    """

    success: bool
    message: str
    service_id: Optional[int] = None


async def addService(
    service_name: str, installation_cmd: str, admin_id: int
) -> CreateServiceResponse:
    """
    Allows administrators to add a new service to the database. It takes service details as input, verifies admin privileges, and updates the HomeAssistant-API database accordingly.

    Args:
        service_name (str): The human-readable name of the service to be added.
        installation_cmd (str): The command line instruction used to install the service.
        admin_id (int): The user ID of the administrator performing the operation, used to verify admin privileges.

    Returns:
        CreateServiceResponse: This model provides feedback on the success or failure of the service addition process.
    """
    admin = await prisma.models.User.prisma().find_unique(
        where={"id": admin_id}, include={"role": True}
    )
    if not admin or admin.role != prisma.enums.Role.ADMIN:
        return CreateServiceResponse(
            success=False, message="Unauthorized: Only admins can add services."
        )
    try:
        new_service = await prisma.models.Service.prisma().create(
            data={"serviceName": service_name, "installationCmd": installation_cmd}
        )
        return CreateServiceResponse(
            success=True,
            message="Service successfully added.",
            service_id=new_service.id,
        )
    except Exception as e:
        return CreateServiceResponse(
            success=False, message=f"Failed to add service: {str(e)}"
        )
