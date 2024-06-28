from power_bi_api.models.dataflow.service import DataflowService


class DataflowController:
    def __init__(self, access_token: str) -> None:
        self.__service = DataflowService(access_token)

    def get(
        self,
    ):
        return self.__service.get()

    def get_dataflow_datasources(self, dataflow_id):
        return self.__service.get_dataflow_datasources(dataflow_id=dataflow_id)

    def get_dataflow_users(self, dataflow_id):
        return self.__service.get_dataflow_users(dataflow_id=dataflow_id)

    def get_dataflows(self, top: int = None, skip: int = None, filter: str = None):
        return self.__service.get_dataflows(top=top, skip=skip, filter=filter)

    def get_dataflows_in_group(
        self, group_id, top: int = None, skip: int = None, filter: str = None
    ):
        return self.__service.get_dataflows_in_group(
            group_id=group_id, top=top, skip=skip, filter=filter
        )

    def get_upstream_dataflows_in_group(self, dataflow_id, group_id):
        return self.__service.get_upstream_dataflows_in_group(
            dataflow_id=dataflow_id, group_id=group_id
        )
