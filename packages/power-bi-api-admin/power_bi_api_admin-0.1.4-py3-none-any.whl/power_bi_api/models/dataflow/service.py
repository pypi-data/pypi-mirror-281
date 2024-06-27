import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.dataflow.urls import endpoint, endpoint_group


class DataflowService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_dataflow_datasources(self, dataflow_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dataflows-get-dataflow-datasources-as-admin
        \nReturn:\n
        A a list of data sources for the specified dataflow.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dataflow_id}/datasources"), method="get"
            )
        )
        return response

    def get_dataflow_users(self, dataflow_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dataflows-get-dataflow-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified dataflow.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dataflow_id}/users"), method="get"
            )
        )
        return response

    def get_dataflows(self, top: int = None, skip: int = None, filter: str = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dataflows-get-dataflows-as-admin
        \nReturn:\n
        A list of dataflows for the organization.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response

    def get_dataflows_in_group(
        self, group_id, top: int = None, skip: int = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dataflows-get-dataflows-in-group-as-admin
        \nReturn:\n
        A a list of dataflows from the specified workspace.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/dataflows"),
                method="get",
                parameters=parameters,
            )
        )
        return response

    def get_upstream_dataflows_in_group(self, group_id, dataflow_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dataflows-get-upstream-dataflows-in-group-as-admin
        \nReturn:\n
        A list of upstream dataflows for the specified dataflow.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/dataflows/{dataflow_id}"),
                method="get",
            )
        )
        return response
