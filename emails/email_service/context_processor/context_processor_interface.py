from typing import Any, Protocol


class EmailContextProcessorInterface(Protocol):
    @staticmethod
    def get_context() -> dict[Any, Any]:
        raise NotImplementedError()

    def confirm_email(self, user) -> dict[Any, Any]:
        raise NotImplementedError()

    def reset_password(self, user) -> dict[Any, Any]:
        raise NotImplementedError()
