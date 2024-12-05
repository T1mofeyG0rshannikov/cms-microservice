from typing import Protocol


class SystemRepositoryInterface(Protocol):
    def get_system_emails(self) -> list[str]:
        raise NotImplementedError

    def update_or_create_admin_code(self, email: str, code: int) -> int:
        raise NotImplementedError
