from power_bi_api.models.group.service import GroupService


class GroupController:
    def __init__(self, access_token: str) -> None:
        self.__service = GroupService(access_token)

    def get_group_users(self, group_id):
        return self.__service.get_group_users(group_id=group_id)

    def get_groups(
        self,
        top: int = 5000,
        skip: int = None,
        filter: str = None,
        expand: str = "users, reports, dashboards, datasets, dataflows, workbooks",
    ):
        return self.__service.get_groups(
            top=top, skip=skip, filter=filter, expand=expand
        )

    def get_group(self, group_id):
        return self.__service.get_group(group_id=group_id)

    def get_unused_artifacts(self, group_id):
        return self.__service.get_unused_artifacts(group_id=group_id)
