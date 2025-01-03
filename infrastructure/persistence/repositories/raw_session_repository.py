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
    def create(self, **kwargs) -> SessionInterface:
        return SessionModel.objects.create(**kwargs)

    def update(self, session: SessionInterface, updated_fields: list[str] | None = None) -> SessionInterface:
        if hasattr(session, "save"):
            if not updated_fields:
                session.save()
            else:
                session.save(update_fields=updated_fields)
        return session

    def bulk_create_logs(self, logs):
        new_logs = [log for log in logs if log["session_id"] in SessionModel.objects.values_list("id", flat=True)]
        SessionAction.objects.bulk_create([SessionAction(**log) for log in new_logs])

    def get(self, id: int):
        try:
            return SessionModel.objects.get(id=id)
        except SessionModel.DoesNotExist:
            return None

    def change_ban_rate(self, session_id: int, increase_value: int) -> None:
        SessionModel.objects.filter(id=session_id).update(ban_rate=F("ban_rate") + increase_value)

    def add_penalty_to_single_page_session(self, penalty: int):
        time_threshold = timezone.now() - timedelta(minutes=20)

        SessionModel.objects.annotate(actions_count=Count("actions")).filter(
            actions_count=1, start_time__lte=time_threshold, checked_single_page=False
        ).update(ban_rate=F("ban_rate") + penalty, checked_single_page=True)


def get_raw_session_repository() -> RawSessionRepositoryInterface:
    return RawSessionRepository()
