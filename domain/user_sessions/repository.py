from collections.abc import Iterable
from typing import Protocol

from domain.user_sessions.session import UserSessionInterface
from domain.user_sessions.session_filters import (
    SessionFIltersHeader,
    SessionFiltersInterface,
)


class UserSessionRepositoryInterface(Protocol):
    def get(self, id: int) -> UserSessionInterface | None:
        raise NotImplementedError

    def create_searcher_log(self, **kwargs) -> None:
        raise NotImplementedError

    def create(self, **kwargs) -> UserSessionInterface:
        raise NotImplementedError

    def update(self, session: UserSessionInterface) -> UserSessionInterface:
        raise NotImplementedError

    def create_user_action(self, adress: str, text: str, session_id: int) -> None:
        raise NotImplementedError

    def delete_user_session(self, session_id: int) -> None:
        raise NotImplementedError

    def get_searchers(self) -> str:
        raise NotImplementedError

    def get_no_cookie_penalty(self) -> int:
        raise NotImplementedError

    def get_ban_limit(self) -> int:
        raise NotImplementedError

    def delete_hacking_visitors(self, ban_limit: int) -> None:
        raise NotImplementedError

    def get_disallowed_host_penalty(self) -> int:
        raise NotImplementedError

    def create_searcher(self, **kwargs) -> int:
        raise NotImplementedError

    def is_searcher_exists_by_id(self, session_id: int) -> bool:
        raise NotImplementedError

    def get_page_not_found_penalty(self) -> int:
        raise NotImplementedError

    def get_session_filters(self) -> SessionFiltersInterface:
        raise NotImplementedError

    def get_session_filter_headers(self) -> Iterable[SessionFIltersHeader]:
        raise NotImplementedError

    def get_reject_capcha_penalty(self) -> int:
        raise NotImplementedError

    def get_success_capcha_increase(self) -> int:
        raise NotImplementedError

    def increment_user_session_field(self, session_id: int, session_field_name: str) -> None:
        raise NotImplementedError
