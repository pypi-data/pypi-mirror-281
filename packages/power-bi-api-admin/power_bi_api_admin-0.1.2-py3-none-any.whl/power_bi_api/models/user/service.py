import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.user.urls import endpoint


class UserService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_user_subscriptions(self, user_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/users-get-user-subscriptions-as-admin
        \nReturn:\n
        A list of subscriptions for the specified user. This is a preview API call.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{user_id}/subscriptions"), method="get"
            )
        )
        return response

    def get_user_artifact_access(self, user_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/users-get-user-artifact-access-as-admin
        \nReturn:\n
        A list of Power BI items (such as reports or dashboards) that the specified user has access to.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{user_id}/artifactAccess"), method="get"
            )
        )
        return response
