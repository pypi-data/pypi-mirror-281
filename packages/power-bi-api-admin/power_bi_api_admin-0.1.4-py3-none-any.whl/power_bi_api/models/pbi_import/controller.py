from power_bi_api.models.pbi_import.service import ImportService


class ImportController:
    def __init__(self, access_token: str) -> None:
        self.__service = ImportService(access_token)

    def get_imports(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        return self.__service.get_imports(
            top=top, skip=skip, expand=expand, filter=filter
        )
