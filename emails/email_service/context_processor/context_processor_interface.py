from typing import Any, Protocol

from user.user_interface import UserInterface


class EmailContextProcessorInterface(Protocol):
    @staticmethod
    def get_context() -> dict[Any, Any]:
        raise NotImplementedError()

    def confirm_email(self, user: UserInterface) -> dict[Any, Any]:
        raise NotImplementedError()

    def confirm_new_email(self, user: UserInterface) -> dict[Any, Any]:
        raise NotImplementedError()

    def reset_password(self, user: UserInterface) -> dict[Any, Any]:
        raise NotImplementedError()
