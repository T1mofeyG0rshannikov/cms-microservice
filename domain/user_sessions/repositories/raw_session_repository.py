from typing import Protocol

from domain.user_sessions.session import SessionInterface


class RawSessionRepositoryInterface(Protocol):
    def create(self, **kwargs) -> SessionInterface:
        raise NotImplementedError

    def is_exists_by_id(self, session_id: int) -> bool:
        raise NotImplementedError

    def add_penalty_to_single_page_session(self, penalty: int) -> None:
        raise NotImplementedError

    def bulk_create_logs(self, logs) -> None:
        raise NotImplementedError

    def change_ban_rate(self, session_id: int, penalty: int) -> None:
        raise NotImplementedError

    def get(self, session_id: int) -> SessionInterface:
        raise NotImplementedError

    def update(self, id: int, **kwargs) -> None:
        raise NotImplementedError
