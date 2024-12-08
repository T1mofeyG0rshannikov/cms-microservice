from typing import Any, Protocol

from domain.user.user import UserInterface


class EmailContextProcessorInterface(Protocol):
    @staticmethod
    def get_context() -> dict[str, Any]:
        raise NotImplementedError

    def confirm_email(self, user: UserInterface) -> dict[str, Any]:
        raise NotImplementedError

    def confirm_new_email(self, user: UserInterface) -> dict[str, Any]:
        raise NotImplementedError

    def reset_password(self, user: UserInterface) -> dict[str, Any]:
        raise NotImplementedError
