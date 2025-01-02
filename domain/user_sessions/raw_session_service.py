from typing import Protocol

from domain.user_sessions.session import SessionInterface


class RawSessionServiceInterface(Protocol):
    def filter_sessions(
        self, session_data: SessionInterface, host: str, path: str, port: str, session_id: int
    ) -> tuple[int, bool, bool]:
        raise NotImplementedError

    def success_capcha(self, session: SessionInterface) -> None:
        raise NotImplementedError

    def create(self, device: bool) -> SessionInterface:
        raise NotImplementedError
