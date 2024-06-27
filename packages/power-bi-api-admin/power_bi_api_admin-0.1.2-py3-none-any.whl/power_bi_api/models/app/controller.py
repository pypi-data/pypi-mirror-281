from power_bi_api.models.app.service import AppService


class AppController:
    def __init__(self, access_token: str) -> None:
        self.__service = AppService(access_token)

    def get_apps(self, top: int = 100, skip: int = None):
        return self.__service.get_apps(top=top, skip=skip)

    def get_app_users(self, app_id):
        return self.__service.get_app_users(app_id)
