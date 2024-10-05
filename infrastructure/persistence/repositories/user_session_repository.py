from datetime import datetime
from typing import Any

from django.db.models import F
from django.utils.timezone import now

from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import UserSessionInterface
from infrastructure.persistence.models.site_statistics import (
    SessionAction,
    SessionFilters,
    SessionModel,
    UserAction,
    UserActivity,
)


class UserSessionRepository(UserSessionRepositoryInterface):
    def create_user_action(self, adress: str, text: str, session_unique_key: str, time: datetime = now()) -> None:
        print(session_unique_key, "session_unique_key")
        UserAction.objects.create(
            adress=adress,
            text=text,
            time=time,
            session=UserActivity.objects.get(unique_key=session_unique_key),
        )

    def get_raw_session(self, unique_key: str):
        try:
            return SessionModel.objects.get(unique_key=unique_key)
        except SessionModel.DoesNotExist:
            return None

    def get_user_session(self, unique_key: str):
        try:
            return UserActivity.objects.get(unique_key=unique_key)
        except UserActivity.DoesNotExist:
            return None

    def create_session_action(self, adress: str, session_unique_key: str, time: datetime, is_page: bool, is_source: bool) -> None:
        SessionAction.objects.create(
            adress=adress,
            time=time,
            is_page=is_page,
            is_source=is_source,
            session_id=SessionModel.objects.values_list("id", flat=True).get(unique_key=session_unique_key),
        )

    def create_user_session(self, **kwargs) -> None:
        UserActivity.objects.create(**kwargs)

    def get_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> UserSessionInterface:
        session_db, _ = UserActivity.objects.get_or_create(unique_key=unique_key, defaults=session_data)

        return session_db

    def get_session_filters(self):
        return SessionFilters.objects.first()

    def is_raw_session_exists(self, unique_key: str) -> bool:
        return SessionModel.objects.filter(unique_key=unique_key).exists()

    def is_user_session_exists(self, unique_key: str) -> bool:
        return UserActivity.objects.filter(unique_key=unique_key).exists()

    def update_raw_session_unique_key(self, old_unique_key: str, new_unique_key: str) -> None:
        SessionModel.objects.filter(unique_key=old_unique_key).update(unique_key=new_unique_key)

    def update_user_session_unique_key(self, old_unique_key: str, new_unique_key: str) -> None:
        UserActivity.objects.filter(unique_key=old_unique_key).update(unique_key=new_unique_key)

    def create_raw_session(self, **kwargs):
        return SessionModel.objects.create(**kwargs)

    def update_raw_session(self, unique_key, **kwargs):
        SessionModel.objects.filter(unique_key=unique_key).update(**kwargs)

    def update_user_session(self, unique_key, **kwargs):
        UserActivity.objects.filter(unique_key=unique_key).update(**kwargs)

    def increment_user_session_field(self, unique_key: str, field_name: str) -> None:
        UserActivity.objects.filter(unique_key=unique_key).update(**{field_name: F(field_name) + 1})

    def increment_raw_session_field(self, unique_key: str, field_name: str) -> None:
        SessionModel.objects.filter(unique_key=unique_key).update(**{field_name: F(field_name) + 1})
        
    def bulk_create_raw_session_logs(self, logs):
        SessionAction.objects.bulk_crete(logs)


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
