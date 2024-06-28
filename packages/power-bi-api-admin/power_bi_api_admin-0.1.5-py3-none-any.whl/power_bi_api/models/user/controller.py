from power_bi_api.models.user.service import UserService


class UserController:
    def __init__(self, access_token: str) -> None:
        self.__service = UserService(access_token)

    def get_user_subscriptions(self, user_id):
        return self.__service.get_user_subscriptions(user_id=user_id)

    def get_user_artifact_access(self, user_id):
        return self.__service.get_user_artifact_access(user_id=user_id)
