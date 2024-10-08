import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_raw_logs
from infrastructure.persistence.models.site_statistics import SessionAction
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service


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


logger = logging.getLogger("main")


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    logs_array_length = 100
    logs = []

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        raw_session_service = RawSessionService(
            get_request_service(request), self.user_session_repository, self.url_parser
        )
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None
        expires = datetime.utcnow() + timedelta(days=365 * 10)

        cookie = request.COOKIES.get(settings.RAW_SESSION_COOKIE_NAME)

        response = self.get_response(request)

        if path == "/user/get-user-info":
            return response
        # cookie = None
        session_id = None
        # print(cookie)

        if not cookie or ("/" not in cookie):
            session_data = raw_session_service.get_initial_raw_session(path, site, request.user_agent.is_mobile)

            session_id = self.user_session_repository.create_raw_session(**session_data.__dict__).id
        else:
            session_id = int(cookie.split("/")[1])

            session_data = raw_session_service.filter_sessions(
                raw_session_service.get_initial_raw_session(path, site, request.user_agent.is_mobile),
                host,
                page_adress,
                port,
            )

            if not self.user_session_repository.is_raw_session_exists_by_id(session_id):
                session_id = self.user_session_repository.create_raw_session(**session_data.__dict__).id

            else:
                if session_data.hacking:
                    self.user_session_repository.update_raw_session(
                        id,
                        hacking=session_data.hacking,
                        hacking_reason=session_data.hacking_reason,
                    )
                    return HttpResponse(status=503)

        response.set_cookie(settings.RAW_SESSION_COOKIE_NAME, f"{session_id}/{session_id}", expires=expires)

        if "null" not in path:
            self.logs.append(create_raw_log(session_id, page_adress, path, time=now()))

        if len(self.logs) > self.logs_array_length:
            print(self.logs, "LLLLOGGGS")
            create_raw_logs.delay(self.logs)
            # self.user_session_repository.bulk_create_raw_session_logs(self.logs)
            self.logs.clear()

        return response
