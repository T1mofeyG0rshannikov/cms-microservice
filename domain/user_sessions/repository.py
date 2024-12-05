from collections.abc import Iterable
from typing import Any, Protocol

from domain.user_sessions.session import SessionInterface, UserSessionInterface
from domain.user_sessions.session_filters import SessionFIltersHeader
from infrastructure.persistence.models.site_statistics import SessionFilters


class UserSessionRepositoryInterface(Protocol):
    def create_searcher_log(self, fields: dict[str, Any]) -> None:
        raise NotImplementedError

    def create_user_session(self, fields: dict[str, Any]) -> UserSessionInterface:
        raise NotImplementedError

    def is_user_session_exists_by_id(self, user_session_id: int) -> bool:
        raise NotImplementedError

    def update_user_session(self, session_id: int, fields: dict[str, Any]) -> None:
        raise NotImplementedError

    def create_user_action(self, adress: str, text: str, session_id: int) -> None:
        raise NotImplementedError

    def delete_user_session(self, session_id: int) -> None:
        raise NotImplementedError

    def create_raw_session(self, fields: dict[str, Any]) -> SessionInterface:
        raise NotImplementedError

    def is_raw_session_exists_by_id(self, session_id: int) -> bool:
        raise NotImplementedError

    def update_or_create_user_session(self, session_data: dict[str, Any]) -> None:
        raise NotImplementedError

    def get_or_create_user_session(self, session_data: dict[str, Any]) -> UserSessionInterface:
        raise NotImplementedError

    def get_searchers(self) -> str:
        raise NotImplementedError

    def get_no_cookie_penalty(self) -> int:
        raise NotImplementedError

    def add_penalty_to_single_page_session(self, penalty: int) -> None:
        raise NotImplementedError

    def get_ban_limit(self) -> int:
        raise NotImplementedError

    def delete_hacking_visitors(self) -> None:
        raise NotImplementedError

    def bulk_create_raw_session_logs(self, logs) -> None:
        raise NotImplementedError

    def get_disallowed_host_penalty(self) -> int:
        raise NotImplementedError

    def change_ban_rate(self, session_id: int, penalty: int) -> None:
        raise NotImplementedError

    def create_searcher(self, fields: dict[str, Any]) -> UserSessionInterface:
        raise NotImplementedError

    def is_searcher_exists_by_id(self, session_id: int) -> bool:
        raise NotImplementedError

    def get_page_not_found_penalty(self) -> int:
        raise NotImplementedError

    def get_raw_session(self, session_id: int) -> SessionInterface:
        raise NotImplementedError

    def update_raw_session(self, session_id: int, fields: dict[str, Any]) -> None:
        raise NotImplementedError

    def get_session_filters(self) -> SessionFilters:
        raise NotImplementedError

    def get_session_filter_headers(self) -> Iterable[SessionFIltersHeader]:
        raise NotImplementedError

    def get_reject_capcha_penalty(self) -> int:
        raise NotImplementedError

    def get_success_capcha_increase(self) -> int:
        raise NotImplementedError

    def increment_user_session_field(self, session_id: int, session_field_name: str) -> None:
        raise NotImplementedError
