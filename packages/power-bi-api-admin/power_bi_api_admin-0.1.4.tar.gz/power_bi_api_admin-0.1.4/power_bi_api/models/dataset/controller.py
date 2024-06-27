from power_bi_api.models.dataset.service import DatasetService


class DatasetController:
    def __init__(self, access_token: str) -> None:
        self.__service = DatasetService(access_token)

    def get_datasets_to_dataflows_linked_in_group(self, group_id):
        return self.__service.get_datasets_to_dataflows_linked_in_group(
            group_id=group_id
        )

    def get_dataset_users(self, dataset_id):
        return self.__service.get_dataset_users(dataset_id=dataset_id)

    def get_datasets(self, top: int = None, skip: int = None, filter: str = None):
        return self.__service.get_datasets(top=top, skip=skip, filter=filter)

    def get_datasets_in_group(
        self,
        group_id,
        top: int = None,
        skip: int = None,
        expand: str = None,
        filter: str = None,
    ):
        return self.__service.get_datasets_in_group(
            group_id=group_id, top=top, skip=skip, expand=expand, filter=filter
        )

    def get_dataset_datasources(self, dataset_id):
        return self.__service.get_dataset_datasources(dataset_id=dataset_id)
