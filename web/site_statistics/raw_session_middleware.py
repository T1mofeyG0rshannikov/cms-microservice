from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.logging.tasks import create_raw_logs
from infrastructure.persistence.models.site_statistics import PenaltyLog, SessionAction
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service


def create_raw_log(
    session_id: int, page_adress: str, path: str, time=now(), url_parser: UrlParserInterface = get_url_parser()
) -> SessionAction:
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
        if request.searcher:
            return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        request_service = get_request_service(request)
        raw_session_service = RawSessionService(
            request_service, self.user_session_repository, self.url_parser, get_admin_settings()
        )

        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
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

            self.user_session_repository.update_raw_session(
                session_id,
                ban_rate=session_data.ban_rate,
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

            self.user_session_repository.update_raw_session(
                session_id,
                ban_rate=session_data.ban_rate,
            )

        # print(cookie, session_id)
        session_data = self.user_session_repository.get_raw_session(session_id)

        reject_capcha_penalty = self.user_session_repository.get_reject_capcha_penalty()

        if session_data.show_capcha:
            if not self.url_parser.is_source(path) and "submit-capcha" not in path:
                session_data.ban_rate += reject_capcha_penalty
                PenaltyLog.objects.create(
                    session_id=session_id,
                    text=f"Отказ от капчи, {reject_capcha_penalty}, {path}",
                )

        self.user_session_repository.update_raw_session(
            session_id,
            hacking=session_data.hacking,
            ban_rate=session_data.ban_rate,
        )

        session_db = self.user_session_repository.get_raw_session(session_id)

        request.raw_session = session_db
        response = self.get_response(request)
        response.set_cookie(self.cookie_name, f"{session_id}/{session_id}", expires=expires)

        self.logs.append(create_raw_log(session_id, page_adress, path, time=now()))

        if len(self.logs) > self.logs_array_length:
            create_raw_logs.delay(self.logs)
            self.logs.clear()

        return response
