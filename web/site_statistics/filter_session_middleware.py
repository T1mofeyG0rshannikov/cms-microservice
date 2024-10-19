from django.http import HttpRequest

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service


class FilterSessionMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """print("333333333333333333333333333333333333333")
        request_service = get_request_service(request)
        raw_session_service = RawSessionService(
            request_service, self.user_session_repository, self.url_parser, get_admin_settings()
        )

        path = request.get_full_path()
        raw_session = self.user_session_repository.get_raw_session(request.raw_session.id)

        site = request.get_host()
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        session_data = raw_session_service.filter_sessions(
            RawSessionDTO.from_dict(raw_session.__dict__),
            host,
            path,
            port,
            request_service.get_all_headers(),
            raw_session,
        )

        request.raw_session = session_data"""
        response = self.get_response(request)

        return response
