from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.sessions.user_activity_service import get_user_session_service
from infrastructure.logging.tasks import create_user_activity_logs
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.logging.user_activity.create_json_logs import create_user_log
from web.site_statistics.middlewares.base import BaseSessionMiddleware


class UserActivityMiddleware(BaseSessionMiddleware):
    logs: list[dict[str, Any]] = []
    logs_array_length = 1
    cookie_name = settings.USER_ACTIVITY_COOKIE_NAME
    user_activity_service = get_user_session_service()

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.exclude_urls = get_user_active_settings().exclude_urls
        self.enabled_adresses = get_user_active_settings().enable_adresses
        self.disable_user_session_urls_to_logg = get_user_active_settings().disable_user_session_urls_to_logg

    def __call__(self, request: HttpRequest):
        if request.searcher:
            return self.get_response(request)

        path = request.get_full_path()
        if "get-user-info" in path:
            return self.get_response(request)

        session_filters = self.user_session_repository.get_session_filters()
        if not session_filters:
            return self.get_response(request)
        
        ban_limit = session_filters.ban_limit
        if not ban_limit:
            ban_limit = 10**10

        raw_session = request.raw_session
        cookie = request.COOKIES.get(self.cookie_name)

        if cookie and "/" in cookie:
            cookie = None

        if raw_session.ban_rate < ban_limit:
            site = raw_session.site
            page_adress = site + path

            user_id = request.user.id if request.user.is_authenticated else None

            session_data = None

            if not cookie:
                session_data = self.user_activity_service.create(
                    user_id=user_id,
                    session_id=raw_session.id,
                )
            else:
                session_id = int(cookie)
                session_data = self.user_session_repository.get(id=session_id)

                if not session_data:
                    session_data = self.user_activity_service.create(user_id=user_id, session_id=raw_session.id)

                if user_id and not session_data.user_id:
                    session_data.auth = "auth"
                    session_data.user_id = user_id
                    session_data = self.user_session_repository.update(session_data)

            request.user_session_id = session_data.id
            response = self.get_response(request)
            expires = datetime.utcnow() + timedelta(days=365 * 10)
            response.set_cookie(self.cookie_name, str(session_data.id), expires=expires)

            if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
                self.logs.append(create_user_log(session_data.id, page_adress, "Перешёл на страницу", time=now()))

            if len(self.logs) > self.logs_array_length:
                create_user_activity_logs.delay(self.logs)
                self.logs.clear()

            return response
        else:
            if cookie:
                session_id = int(cookie)
                self.user_session_repository.delete_user_session(session_id)

            response = HttpResponse(status=503)
            response.delete_cookie(self.cookie_name)

        return response

    def is_disable_url_to_log(self, path: str) -> bool:
        for url in self.disable_user_session_urls_to_logg:
            if url in path:
                return True

        return False

    def is_enable_url_to_log(self, path: str) -> bool:
        for url in self.exclude_urls:
            if url in path:
                return False

        return True

    def is_enable_adress_to_log(self, path: str) -> bool:
        for enable_adress in self.enabled_adresses:
            if enable_adress in path:
                return True

        return False
