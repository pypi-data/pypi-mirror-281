import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.profile.urls import endpoint


class ProfileService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_profiles(self, top: int = None, skip: int = None, filter: str = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/profiles-get-profiles-as-admin
        \nReturn:\n
        A list of service principal profiles for the organization.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response
