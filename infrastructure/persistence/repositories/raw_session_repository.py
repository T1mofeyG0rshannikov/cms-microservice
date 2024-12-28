from datetime import timedelta

from django.db.models import Count, F
from django.utils import timezone

from domain.user_sessions.repositories.raw_session_repository import (
    RawSessionRepositoryInterface,
)
from domain.user_sessions.session import SessionInterface
from infrastructure.persistence.models.site_statistics import (
    SessionAction,
    SessionModel,
)


class RawSessionRepository(RawSessionRepositoryInterface):
    def is_exists_by_id(self, id: int) -> bool:
        return SessionModel.objects.filter(id=id).exists()

    def create(self, **kwargs) -> SessionInterface:
        return SessionModel.objects.create(**kwargs)

    def update(self, id: int, **kwargs) -> None:
        SessionModel.objects.filter(id=id).update(**kwargs)

    def bulk_create_logs(self, logs):
        new_logs = [log for log in logs if log["session_id"] in SessionModel.objects.values_list("id", flat=True)]
        SessionAction.objects.bulk_create([SessionAction(**log) for log in new_logs])

    def get(self, id: int):
        return SessionModel.objects.get(id=id)

    def change_ban_rate(self, session_id: int, increase_value: int):
        SessionModel.objects.filter(id=session_id).update(ban_rate=F("ban_rate") + increase_value)

    def add_penalty_to_single_page_session(self, penalty: int):
        time_threshold = timezone.now() - timedelta(minutes=20)

        SessionModel.objects.annotate(actions_count=Count("actions")).filter(
            actions_count=1, start_time__lte=time_threshold, checked_single_page=False
        ).update(ban_rate=F("ban_rate") + penalty, checked_single_page=True)


def get_raw_session_repository() -> RawSessionRepositoryInterface:
    return RawSessionRepository()
