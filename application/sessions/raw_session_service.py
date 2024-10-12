from typing import Protocol

from application.sessions.dto import RawSessionDB, RawSessionDTO


class RawSessionServiceInterface(Protocol):
    def get_initial_raw_session(self, path: str, site: str, device: bool) -> RawSessionDB:
        raise NotImplementedError

    def filter_sessions(self, session_data: RawSessionDTO, host: str, page_adress: str, port: str) -> RawSessionDTO:
        raise NotImplementedError

    def success_capcha(self, session_id: int) -> None:
        raise NotImplementedError
