from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_user_activity_logs
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.user_activity_service import (
    UserActivitySessionService,
)
from infrastructure.requests.service import RequestService


def create_user_log(session_id, adress, text, time=now()):
    return {"adress": adress, "time": time, "session_id": session_id, "text": text}


class UserActivityMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    logs = []
    logs_array_length = 5
    cookie_name = settings.USER_ACTIVITY_COOKIE_NAME

    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = get_user_active_settings().exclude_urls
        self.enabled_adresses = get_user_active_settings().enable_adresses
        self.disable_user_session_urls_to_logg = get_user_active_settings().disable_user_session_urls_to_logg

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

    def __call__(self, request: HttpRequest):
        if request.searcher:
            return self.get_response(request)

        if not request.raw_session.hacking:
            user_activity_service = UserActivitySessionService(RequestService(request), get_user_session_repository())

            path = request.get_full_path()
            site = request.raw_session.site
            page_adress = site + path

            user_id = request.user.id if request.user.is_authenticated else None

            expires = datetime.utcnow() + timedelta(days=365 * 10)

            cookie = request.COOKIES.get(self.cookie_name)
            # print(cookie, type(cookie), "user")
            # cookie = None

            session_id = None

            if not cookie or ("/" not in cookie):
                session_data = user_activity_service.get_initial_data(
                    user_id=user_id,
                    device=request.user_agent.is_mobile,
                    utm_source=request.GET.get("utm_source"),
                )

                session_id = self.user_session_repository.create_user_session(**session_data.__dict__).id

            else:
                session_id = int(cookie.split("/")[1])

                auth = "login" if user_id else None
                if auth:
                    session_data = user_activity_service.get_initial_data(
                        user_id=user_id,
                        device=request.user_agent.is_mobile,
                        utm_source=request.GET.get("utm_source"),
                        auth=auth,
                    )
                else:
                    session_data = user_activity_service.get_initial_data(
                        user_id=user_id,
                        device=request.user_agent.is_mobile,
                        utm_source=request.GET.get("utm_source"),
                    )

                if not self.user_session_repository.is_user_session_exists_by_id(session_id):
                    session_id = self.user_session_repository.create_user_session(**session_data.__dict__).id

                else:
                    if session_data.auth:
                        self.user_session_repository.update_user_session(session_id, auth=auth, user_id=user_id)

            request.user_session_id = session_id
            response = self.get_response(request)

            if path == "/user/get-user-info":
                return response

            response.set_cookie(self.cookie_name, f"{session_id}/{session_id}", expires=expires)

            if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
                self.logs.append(create_user_log(session_id, page_adress, "Перешёл на страницу"))

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
