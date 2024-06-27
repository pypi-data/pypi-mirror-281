import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.pbi_import.urls import endpoint


class ImportService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_imports(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/imports-get-imports-as-admin
        \nReturn:\n
        A list of imports for the organization.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response
