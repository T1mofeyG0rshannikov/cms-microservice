from typing import Any, Protocol

from domain.user_sessions.session import UserSessionInterface


class UserSessionRepositoryInterface(Protocol):
    def create_user_action(self, adress: str, text: str, session_unique_key: str) -> None:
        raise NotImplementedError

    def update_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        raise NotADirectoryError

    def get_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> UserSessionInterface:
        raise NotADirectoryError

    def update_or_create_raw_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        raise NotADirectoryError
