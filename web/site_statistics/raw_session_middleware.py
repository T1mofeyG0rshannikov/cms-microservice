from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_raw_log
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    session_key = settings.RAW_SESSION_SESSION_KEY

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        raw_session_service = RawSessionService(get_request_service(request), self.user_session_repository)
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key

        cookie = request.COOKIES.get(settings.USER_ACTIVITY_COOKIE_NAME)

        response = self.get_response(request)

        if path == "/user/get-user-info":
            return response
        # cookie = None
        if not cookie:
            expires = datetime.utcnow() + timedelta(days=365 * 10)
            response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

            session_data = raw_session_service.get_initial_raw_session(
                unique_key, path, site, request.user_agent.is_mobile
            )
            # print(1, session_data)

            self.user_session_repository.create_raw_session(**session_data.__dict__)
            create_raw_log.delay(unique_key, page_adress, path, time=now())
        else:
            cookie_unique_key = cookie
            if cookie_unique_key == unique_key:
                session_data = raw_session_service.get_initial_raw_session(
                    unique_key, path, site, request.user_agent.is_mobile
                )
                session_data = raw_session_service.filter_sessions(session_data, host, page_adress, port)

                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    self.user_session_repository.create_raw_session(**session_data.__dict__)
                else:
                    self.user_session_repository.update_raw_session(
                        unique_key,
                        end_time=now(),
                        hacking=session_data.hacking,
                        hacking_reason=session_data.hacking_reason,
                    )

                # print(2, session_data)
            else:
                expires = datetime.utcnow() + timedelta(days=365 * 10)
                response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

                if not self.user_session_repository.is_raw_session_exists(cookie_unique_key):
                    session_data = raw_session_service.get_initial_raw_session(
                        cookie_unique_key, path, site, request.user_agent.is_mobile
                    )
                    self.user_session_repository.create_raw_session(**session_data.__dict__)
                    if not self.user_session_repository.is_raw_session_exists(unique_key):
                        self.user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)

                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    self.user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)

                session_data = self.user_session_repository.get_raw_session(unique_key)
                session_data = raw_session_service.get_initial_raw_session(
                    unique_key, path, site, request.user_agent.is_mobile
                )
                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    self.user_session_repository.create_raw_session(**session_data.__dict__)
                create_raw_log.delay(unique_key, page_adress, path, time=now())
                # print(3, session_data)

        if session_data.hacking:
            return HttpResponse(status=503)

        create_raw_log.delay(unique_key, page_adress, path, time=now())

        return response
