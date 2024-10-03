from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_user_activity_log
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.user_activity_service import (
    UserActivitySessionService,
)
from infrastructure.requests.service import RequestService


class UserActivityMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    session_key = settings.USER_ACTIVITY_SESSION_KEY

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
        user_activity_service = UserActivitySessionService(RequestService(request), get_user_session_repository())

        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        user_id = request.user.id if request.user.is_authenticated else None

        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key

        cookie = request.COOKIES.get(settings.USER_ACTIVITY_COOKIE_NAME)
        print(cookie, type(cookie), "user")
        response = self.get_response(request)

        if path == "/user/get-user-info":
            return response
        # cookie = None
        if not cookie:
            expires = datetime.utcnow() + timedelta(days=365 * 10)
            response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

            session_data = user_activity_service.get_initial_data(
                site, user_id, unique_key, request.user_agent.is_mobile, request.GET.get("utm_source")
            )

            self.user_session_repository.create_user_session(**session_data.__dict__)
            if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
                create_user_activity_log.delay(
                    unique_key,
                    page_adress,
                    now(),
                )
        else:
            cookie_unique_key = cookie
            if cookie_unique_key == unique_key:
                session_data = user_activity_service.get_initial_data(
                    site, user_id, unique_key, request.user_agent.is_mobile, request.GET.get("utm_source")
                )

                if not self.user_session_repository.is_user_session_exists(unique_key):
                    self.user_session_repository.create_user_session(**session_data.__dict__)
                else:
                    auth = "login" if user_id else None
                    if auth:
                        self.user_session_repository.update_user_session(
                            unique_key,
                            end_time=now(),
                            hacking=session_data.hacking,
                            hacking_reason=session_data.hacking_reason,
                            auth=auth,
                            user_id=user_id,
                        )
                    else:
                        self.user_session_repository.update_user_session(
                            unique_key,
                            end_time=now(),
                            hacking=session_data.hacking,
                            hacking_reason=session_data.hacking_reason,
                        )
            else:
                expires = datetime.utcnow() + timedelta(days=365 * 10)
                response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

                self.user_session_repository.update_user_session_unique_key(cookie_unique_key, unique_key)

                auth = "login" if user_id else None
                if auth:
                    self.user_session_repository.update_user_session(
                        unique_key, end_time=now(), auth=auth, user_id=user_id
                    )
                else:
                    self.user_session_repository.update_user_session(unique_key, end_time=now())

        if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
            create_user_activity_log.delay(
                unique_key,
                page_adress,
                now(),
            )

        return response
