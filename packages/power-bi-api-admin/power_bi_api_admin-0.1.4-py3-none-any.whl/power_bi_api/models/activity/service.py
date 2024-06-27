import asyncio

from power_bi_api.helpers.https_base import HTTPRequest
from power_bi_api.models.activity.urls import endpoint


class ActivityService:
    def __init__(self, access_token: str) -> None:
        self.__base_request = HTTPRequest(access_token)

    def get_activity_events(
        self, startDateTime: str = None, endDateTime: str = None, filter: str = None
    ):
        """API Reference:
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/get-activity-events
        \nReturn:\n
        A list of audit activity events for a tenant.
        """
        # filter = "Activity eq 'viewreport'"
        parameters = {
            "startDateTime": startDateTime,
            "endDateTime": endDateTime,
            "$filter": filter,
        }
        audit = []
        total_request = 1
        response = asyncio.run(
            self.__base_request.request(
                endpoint=endpoint, method="get", parameters=parameters
            )
        )
        audit += response.get("activityEventEntities")
        while True:
            if not response.get("lastResultSet"):
                total_request += 1
                response = asyncio.run(
                    self.__base_request.request(
                        endpoint=response.get("continuationUri"),
                        method="get",
                        full_endpoint=True,
                    )
                )
                audit += response.get("activityEventEntities")
            else:
                break
        print(
            f"Total requests on the day {parameters['startDateTime']} : {total_request}"
        )
        return audit
