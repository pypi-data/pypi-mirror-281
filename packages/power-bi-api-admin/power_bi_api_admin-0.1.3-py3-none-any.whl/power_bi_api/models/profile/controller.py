from power_bi_api.models.profile.service import ProfileService


class ProfileController:
    def __init__(self, access_token: str) -> None:
        self.__service = ProfileService(access_token)

    def get_profiles(self, top: int = None, skip: int = None, filter: str = None):
        return self.__service.get_profiles(top=top, skip=skip, filter=filter)
