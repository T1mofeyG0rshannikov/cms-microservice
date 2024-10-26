from typing import Protocol


class SystemRepositoryInterface(Protocol):
    def get_system_emails(self) -> list[str]:
        raise NotImplementedError()
