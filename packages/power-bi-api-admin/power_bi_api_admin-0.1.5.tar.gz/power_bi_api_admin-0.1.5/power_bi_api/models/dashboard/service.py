import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.dashboard.urls import endpoint, endpoint_group


class DashboardService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_dashboard_subscriptions(self, dashboard_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboard-subscriptions-as-admin
        \nReturn:\n
        A list of dashboard subscriptions along with subscriber details. This is a preview API call.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dashboard_id}/subscriptions"), method="get"
            )
        )
        return response

    def get_dashboard_users(self, dashboard_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboard-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified dashboard.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dashboard_id}/users"), method="get"
            )
        )
        return response

    def get_dashboards(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboards-as-admin
        \nReturn:\n
        A list of dashboards for the organization.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response

    def get_dashboards_in_group(
        self,
        group_id,
        top: int = None,
        skip: int = None,
        expand: str = None,
        filter: str = None,
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboards-in-group-as-admin
        \nReturn:\n
        A list of dashboards from the specified workspace.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/dashboards"),
                method="get",
                parameters=parameters,
            )
        )
        return response

    def get_dashboard_tiles(self, dashboard_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-tiles-as-admin
        \nReturn:\n
        A list of tiles within the specified dashboard.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dashboard_id}/tiles"), method="get"
            )
        )
        return response
