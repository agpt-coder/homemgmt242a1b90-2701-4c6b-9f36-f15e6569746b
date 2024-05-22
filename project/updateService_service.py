from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateServiceResponse(BaseModel):
    """
    Response model confirming successful update of the service.
    """

    success: bool
    serviceId: int
    message: str


async def updateService(
    serviceId: int, serviceName: Optional[str], installationCmd: Optional[str]
) -> UpdateServiceResponse:
    """
    Provides functionality for updating an existing service's details. Only accessible by admins, this endpoint expects a
    service ID as part of the URL, and updates the specific service data.

    Args:
        serviceId (int): The identifier of the service to be updated.
        serviceName (Optional[str]): New name for the service, if it needs to be updated.
        installationCmd (Optional[str]): The command used to install or update the service, if it needs an update.

    Returns:
        UpdateServiceResponse: Response model confirming successful update of the service.

    Example:
        response = updateService(1, "New Name", "pip install service-kit")
        print(response.success) # True
        print(response.serviceId) # 1
        print(response.message) # "Service updated successfully."
    """
    try:
        service = await prisma.models.Service.prisma().find_unique(
            where={"id": serviceId}
        )
        if not service:
            return UpdateServiceResponse(
                success=False, serviceId=serviceId, message="Service not found."
            )
        update_data = {}
        if serviceName is not None:
            update_data["serviceName"] = serviceName
        if installationCmd is not None:
            update_data["installationCmd"] = installationCmd
        if update_data:
            await prisma.models.Service.prisma().update(
                where={"id": serviceId}, data=update_data
            )
        return UpdateServiceResponse(
            success=True, serviceId=serviceId, message="Service updated successfully."
        )
    except Exception as e:
        return UpdateServiceResponse(success=False, serviceId=serviceId, message=str(e))
