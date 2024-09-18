from typing import Protocol


class AdminLogRepositoryInterface(Protocol):
    @staticmethod
    def create_logg(ip: str, login: str) -> None:
        raise NotImplementedError()
