from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from application.sessions.raw_session_service import get_raw_session_service
from infrastructure.logging.tasks import create_raw_logs
from infrastructure.logging.user_activity.create_json_logs import create_raw_log
from infrastructure.requests.service import get_request_service
from web.site_statistics.middlewares.base import BaseSessionMiddleware


class RawSessionMiddleware(BaseSessionMiddleware):
    logs_array_length = 1
    logs: list[dict[str, Any]] = []
    cookie_name = settings.RAW_SESSION_COOKIE_NAME

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if hasattr(request, "search"):
            if request.searcher:
                return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        raw_session_service = get_raw_session_service(request_service=get_request_service(request))

        cookie = request.COOKIES.get(self.cookie_name)

        if cookie and "/" in cookie:
            cookie = None

        if not cookie:
            session_data = raw_session_service.create(
                device=request.user_agent.is_mobile
            )
        else:
            session_data = self.raw_session_repository.get(id=int(cookie))

            if not session_data:
                session_data = raw_session_service.create(
                    device=request.user_agent.is_mobile
                )

        if session_data.show_capcha:
            if not self.url_parser.is_source(path) and "submit-capcha" not in path:
                reject_capcha_penalty = self.user_session_repository.get_session_filters().reject_capcha

                session_data.ban_rate += reject_capcha_penalty
                session_data = self.raw_session_repository.update(session_data)
                self.penalty_logger(session_data.id, f"Отказ от капчи, {reject_capcha_penalty}, {path}")

        request.raw_session = session_data

        response = self.get_response(request)
        expires = datetime.utcnow() + timedelta(days=365 * 10)
        response.set_cookie(self.cookie_name, str(session_data.id), expires=expires)

        site = request.get_host()
        page_adress = site + path
        self.logs.append(create_raw_log(session_data.id, page_adress, path, time=now()))

        if len(self.logs) > self.logs_array_length:
            create_raw_logs.delay(self.logs)
            self.logs.clear()

        return response
