from application.texts.errors import Errors
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.models.site_statistics import PenaltyLog


class AddDisallowedHostPenalty:
    def __init__(self, repository: UserSessionRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, session_id: int) -> None:
        disallowed_host_penalty = self.repository.get_disallowed_host_penalty()
        self.repository.change_ban_rate(session_id, disallowed_host_penalty)

        PenaltyLog.objects.create(
            session_id=session_id,
            text=Errors.disallowed_host,
        )
