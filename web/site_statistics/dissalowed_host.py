from django.core.exceptions import DisallowedHost
from django.http import HttpRequest

from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)


class DissalowedHostMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            host = request.get_host()
        except DisallowedHost:
            session_id = request.raw_session.id
            disallowed_host_penalty = self.user_session_repository.get_disallowed_host_penalty()
            self.user_session_repository.change_ban_rate(session_id, disallowed_host_penalty)

        return self.get_response(request)
