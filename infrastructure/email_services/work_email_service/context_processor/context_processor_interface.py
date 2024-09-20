from typing import Any, Protocol


class WorkEmailContextProcessorInterface(Protocol):
    def try_login_in_admin(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError()

    def login_in_fake_admin(self, **kwargs) -> dict[str, Any]:
        raise NotImplementedError()
