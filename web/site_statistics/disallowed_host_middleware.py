from django.core.exceptions import DisallowedHost
from django.http import HttpRequest

from application.usecases.user_activity.disallowed_host import AddDisallowedHostPenalty
from infrastructure.persistence.models.site_statistics import SessionModel
from infrastructure.persistence.repositories.raw_session_repository import (
    get_raw_session_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from web.site_statistics.base_session_middleware import BaseSessionMiddleware


class DisallowedHostMiddleware(BaseSessionMiddleware):
    add_disallowed_host_penalty = AddDisallowedHostPenalty(get_user_session_repository(), get_raw_session_repository())

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.searcher:
            return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        try:
            request.get_host()
        except DisallowedHost:
            self.add_disallowed_host_penalty(request.raw_session.id)

        try:
            request.raw_session = self.raw_session_repository.get(request.raw_session.id)
        except SessionModel.DoesNotExist:
            pass

        return self.get_response(request)
