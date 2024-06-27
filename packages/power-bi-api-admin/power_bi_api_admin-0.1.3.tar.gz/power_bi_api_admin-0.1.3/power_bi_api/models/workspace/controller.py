from power_bi_api.models.workspace.service import WorkspaceService


class WorkspaceController:
    def __init__(self, access_token: str) -> None:
        self.__service = WorkspaceService(access_token)

    def get_modified_workspaces(
        self,
        excludeInActiveWorkspaces: bool = True,
        excludePersonalWorkspaces: bool = True,
        modifiedSince: str = None,
    ):
        return self.__service.get_modified_workspaces(
            excludeInActiveWorkspaces=excludeInActiveWorkspaces,
            excludePersonalWorkspaces=excludePersonalWorkspaces,
            modifiedSince=modifiedSince,
        )

    def get_workspaces_info(
        self,
        workspaces: list,
        datasetExpressions: bool = True,
        datasetSchema: bool = True,
        datasourceDetails: bool = True,
        getArtifactUsers: bool = True,
        lineage: bool = True,
    ):
        return self.__service.get_workspaces_info(
            workspaces=workspaces,
            datasetExpressions=datasetExpressions,
            datasetSchema=datasetSchema,
            datasourceDetails=datasourceDetails,
            getArtifactUsers=getArtifactUsers,
            lineage=lineage,
        )

    def get_scan_result(self, scan_id):
        return self.__service.get_scan_result(scan_id=scan_id)

    def get_scan_status(self, scan_id):
        return self.__service.get_scan_status(scan_id=scan_id)
