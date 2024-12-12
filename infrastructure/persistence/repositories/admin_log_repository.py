from domain.logging.admin import AdminLogRepositoryInterface
from infrastructure.persistence.models.site_statistics import (
    TryLoginToAdminPanel,
    TryLoginToFakeAdminPanel,
)


class AdminLogRepository(AdminLogRepositoryInterface):
    def create_logg(self, client_ip: str, login: str):
        return TryLoginToAdminPanel.objects.create(client_ip=client_ip, login=login)

    def create_logg_fake_admin(self, ip: str, login: str):
        return TryLoginToFakeAdminPanel.objects.create(client_ip=ip, login=login)


def get_admin_log_repository() -> AdminLogRepositoryInterface:
    return AdminLogRepository()
