from collections.abc import Iterable
from datetime import datetime

from django.db.models import F
from django.utils.timezone import now

from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import UserSessionInterface
from domain.user_sessions.session_filters import SessionFIltersHeader
from infrastructure.persistence.models.site_statistics import (
    SessionFilters,
    UserAction,
    UserActivity,
    WebSearcher,
    WebSearcherAction,
)


class UserSessionRepository(UserSessionRepositoryInterface):
    def create_user_action(self, adress: str, text: str, session_id: int, time: datetime | None = None) -> None:
        if time is None:
            time = now()

        UserAction.objects.create(
            adress=adress,
            text=text,
            time=time,
            session_id=session_id,
        )

    def get_session_filter_headers(self) -> Iterable[SessionFIltersHeader]:
        filters = SessionFilters.objects.first()
        if filters:
            return filters.headers.all()

        return []

    def create_user_session(self, **kwargs) -> UserSessionInterface:
        return UserActivity.objects.create(**kwargs)

    def get_session_filters(self):
        return SessionFilters.objects.first()

    def get_searchers(self) -> str:
        session_filters = SessionFilters.objects.values_list("searchers").first()
        return session_filters[0] if session_filters else ""

    def is_user_session_exists_by_id(self, id: int) -> bool:
        return UserActivity.objects.filter(id=id).exists()

    def is_searcher_exists_by_id(self, id: int) -> bool:
        return WebSearcher.objects.filter(id=id).exists()

    def create_searcher_log(self, **kwargs) -> None:
        WebSearcherAction.objects.create(**kwargs)

    def create_searcher(self, **kwargs) -> int:
        searcher = WebSearcher.objects.create(**kwargs)
        return searcher.id

    def update_user_session(self, id: int, **kwargs) -> None:
        UserActivity.objects.filter(id=id).update(**kwargs)

    def increment_user_session_field(self, id: int, field_name: str) -> None:
        UserActivity.objects.filter(id=id).update(**{field_name: F(field_name) + 1})

    def bulk_create_user_session_logs(self, logs):
        new_logs = [log for log in logs if log["session_id"] in UserActivity.objects.values_list("id", flat=True)]
        UserAction.objects.bulk_create([UserAction(**log) for log in new_logs])

    def delete_user_session(self, id: int) -> None:
        return UserActivity.objects.get(id=id).delete()

    def get_success_capcha_increase(self):
        return SessionFilters.objects.values_list("capcha_success", flat=True).first()

    def get_page_not_found_penalty(self):
        return SessionFilters.objects.values_list("page_not_found_penalty", flat=True).first()

    def get_capcha_limit(self):
        return SessionFilters.objects.values_list("capcha_limit", flat=True).first()

    def get_ban_limit(self):
        return SessionFilters.objects.values_list("ban_limit", flat=True).first()

    def get_reject_capcha_penalty(self):
        return SessionFilters.objects.values_list("reject_capcha", flat=True).first()

    def get_disallowed_host_penalty(self):
        return SessionFilters.objects.values_list("disallowed_host", flat=True).first()

    def delete_hacking_visitors(self, ban_limit: int) -> None:
        UserActivity.objects.filter(session__ban_rate__gte=ban_limit).delete()

    def get_no_cookie_penalty(self) -> int:
        return SessionFilters.objects.values_list("no_cookie", flat=True).first()


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
