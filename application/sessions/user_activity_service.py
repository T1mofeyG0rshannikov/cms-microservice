from django.utils.timezone import now

from application.sessions.dto import UserSessionDB
from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import UserSessionInterface
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)


class UserActivitySessionService:
    def __init__(self, user_session_repository: UserSessionRepositoryInterface) -> None:
        self.user_session_repository = user_session_repository

    def get_initial_data(self, session_id: int, user_id: int | None = None, auth: str | None = None) -> UserSessionDB:
        if not auth:
            auth = "login" if user_id else None

        return UserSessionDB(
            start_time=now().isoformat(),
            user_id=user_id,
            auth=auth,
            session_id=session_id,
        )

    def create(self, user_id: int, session_id: int) -> UserSessionInterface:
        session_data = self.get_initial_data(
            user_id=user_id,
            session_id=session_id,
        )

        return self.user_session_repository.create(**session_data.__dict__)


def get_user_session_service(
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository(),
) -> UserActivitySessionService:
    return UserActivitySessionService(user_session_repository=user_session_repository)
