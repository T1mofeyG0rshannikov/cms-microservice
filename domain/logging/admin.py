from typing import Protocol


class AdminLogRepositoryInterface(Protocol):
    def create_logg(self, ip: str, login: str) -> None:
        raise NotImplementedError
