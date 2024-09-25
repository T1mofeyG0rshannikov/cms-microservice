from domain.user_sessions.repository import UserSessionRepositoryInterface
from web.site_statistics.models import UserAction, UserActivity


class UserSessionRepository(UserSessionRepositoryInterface):
    def create_user_action(self, adress: str, text: str, session_unique_key: str) -> None:
        UserAction.objects.create(
            adress=adress,
            text=text,
            session=UserActivity.objects.get(unique_key=session_unique_key),
        )


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
