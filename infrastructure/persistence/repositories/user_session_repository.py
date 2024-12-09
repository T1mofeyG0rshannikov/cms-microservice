from collections.abc import Iterable
from datetime import datetime, timedelta

from django.db.models import Count, F
from django.utils import timezone
from django.utils.timezone import now

from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import UserSessionInterface
from domain.user_sessions.session_filters import SessionFIltersHeader
from infrastructure.persistence.models.site_statistics import (
    SessionAction,
    SessionFilters,
    SessionModel,
    UserAction,
    UserActivity,
    WebSearcher,
    WebSearcherAction,
)


class UserSessionRepository(UserSessionRepositoryInterface):
    def create_user_action(self, adress: str, text: str, session_id: int, time: datetime = None) -> None:
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

    def create_session_action(
        self, adress: str, session_id: int, time: datetime, is_page: bool, is_source: bool
    ) -> None:
        SessionAction.objects.create(
            adress=adress,
            time=time,
            is_page=is_page,
            is_source=is_source,
            session_id=session_id,
        )

    def create_user_session(self, **kwargs) -> UserSessionInterface:
        return UserActivity.objects.create(**kwargs)

    def get_session_filters(self):
        return SessionFilters.objects.first()

    def get_searchers(self) -> str:
        session_filters = SessionFilters.objects.values_list("searchers").first()
        if session_filters:
            return session_filters[0]

    def is_raw_session_exists_by_id(self, id: int) -> bool:
        return SessionModel.objects.filter(id=id).exists()

    def is_user_session_exists_by_id(self, id: int) -> bool:
        return UserActivity.objects.filter(id=id).exists()

    def create_raw_session(self, **kwargs) -> int:
        return SessionModel.objects.create(**kwargs)

    def update_raw_session(self, id, **kwargs) -> None:
        SessionModel.objects.filter(id=id).update(**kwargs)

    def is_searcher_exists_by_id(self, id: int) -> bool:
        return WebSearcher.objects.filter(id=id).exists()

    def create_searcher_log(self, **kwargs) -> None:
        WebSearcherAction.objects.create(**kwargs)

    def create_searcher(self, **kwargs) -> None:
        WebSearcher.objects.create(**kwargs)

    def update_user_session(self, id: int, **kwargs):
        UserActivity.objects.filter(id=id).update(**kwargs)

    def increment_user_session_field(self, id: int, field_name: str) -> None:
        UserActivity.objects.filter(id=id).update(**{field_name: F(field_name) + 1})

    def increment_raw_session_field(self, id: int, field_name: str) -> None:
        SessionModel.objects.filter(id=id).update(**{field_name: F(field_name) + 1})

    def bulk_create_raw_session_logs(self, logs):
        new_logs = [log for log in logs if log["session_id"] in SessionModel.objects.values_list("id", flat=True)]
        SessionAction.objects.bulk_create([SessionAction(**log) for log in new_logs])

    def bulk_create_user_session_logs(self, logs):
        new_logs = [log for log in logs if log["session_id"] in UserActivity.objects.values_list("id", flat=True)]
        UserAction.objects.bulk_create([UserAction(**log) for log in new_logs])

    def get_raw_session(self, id: int):
        return SessionModel.objects.get(id=id)

    def delete_user_session(self, id):
        return SessionModel.objects.filter(id=id).delete()

    def get_success_capcha_increase(self):
        return SessionFilters.objects.values_list("capcha_success", flat=True).first()

    def get_page_not_found_penalty(self):
        return SessionFilters.objects.values_list("page_not_found_penalty", flat=True).first()

    def change_ban_rate(self, session_id: int, increase_value: int):
        SessionModel.objects.filter(id=session_id).update(ban_rate=F("ban_rate") + increase_value)

    def get_capcha_limit(self):
        return SessionFilters.objects.values_list("capcha_limit", flat=True).first()

    def get_ban_limit(self):
        return SessionFilters.objects.values_list("ban_limit", flat=True).first()

    def get_reject_capcha_penalty(self):
        return SessionFilters.objects.values_list("reject_capcha", flat=True).first()

    def get_disallowed_host_penalty(self):
        return SessionFilters.objects.values_list("disallowed_host", flat=True).first()

    def add_penalty_to_single_page_session(self, penalty: int):
        time_threshold = timezone.now() - timedelta(minutes=20)

        SessionModel.objects.annotate(actions_count=Count("actions")).filter(
            actions_count=1, start_time__lte=time_threshold, checked_single_page=False
        ).update(ban_rate=F("ban_rate") + penalty, checked_single_page=True)

    def delete_hacking_visitors(self, ban_limit: int):
        UserActivity.objects.filter(session__ban_rate__gte=ban_limit).delete()

    def get_no_cookie_penalty(self) -> int:
        return SessionFilters.objects.values_list("no_cookie", flat=True).first()


def get_user_session_repository() -> UserSessionRepositoryInterface:
    return UserSessionRepository()
