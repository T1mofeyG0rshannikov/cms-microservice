from domain.email.repository import SystemRepositoryInterface
from infrastructure.persistence.models.admin import AdminLoginCode
from infrastructure.persistence.models.system.codes import ConfirmPhoneCode
from infrastructure.persistence.models.system.email import Email


class SystemRepository(SystemRepositoryInterface):
    def get_system_emails(self) -> list[str]:
        return list(Email.objects.values_list("email", flat=True).all())

    def update_or_create_admin_code(self, email: str, code: int) -> int:
        admin_code, _ = AdminLoginCode.objects.update_or_create(email=email, defaults={"code": code})

        return admin_code.code

    def code_exists(self, email: str, code: int) -> bool:
        return AdminLoginCode.objects.filter(email=email, code=code).exists()

    def delete_user_code(self, email: str) -> None:
        AdminLoginCode.objects.filter(email=email).delete()

    def create_user_confirm_phone_code(self, user_id: int, code: str) -> None:
        ConfirmPhoneCode.objects.create(user_id=user_id, code=code)

    def get_user_confirm_phone_code(self, user_id: int) -> str:
        return ConfirmPhoneCode.objects.get(user_id=user_id).code

    def delete_user_confirm_phone_code(self, user_id: int) -> None:
        ConfirmPhoneCode.objects.get(user_id=user_id).delete()

    def update_or_create_confirm_phone_code(self, user_id: int, code: str, phone: str) -> str:
        code, _ = ConfirmPhoneCode.objects.update_or_create(user_id=user_id, defaults={"code": code, "phone": phone})

        return code.code


def get_system_repository() -> SystemRepositoryInterface:
    return SystemRepository()
