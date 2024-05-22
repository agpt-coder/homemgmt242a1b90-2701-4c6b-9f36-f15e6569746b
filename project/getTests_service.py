import prisma
import prisma.models
from pydantic import BaseModel


class test(BaseModel):
    """
    Hello
    """

    test: str


async def getTests() -> test:
    """
    Retrieves a predefined test message stored in a test class.

    This function queries the 'prisma.models.Service' table to retrieve service details, ensuring the installation
    command matches 'pip install HomeAssistant-API' and then returns the data encapsulated in a 'test' class.
    It's designed to integrate with an application that interfaces with home automation systems.

    Args:
        None

    Returns:
        test: An object of the test class containing a test string.

    Example:
        getTests()
        > test(test='First retrieved installation command: pip install HomeAssistant-API')
    """
    service = await prisma.models.Service.prisma().find_first(
        where={"installationCmd": "pip install HomeAssistant-API"}
    )
    if service is None:
        return test(test="No matching service found.")
    return test(test=f"First retrieved installation command: {service.installationCmd}")
