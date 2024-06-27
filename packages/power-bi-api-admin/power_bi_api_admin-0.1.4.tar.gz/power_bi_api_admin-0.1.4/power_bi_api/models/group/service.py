import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.group.urls import endpoint


class GroupService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_group_users(self, group_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-group-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified workspace.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{group_id}/users"), method="get"
            )
        )
        return response

    def get_groups(
        self, top: int = None, skip: int = None, filter: str = None, expand: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-groups-as-admin
        \nReturn:\n
        A list of workspaces for the organization.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response

    def get_group(self, group_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-group-as-admin
        \nReturn:\n
        A workspace for the organization.
        """

        response = asyncio.run(
            self.__base_request.request(endpoint=endpoint(group_id), method="get")
        )
        return response

    def get_unused_artifacts(self, group_id):
        """
        API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/groups-get-unused-artifacts-as-admin
        \nReturn:\n
        A list of datasets, reports, and dashboards that have not been used within 30 days for the specified workspace. This is a preview API call.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{group_id}/unused"), method="get"
            )
        )
        return response
