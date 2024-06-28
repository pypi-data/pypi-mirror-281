import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.app.urls import endpoint


class AppService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_apps(self, top: int, skip: int = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/apps-get-apps-as-admin
        \nReturn:\n
        A list of apps in the organization.
        """
        parameters = {"$top": top, "$skip": skip}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=f"{endpoint()}", method="get", parameters=parameters
            )
        )
        return response

    def get_app_users(self, app_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/apps-get-app-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified app.
        """
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{app_id}/users"), method="get"
            )
        )
        return response
