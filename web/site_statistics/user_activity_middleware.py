from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.sessions.user_activity_service import UserActivitySessionService
from domain.user_sessions.session import SessionInterface
from infrastructure.logging.tasks import create_user_activity_logs
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.logging.user_activity.create_json_logs import create_user_log
from infrastructure.requests.service import RequestService
from web.site_statistics.base_session_middleware import BaseSessionMiddleware


class UserActivityMiddleware(BaseSessionMiddleware):
    logs = []
    logs_array_length = 5
    cookie_name = settings.USER_ACTIVITY_COOKIE_NAME

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

        if request.searcher:
            return self.get_response(request)

        ban_limit = self.user_session_repository.get_ban_limit()
        if not ban_limit:
            ban_limit = 10**10

        raw_session: SessionInterface = request.raw_session

        if raw_session.ban_rate < ban_limit:
            user_activity_service = UserActivitySessionService(RequestService(request))

            site = raw_session.site
            page_adress = site + path

            user_id = request.user.id if request.user.is_authenticated else None

            expires = datetime.utcnow() + timedelta(days=365 * 10)

            cookie = request.COOKIES.get(self.cookie_name)

            session_id = None

            if not cookie or ("/" not in cookie):
                session_data = user_activity_service.get_initial_data(
                    user_id=user_id,
                    device=request.user_agent.is_mobile,
                    session_id=raw_session.id,
                )

                session_id = self.user_session_repository.create_user_session(**session_data.__dict__).id

            else:
                session_id = int(cookie.split("/")[1])

                auth = "login" if user_id else None
                if auth:
                    session_data = user_activity_service.get_initial_data(
                        user_id=user_id,
                        device=request.user_agent.is_mobile,
                        auth=auth,
                        session_id=raw_session.id,
                    )
                else:
                    session_data = user_activity_service.get_initial_data(
                        user_id=user_id,
                        device=request.user_agent.is_mobile,
                        session_id=raw_session.id,
                    )

                if not self.user_session_repository.is_user_session_exists_by_id(session_id):
                    session_id = self.user_session_repository.create_user_session(**session_data.__dict__).id

                else:
                    if session_data.auth:
                        self.user_session_repository.update_user_session(session_id, auth=auth, user_id=user_id)

            request.user_session_id = session_id
            response = self.get_response(request)

            response.set_cookie(self.cookie_name, f"{session_id}/{session_id}", expires=expires)

            if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
                self.logs.append(create_user_log(session_id, page_adress, "Перешёл на страницу", time=now()))

            if len(self.logs) > self.logs_array_length:
                create_user_activity_logs.delay(self.logs)
                self.logs.clear()

            return response
        else:
            cookie = request.COOKIES.get(self.cookie_name)

            if not cookie or ("/" not in cookie):
                pass

            else:
                session_id = int(cookie.split("/")[1])
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
