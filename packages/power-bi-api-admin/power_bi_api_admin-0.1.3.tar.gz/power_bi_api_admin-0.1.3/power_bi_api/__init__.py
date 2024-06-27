from power_bi_api.helpers.auth import Auth
from power_bi_api.models.activity.controller import ActivityController
from power_bi_api.models.app.controller import AppController
from power_bi_api.models.capacity.controller import CapacityController
from power_bi_api.models.dashboard.controller import DashboardController
from power_bi_api.models.dataflow.controller import DataflowController
from power_bi_api.models.dataset.controller import DatasetController
from power_bi_api.models.group.controller import GroupController
from power_bi_api.models.pbi_import.controller import ImportController
from power_bi_api.models.pipeline.controller import PipelineController
from power_bi_api.models.profile.controller import ProfileController
from power_bi_api.models.report.controller import ReportController
from power_bi_api.models.user.controller import UserController
from power_bi_api.models.workspace.controller import WorkspaceController


class PowerBiApp:
    def __init__(self) -> None:
        self.authenticator = Auth()

    @property
    def activity(self):
        return ActivityController(self.authenticator.access_token)

    @property
    def app(self):
        return AppController(self.authenticator.access_token)

    @property
    def capacity(self):
        return CapacityController(self.authenticator.access_token)

    @property
    def dashboard(self):
        return DashboardController(self.authenticator.access_token)

    @property
    def dataflow(self):
        return DataflowController(self.authenticator.access_token)

    @property
    def dataset(self):
        return DatasetController(self.authenticator.access_token)

    @property
    def group(self):
        return GroupController(self.authenticator.access_token)

    @property
    def pbi_import(self):
        return ImportController(self.authenticator.access_token)

    @property
    def pipeline(self):
        return PipelineController(self.authenticator.access_token)

    @property
    def profile(self):
        return ProfileController(self.authenticator.access_token)

    @property
    def report(self):
        return ReportController(self.authenticator.access_token)

    @property
    def user(self):
        return UserController(self.authenticator.access_token)

    @property
    def workspace(self):
        return WorkspaceController(self.authenticator.access_token)
