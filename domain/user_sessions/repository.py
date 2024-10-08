from typing import Any, Protocol

from domain.user_sessions.session import UserSessionInterface


class UserSessionRepositoryInterface(Protocol):
    def create_user_action(self, adress: str, text: str, session_id: int) -> None:
        raise NotImplementedError

    def update_or_create_user_session(self, session_data: dict[str, Any]) -> None:
        raise NotADirectoryError

    def get_or_create_user_session(self, session_data: dict[str, Any]) -> UserSessionInterface:
        raise NotADirectoryError
