from typing import Protocol

from domain.logging.log import LogInterface


class AdminLogRepositoryInterface(Protocol):
    def create_logg(self, client_ip: str, login: str) -> LogInterface:
        raise NotImplementedError

    def create_logg_fake_admin(self, ip: str, login: str) -> LogInterface:
        raise NotImplementedError
