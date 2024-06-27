import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.pipeline.urls import endpoint


class PipelineService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_pipeline_users(self, pipeline_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/pipelines-get-pipeline-users-as-admin
        \nReturn:\n
        A list of users that have access to a specified deployment pipeline.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{pipeline_id}/users"), method="get"
            )
        )
        return response

    def get_pipelines(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/pipelines-get-pipelines-as-admin
        \nReturn:\n
        A list of deployment pipelines for the organization.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response
