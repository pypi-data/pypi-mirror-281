from power_bi_api.models.activity.service import ActivityService


class ActivityController:
    def __init__(self, access_token: str) -> None:
        self.__service = ActivityService(access_token)

    def get_activity_events(
        self, startDateTime: str = None, endDateTime: str = None, filter: str = None
    ):
        return self.__service.get_activity_events(startDateTime, endDateTime, filter)
