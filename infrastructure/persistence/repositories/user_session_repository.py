from typing import Any

from django.db.utils import OperationalError

from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import UserSessionInterface
from web.site_statistics.models import (
    SessionAction,
    SessionModel,
    UserAction,
    UserActivity,
)


class UserSessionRepository(UserSessionRepositoryInterface):
    def create_user_action(self, adress: str, text: str, session_unique_key: str) -> None:
        UserAction.objects.create(
            adress=adress,
            text=text,
            session=UserActivity.objects.get(unique_key=session_unique_key),
        )

    def create_session_action(self, adress: str, session_unique_key: str) -> None:
        try:
            SessionAction.objects.create(
                adress=adress,
                session=SessionModel.objects.get(unique_key=session_unique_key),
            )
        except OperationalError:
            pass

    def update_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        UserActivity.objects.update_or_create(unique_key=unique_key, defaults=session_data)

    def get_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> UserSessionInterface:
        session_db, _ = UserActivity.objects.get_or_create(unique_key=unique_key, defaults=session_data)

        return session_db

    def update_or_create_raw_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        try:
            if SessionModel.objects.filter(unique_key=unique_key).exists():
                pages_count = SessionModel.objects.get(unique_key=unique_key).pages_count + 1
                session_data["pages_count"] = pages_count

                SessionModel.objects.update(**session_data)
                return

            SessionModel.objects.create(**session_data)
        except OperationalError:
            pass


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
