from power_bi_api.models.pipeline.service import PipelineService


class PipelineController:
    def __init__(self, access_token: str) -> None:
        self.__service = PipelineService(access_token)

    def get_pipeline_users(self, pipeline_id):
        return self.__service.get_pipeline_users(pipeline_id=pipeline_id)

    def get_pipelines(
        self, top: int = None, skip: int = None, expand: str = None, filter: str = None
    ):
        return self.__service.get_pipelines()
