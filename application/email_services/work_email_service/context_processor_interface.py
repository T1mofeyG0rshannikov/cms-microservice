from typing import Any, Protocol


class WorkEmailContextProcessorInterface(Protocol):
    def login_in_fake_admin(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    def error_message(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    def login_code(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError
