from application.texts.errors import ErrorsMessages
from application.usecases.user_activity.add_penalty import AddPenaltyLog
from domain.user_sessions.repositories.raw_session_repository import (
    RawSessionRepositoryInterface,
)
from domain.user_sessions.repository import UserSessionRepositoryInterface


class AddDisallowedHostPenalty:
    def __init__(
        self, repository: UserSessionRepositoryInterface, raw_session_repository: RawSessionRepositoryInterface
    ) -> None:
        self.repository = repository
        self.raw_session_repository = raw_session_repository
        self.penalty_logger = AddPenaltyLog()

    def __call__(self, session_id: int) -> None:
        disallowed_host_penalty = self.repository.get_disallowed_host_penalty()
        self.raw_session_repository.change_ban_rate(session_id, disallowed_host_penalty)

        self.penalty_logger(
            session_id=session_id,
            text=ErrorsMessages.disallowed_host,
        )
