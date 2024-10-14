from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now
from rest_framework.renderers import JSONRenderer

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_raw_logs
from infrastructure.persistence.models.site_statistics import SessionAction
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service
from web.site_statistics.views import CapchaView


def create_raw_log(session_id, page_adress, path, time=now()) -> SessionAction:
    url_parser = get_url_parser()

    is_page = None
    is_source = None

    is_page = False if url_parser.is_source(path) else True
    is_source = not is_page

    return {
        "adress": page_adress,
        "time": time,
        "is_page": is_page,
        "is_source": is_source,
        "session_id": session_id,
    }


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    logs_array_length = 100
    logs = []
    cookie_name = settings.RAW_SESSION_COOKIE_NAME

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request_service = get_request_service(request)
        raw_session_service = RawSessionService(request_service, self.user_session_repository, self.url_parser)

        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None
        expires = datetime.utcnow() + timedelta(days=365 * 10)

        cookie = request.COOKIES.get(self.cookie_name)

        # cookie = None
        session_id = None

        if not cookie or ("/" not in cookie):
            session_data = raw_session_service.get_initial_raw_session(request.user_agent.is_mobile)
            session_db = self.user_session_repository.create_raw_session(**session_data.__dict__)
            session_id = session_db.id

            session_data = raw_session_service.check_headers(
                RawSessionDTO.from_dict(session_db.__dict__),
                request_service.get_all_headers(),
                session_db,
            )
        else:
            session_id = int(cookie.split("/")[1])

        if not self.user_session_repository.is_raw_session_exists_by_id(session_id):
            session_data = raw_session_service.get_initial_raw_session(request.user_agent.is_mobile)
            session_db = self.user_session_repository.create_raw_session(**session_data.__dict__)
            session_id = session_db.id

            session_data = raw_session_service.check_headers(
                RawSessionDTO.from_dict(session_db.__dict__),
                request_service.get_all_headers(),
                session_db,
            )

        print(cookie, session_id)
        session_data = self.user_session_repository.get_raw_session(session_id)

        capcha_limit = self.user_session_repository.get_capcha_limit()
        ban_limit = self.user_session_repository.get_ban_limit()
        reject_capcha_penalty = self.user_session_repository.get_reject_capcha_penalty()

        if capcha_limit <= session_data.ban_rate <= ban_limit:
            # print(path, self.url_parser.is_source(path))
            if not self.url_parser.is_source(path) and "submit-capcha" not in path:
                session_data.ban_rate += reject_capcha_penalty
                # print("capcha_reject")

        session_data = raw_session_service.filter_sessions(
            RawSessionDTO.from_dict(session_data.__dict__),
            host,
            path,
            port,
            request_service.get_all_headers(),
            session_data,
        )

        self.user_session_repository.update_raw_session(
            session_id,
            hacking=session_data.hacking,
            hacking_reason=session_data.hacking_reason,
            ban_rate=session_data.ban_rate,
        )

        session_db = self.user_session_repository.get_raw_session(session_id)

        if (
            session_data.show_capcha
            and (not self.url_parser.is_source(path) and not "submit-capcha" in path)
            and not session_data.hacking
        ):
            response = CapchaView.as_view()(request)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            return response

        print(session_db.ban_rate)
        # if session_db.hacking:
        #    return HttpResponse(status=503)
        request.raw_session = session_db
        response = self.get_response(request)

        if path == "/user/get-user-info":
            return response

        response.set_cookie(self.cookie_name, f"{session_id}/{session_id}", expires=expires)

        if "null" not in path:
            self.logs.append(create_raw_log(session_id, page_adress, path, time=now()))

        if len(self.logs) > self.logs_array_length:
            print(self.logs, "LLLLOGGGS")
            create_raw_logs.delay(self.logs)
            # self.user_session_repository.bulk_create_raw_session_logs(self.logs)
            self.logs.clear()

        return response

        """if not url_parser.is_source(path) and not "submit-capcha" in path:
            response = CapchaView.as_view()(request)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            return response"""
