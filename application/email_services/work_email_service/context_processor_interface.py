from typing import Any, Protocol

from domain.user.entities import UserInterface


class WorkEmailContextProcessorInterface(Protocol):
    def login_in_fake_admin(self, user: UserInterface, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    def error_message(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    def login_code(self, code: int, **kwargs) -> dict[str, Any]:
        raise NotImplementedError
