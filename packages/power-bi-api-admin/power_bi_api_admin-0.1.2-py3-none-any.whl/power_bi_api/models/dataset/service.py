import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.dataset.urls import endpoint, endpoint_group


class DatasetService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_datasets_to_dataflows_linked_in_group(self, group_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-dataset-to-dataflows-links-in-group-as-admin
        \nReturn:\n
        A list of upstream dataflows for datasets from the specified workspace.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/datasets/upstreamDataflows"),
                method="get",
            )
        )
        return response

    def get_dataset_users(self, dataset_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-dataset-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified dataset.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dataset_id}/users"), method="get"
            )
        )
        return response

    def get_datasets(self, top: int = None, skip: int = None, filter: str = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-datasets-as-admin
        \nReturn:\n
        A list of datasets for the organization.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response

    def get_datasets_in_group(
        self,
        group_id,
        top: int = None,
        skip: int = None,
        expand: str = None,
        filter: str = None,
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-datasets-in-group-as-admin
        \nReturn:\n
        A list of datasets from the specified workspace.
        """
        parameters = {"$top": top, "$expand": expand, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/datasets"),
                method="get",
                parameters=parameters,
            )
        )
        return response

    def get_dataset_datasources(self, dataset_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/datasets-get-datasources-as-admin
        \nReturn:\n
        A list of data sources for the specified dataset.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{dataset_id}/datasources"), method="get"
            )
        )
        return response
