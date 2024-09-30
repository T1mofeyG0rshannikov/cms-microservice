from domain.logging.admin import AdminLogRepositoryInterface
from infrastructure.persistence.models.site_statistics import (
    TryLoginToAdminPanel,
    TryLoginToFakeAdminPanel,
)


class AdminLogRepository(AdminLogRepositoryInterface):
    @staticmethod
    def create_logg(ip: str, **kwargs):
        return TryLoginToAdminPanel.objects.create(client_ip=ip, login=kwargs.get("username"))

    @staticmethod
    def create_logg_fake_admin(ip: str, **kwargs):
        return TryLoginToFakeAdminPanel.objects.create(client_ip=ip, login=kwargs.get("username"))


def get_admin_log_repository() -> AdminLogRepositoryInterface:
    return AdminLogRepository()
