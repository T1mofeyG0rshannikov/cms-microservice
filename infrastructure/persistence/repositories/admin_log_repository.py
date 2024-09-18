from domain.logging.admin import AdminLogRepositoryInterface
from web.site_statistics.models import TryLoginToAdminPanel


class AdminLogRepository(AdminLogRepositoryInterface):
    @staticmethod
    def create_logg(ip: str, **kwargs) -> None:
        TryLoginToAdminPanel.objects.create(client_ip=ip, login=kwargs.get("username"))


def get_admin_log_repository() -> AdminLogRepositoryInterface:
    return AdminLogRepository()
