from datetime import datetime
from typing import Any

from django.db.models import F
from django.db.utils import OperationalError
from django.utils.timezone import now

from application.services.domains.url_parser import get_url_parser
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
    def create_user_action(self, adress: str, text: str, session_unique_key: str, time: datetime = None) -> None:
        if not time:
            time = now()

        UserAction.objects.create(
            adress=adress,
            text=text,
            time=time,
            session=UserActivity.objects.get(unique_key=session_unique_key),
        )

    def get_raw_session(self, unique_key: str):
        return SessionModel.objects.get(unique_key=unique_key)

    def create_session_action(self, adress: str, session_unique_key: str, time: datetime, path) -> None:
        if not time:
            time = now()

        url_parser = get_url_parser()
        if url_parser.is_source(path):
            SessionModel.objects.filter(unique_key=session_unique_key).update(source_count=F("source_count") + 1)
        else:
            SessionModel.objects.filter(unique_key=session_unique_key).update(pages_count=F("pages_count") + 1)

        try:
            SessionAction.objects.create(
                adress=adress,
                time=time,
                session=SessionModel.objects.get(unique_key=session_unique_key),
            )
        except OperationalError:
            pass

    def update_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        UserActivity.objects.update_or_create(unique_key=unique_key, defaults=session_data)

    def get_or_create_user_session(self, unique_key: str, session_data: dict[str, Any]) -> UserSessionInterface:
        session_db, _ = UserActivity.objects.get_or_create(unique_key=unique_key, defaults=session_data)

        return session_db

    def get_session_filters(self):
        return SessionFilters.objects.first()

    def is_raw_session_exists(self, unique_key: str) -> bool:
        return SessionModel.objects.filter(unique_key=unique_key).exists()
    
    def increment_pages_count(self, unique_key: str) -> None:
        UserActivity.objects.filter(unique_key=unique_key).update(pages_count=F("pages_count")+1)

    def update_or_create_raw_session(self, unique_key: str, session_data: dict[str, Any]) -> None:
        try:
            if session_data["new"]:
                del session_data["new"]
                return SessionModel.objects.create(**session_data)
            else:
                if "headers" in session_data:
                    del session_data["headers"]

                del session_data["new"]
                old_unique_key = session_data["unique_key"]
                del session_data["unique_key"]
                print(unique_key, old_unique_key)
                SessionModel.objects.filter(unique_key=old_unique_key).update(**session_data, unique_key=unique_key)
                return SessionModel.objects.get(unique_key=unique_key)

        except OperationalError:
            pass


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
