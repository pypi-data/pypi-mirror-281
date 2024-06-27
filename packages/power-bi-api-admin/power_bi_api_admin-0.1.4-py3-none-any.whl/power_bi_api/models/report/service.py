import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.report.urls import endpoint, endpoint_group


class ReportService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_report_subscriptions(self, report_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-report-subscriptions-as-admin
        \nReturn:\n
        A list of report subscriptions along with subscriber details. This is a preview API call.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{report_id}/subscriptions"), method="get"
            )
        )
        return response

    def get_report_users(self, report_id):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-report-users-as-admin
        \nReturn:\n
        A list of users that have access to the specified report.
        """

        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(f"{report_id}/users"), method="get"
            )
        )
        return response

    def get_reports(self, top: int = None, skip: int = None, filter: str = None):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-reports-as-admin
        \nReturn:\n
        A list of reports for the organization.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint(), method="get", parameters=parameters
            )
        )
        return response

    def get_reports_in_group(
        self, group_id, top: int = None, skip: int = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-reports-in-group-as-admin
        \nReturn:\n
        A list of reports from the specified workspace.
        """
        parameters = {"$top": top, "$skip": skip, "$filter": filter}
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint_group(f"{group_id}/reports"),
                method="get",
                parameters=parameters,
            )
        )
        return response
