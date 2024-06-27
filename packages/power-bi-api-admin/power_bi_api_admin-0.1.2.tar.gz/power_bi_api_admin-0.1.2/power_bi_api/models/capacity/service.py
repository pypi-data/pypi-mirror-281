import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.capacity.urls import endpoint


class CapacityService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_capacity_users(self, capacity_id, tenant_id: str = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/capacities-get-capacity-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified workspace.
        """
        parameters = {"tenantId": tenant_id}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{capacity_id}/users"),
                method="get",
                parameters=parameters,
            )
        )
        return response

    def get_capacities(self):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/get-capacities-as-admin
        \nReturn:\n
        A list of users that have access to the specified workspace.
        """
        response = asyncio.run(
            self.__base_request.request(endpoint=endpoint(), method="get")
        )
        return response
