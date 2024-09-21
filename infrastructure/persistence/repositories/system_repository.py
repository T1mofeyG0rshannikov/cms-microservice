from domain.email.repository import SystemRepositoryInterface
from infrastructure.persistence.models.admin import AdminLoginCode
from infrastructure.persistence.models.system.email import Email


class SystemRepository(SystemRepositoryInterface):
    @staticmethod
    def get_system_emails():
        return list(Email.objects.values_list("email", flat=True).all())

    def update_or_create_admin_code(self, email: str, code: int) -> int:
        admin_code, _ = AdminLoginCode.objects.update_or_create(email=email, defaults={"code": code})

        return admin_code.code

    def code_exists(self, email: str, code: int) -> bool:
        return AdminLoginCode.objects.filter(email=email, code=code).exists()


def get_system_repository() -> SystemRepositoryInterface:
    return SystemRepository()
