from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import SessionInterface


class IncrementSessionCount:
    def __init__(self, repository: UserSessionRepositoryInterface, session_key: str, session_field: str) -> None:
        self.user_session_repository = repository
        self.session_key = session_key
        self.session_field = session_field

    def __call__(self, session: SessionInterface) -> None:
        session[self.session_key][self.session_field] += 1
        session.save()

        self.user_session_repository.update_or_create_user_session(
            unique_key=session[self.session_key]["unique_key"], session_data=session[self.session_key]
        )
