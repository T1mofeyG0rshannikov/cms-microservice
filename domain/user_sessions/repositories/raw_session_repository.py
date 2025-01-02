from typing import Protocol

from domain.user_sessions.session import SessionInterface


class RawSessionRepositoryInterface(Protocol):
    def create(self, **kwargs) -> SessionInterface:
        raise NotImplementedError

    def add_penalty_to_single_page_session(self, penalty: int) -> None:
        raise NotImplementedError

    def bulk_create_logs(self, logs) -> None:
        raise NotImplementedError

    def change_ban_rate(self, session_id: int, penalty: int) -> None:
        raise NotImplementedError

    def get(self, id: int) -> SessionInterface:
        raise NotImplementedError

    def update(self, session: SessionInterface, updated_fields: list[str] | None = None) -> SessionInterface:
        raise NotImplementedError
