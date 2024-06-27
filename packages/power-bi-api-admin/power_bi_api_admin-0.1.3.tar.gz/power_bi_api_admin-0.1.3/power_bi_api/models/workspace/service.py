import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.workspace.urls import endpoint


class WorkspaceService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_modified_workspaces(
        self,
        excludeInActiveWorkspaces: bool = True,
        excludePersonalWorkspaces: bool = True,
        modifiedSince: str = None,
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-modified-workspaces
        \nReturn:\n
        A list of workspace IDs in the organization.
        """
        parameters = {
            "excludeInActiveWorkspaces": excludeInActiveWorkspaces,
            "excludePersonalWorkspaces": excludePersonalWorkspaces,
            "modifiedSince": modifiedSince,
        }
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint("modified"), method="get", parameters=parameters
            )
        )
        return response

    def get_workspaces_info(
        self,
        workspaces: list,
        datasetExpressions: bool = True,
        datasetSchema: bool = True,
        datasourceDetails: bool = True,
        getArtifactUsers: bool = True,
        lineage: bool = True,
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info
        \nReturn:\n
        The metadata for the requested list of workspaces.
        """
        workspaces = {
            "workspaces": workspaces
        }
        parameters = {
            "datasetExpressions": datasetExpressions,
            "datasetSchema": datasetSchema,
            "datasourceDetails": datasourceDetails,
            "getArtifactUsers": getArtifactUsers,
            "lineage": lineage,
        }
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint("getInfo"),
                method="post",
                json=workspaces,
                parameters=parameters,
            )
        )
        return response

    def get_scan_result(self, scan_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result
        \nReturn:\n
        A scan result for the specified scan.
        Only make this API call after a successful GetScanStatus API call. The scan result will remain available for 24 hours.
        """
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"scanResult/{scan_id}"), method="get"
            )
        )
        return response

    def get_scan_status(self, scan_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-status
        \nReturn:\n
        A scan status for the specified scan.
        """
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"scanStatus/{scan_id}"), method="get"
            )
        )
        return response
