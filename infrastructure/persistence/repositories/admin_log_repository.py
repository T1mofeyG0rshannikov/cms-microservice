from web.site_statistics.models import TryLoginToAdminPanel


class AdminLogRepository:
    @staticmethod
    def create_logg(ip: str, login: str) -> None:
        TryLoginToAdminPanel.objects.create(client_ip=ip, login=login)


def get_admin_log_repository():
    return AdminLogRepository()
