from power_bi_api.models.report.service import ReportService


class ReportController:
    def __init__(self, access_token: str) -> None:
        self.__service = ReportService(access_token)

    def get_report_subscriptions(self, report_id):
        return self.__service.get_report_subscriptions(report_id=report_id)

    def get_report_users(self, report_id):
        return self.__service.get_report_users(report_id=report_id)

    def get_reports(self, top: int = None, skip: int = None, filter: str = None):
        return self.__service.get_reports(top=top, skip=skip, filter=filter)

    def get_reports_in_group(
        self, group_id, top: int = None, skip: int = None, filter: str = None
    ):
        return self.__service.get_reports_in_group(
            group_id=group_id, top=top, skip=skip, filter=filter
        )
