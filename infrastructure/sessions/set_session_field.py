from typing import Any

from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import SessionInterface


class SetSessionField:
    def __init__(self, repository: UserSessionRepositoryInterface, session_key: str) -> None:
        self.user_session_repository = repository
        self.session_key = session_key

    def __call__(self, session: SessionInterface, session_field: str, value: Any) -> None:
        session[self.session_key][session_field] = value
        session.save()

        self.user_session_repository.update_or_create_user_session(
            unique_key=session[self.session_key]["unique_key"], session_data=session[self.session_key]
        )
