from typing import Protocol


class SystemRepositoryInterface(Protocol):
    @staticmethod
    def get_system_emails() -> list[str]:
        raise NotImplementedError()
