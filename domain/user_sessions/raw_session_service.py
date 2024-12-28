from typing import Protocol

from domain.user_sessions.session import SessionInterface


class RawSessionServiceInterface(Protocol):
    def get_initial_raw_session(self, device: bool) -> SessionInterface:
        raise NotImplementedError

    def filter_sessions(
        self, session_data: SessionInterface, host: str, path: str, port: str, session_id: int
    ) -> SessionInterface:
        raise NotImplementedError

    def success_capcha(self, session_id: int) -> None:
        raise NotImplementedError
