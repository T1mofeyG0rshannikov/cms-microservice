from domain.email.repository import SystemRepositoryInterface
from web.system.models import Email


class SystemRepository(SystemRepositoryInterface):
    @staticmethod
    def get_system_emails():
        return list(Email.objects.values_list("email", flat=True).all())


def get_system_repository() -> SystemRepositoryInterface:
    return SystemRepository()
