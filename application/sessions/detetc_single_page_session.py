from domain.user_sessions.repository import UserSessionRepositoryInterface


class DetectSinglePageSession:
    def __init__(self, user_session_repository: UserSessionRepositoryInterface) -> None:
        self.user_session_repository = user_session_repository

    def __call__(self) -> None:
        penalty = self.user_session_repository.get_no_cookie_penalty()

        self.user_session_repository.add_penalty_to_single_page_session(penalty)

        limit = self.user_session_repository.get_ban_limit()
        self.user_session_repository.delete_hacking_visitors(limit)
