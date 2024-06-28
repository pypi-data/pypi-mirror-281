from power_bi_api.models.dashboard.service import DashboardService


class DashboardController:
    def __init__(self, access_token: str) -> None:
        self.__service = DashboardService(access_token)

    def get_dashboard_subscriptions(self, dashboard_id):
        return self.__service.get_dashboard_subscriptions(dashboard_id=dashboard_id)

    def get_dashboard_users(self, dashboard_id):
        return self.__service.get_dashboard_users(dashboard_id=dashboard_id)

    def get_dashboards(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        return self.__service.get_dashboards(
            top=top, skip=skip, expand=expand, filter=filter
        )

    def get_dashboards_in_group(
        self,
        group_id,
        top: int = None,
        skip: int = None,
        expand: str = None,
        filter: str = None,
    ):
        return self.__service.get_dashboards_in_group(
            group_id=group_id, top=top, skip=skip, expand=expand, filter=filter
        )

    def get_dashboard_tiles(self, dashboard_id):
        return self.__service.get_dashboard_tiles(dashboard_id=dashboard_id)
