from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from application.sessions.raw_session_service import get_raw_session_service
from infrastructure.logging.tasks import create_raw_logs
from infrastructure.logging.user_activity.create_json_logs import create_raw_log
from infrastructure.requests.service import get_request_service
from web.site_statistics.base_session_middleware import BaseSessionMiddleware


class RawSessionMiddleware(BaseSessionMiddleware):
    logs_array_length = 100
    logs: list[dict[str, Any]] = []
    cookie_name = settings.RAW_SESSION_COOKIE_NAME

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.searcher:
            return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        raw_session_service = get_raw_session_service(request_service=get_request_service(request))

        site = request.get_host()
        page_adress = site + path
        expires = datetime.utcnow() + timedelta(days=365 * 10)

        cookie = request.COOKIES.get(self.cookie_name)

        # cookie = None
        session_data = None

        if not cookie or ("/" not in cookie):
            session_data = raw_session_service.create(request.user_agent.is_mobile)
        else:
            session_data = self.raw_session_repository.get(id=int(cookie.split("/")[1]))

        if not session_data:
            session_data = raw_session_service.create(request.user_agent.is_mobile)

        reject_capcha_penalty = self.user_session_repository.get_session_filters().reject_capcha

        if session_data.show_capcha:
            if not self.url_parser.is_source(path) and "submit-capcha" not in path:
                session_data.ban_rate += reject_capcha_penalty
                session_data = self.raw_session_repository.update(session_data)
                self.penalty_logger(session_data.id, f"Отказ от капчи, {reject_capcha_penalty}, {path}")

        request.raw_session = session_data

        response = self.get_response(request)
        response.set_cookie(self.cookie_name, f"{session_data.id}/{session_data.id}", expires=expires)

        self.logs.append(create_raw_log(session_data.id, page_adress, path, time=now()))

        if len(self.logs) > self.logs_array_length:
            create_raw_logs.delay(self.logs)
            self.logs.clear()

        return response
