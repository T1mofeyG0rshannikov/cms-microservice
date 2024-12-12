from typing import Protocol


class SystemRepositoryInterface(Protocol):
    def get_system_emails(self) -> list[str]:
        raise NotImplementedError

    def update_or_create_admin_code(self, email: str, code: int) -> int:
        raise NotImplementedError

    def update_or_create_confirm_phone_code(self, user_id: int, code: str, phone: str) -> str:
        raise NotImplementedError

    def get_user_confirm_phone_code(self, user_id: int) -> str:
        raise NotImplementedError

    def delete_user_confirm_phone_code(self, user_id: int) -> None:
        raise NotImplementedError
