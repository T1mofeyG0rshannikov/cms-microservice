from django.http import HttpRequest
from rest_framework.renderers import JSONRenderer

from application.sessions.raw_session_service import RawSessionService
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.persistence.models.site_statistics import SessionModel
from infrastructure.requests.service import get_request_service
from web.site_statistics.base_session_middleware import BaseSessionMiddleware
from web.site_statistics.views import CapchaView


class PageNotFoundMiddleware(BaseSessionMiddleware):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.searcher:
            return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        response = self.get_response(request)

        if response.status_code == 404 and not self.url_parser.is_source(request.path):
            session_id = request.raw_session.id
            page_not_found_penalty = self.user_session_repository.get_page_not_found_penalty()
            self.raw_session_repository.change_ban_rate(session_id, page_not_found_penalty)
            self.penalty_logger(session_id, f"Несуществующий адрес, {page_not_found_penalty}, {path}")

        request_service = get_request_service(request)
        raw_session_service = RawSessionService(
            request_service,
            self.user_session_repository,
            self.raw_session_repository,
            self.url_parser,
            self.penalty_logger,
            get_admin_settings(),
        )

        try:
            session_id = request.raw_session.id
            raw_session = self.raw_session_repository.get(session_id)
        except SessionModel.DoesNotExist:
            return self.get_response(request)

        site = request.get_host()
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        raw_session = raw_session_service.filter_sessions(
            raw_session,
            host,
            path,
            port,
            raw_session.id,
        )

        self.raw_session_repository.update(
            raw_session.id,
            hacking=raw_session.hacking,
            ban_rate=raw_session.ban_rate,
        )

        if (
            raw_session.show_capcha
            and (not self.url_parser.is_source(path) and "submit-capcha" not in path)
            and not raw_session.hacking
        ):
            response = CapchaView.as_view()(request)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            self.raw_session_repository.update(request.raw_session.id, show_capcha=True)

            return response

        return response
