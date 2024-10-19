from django.http import HttpRequest
from rest_framework.renderers import JSONRenderer

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
from web.site_statistics.views import CapchaView


class PageNotFoundMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        print("2222222222222222222222222222222222")
        response = self.get_response(request)
        if response.status_code == 404 and not self.url_parser.is_source(request.path) and "null" not in request.path:
            session_id = request.raw_session.id
            page_not_found_penalty = self.user_session_repository.get_page_not_found_penalty()
            self.user_session_repository.change_ban_rate(session_id, page_not_found_penalty)
            print("page not found")

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

        raw_session = session_data
        path = request.get_full_path()
        print(raw_session.ban_rate, raw_session.show_capcha)
        print(path)
        print(
            raw_session.show_capcha
            and (not self.url_parser.is_source(path) and not "submit-capcha" in path)
            and not raw_session.hacking
            and not "null" in path
        )
        if (
            raw_session.show_capcha
            and (not self.url_parser.is_source(path) and not "submit-capcha" in path)
            and not raw_session.hacking
            and not "null" in path
        ):
            response = CapchaView.as_view()(request)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            self.user_session_repository.update_raw_session(request.raw_session.id, show_capcha=True)

            return response

        return response
