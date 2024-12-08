from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.requests.request_interface import RequestInterface


class IncrementSessionCount:
    def __init__(self, repository: UserSessionRepositoryInterface, field_name: str) -> None:
        self.user_session_repository = repository
        self.session_field_name = field_name

    def __call__(self, request: RequestInterface) -> None:
        self.user_session_repository.increment_user_session_field(request.user_session_id, self.session_field_name)


def get_increment_session_count(
    field: str,
    repository: UserSessionRepositoryInterface = get_user_session_repository(),
) -> IncrementSessionCount:
    return IncrementSessionCount(field_name=field, repository=repository)
