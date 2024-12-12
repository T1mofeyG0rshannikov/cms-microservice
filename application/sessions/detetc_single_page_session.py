from domain.user_sessions.repositories.raw_session_repository import (
    RawSessionRepositoryInterface,
)
from domain.user_sessions.repository import UserSessionRepositoryInterface


class DetectSinglePageSession:
    def __init__(
        self,
        user_session_repository: UserSessionRepositoryInterface,
        raw_session_repository: RawSessionRepositoryInterface,
    ) -> None:
        self.user_session_repository = user_session_repository
        self.raw_session_repository = raw_session_repository

    def __call__(self) -> None:
        penalty = self.user_session_repository.get_no_cookie_penalty()

        self.raw_session_repository.add_penalty_to_single_page_session(penalty)

        limit = self.user_session_repository.get_ban_limit()
        self.user_session_repository.delete_hacking_visitors(limit)
