from power_bi_api.models.capacity.service import CapacityService


class CapacityController:
    def __init__(self, access_token: str) -> None:
        self.__service = CapacityService(access_token)

    def get_capacity_users(self, capacity_id, tenant_id: str = None):
        return self.__service.get_capacity_users(
            capacity_id=capacity_id, tenant_id=tenant_id
        )

    def get_capacities(self):
        return self.__service.get_capacities()
