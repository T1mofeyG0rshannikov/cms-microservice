from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import UserActivityDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_user_activity_log
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
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
        request_service = RequestService(request)
        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        user_id = request.user.id if request.user.is_authenticated else None

        if self.session_key not in request.session:
            ip = request_service.get_client_ip()
            hacking = False
            hacking_reason = None

            user_session_data = UserActivityDTO(
                unique_key=unique_key,
                ip=ip,
                start_time=now().isoformat(),
                end_time=now().isoformat(),
                site=site,
                device=request.user_agent.is_mobile,
                user_id=user_id,
                utm_source=request.GET.get("utm_source"),
                hacking=hacking,
                hacking_reason=hacking_reason,
            ).__dict__

            request.session[self.session_key] = user_session_data

        if user_id:
            request.session[self.session_key]["auth"] = "login"
            request.session[self.session_key]["user_id"] = user_id

        request.session[self.session_key]["end_time"] = now().isoformat()
        request.session[self.session_key]["unique_key"] = unique_key

        if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
            self.user_session_repository.increment_pages_count(unique_key)

        request.session.save()

        user_session_data = request.session[self.session_key]

        create_user_activity_log.delay(
            unique_key,
            user_session_data,
            page_adress,
            self.is_disable_url_to_log(path),
            self.is_enable_url_to_log(path),
            now(),
        )

        """try:
            executed_user_session = True
            self.user_session_repository.update_or_create_user_session(unique_key=unique_key, session_data=user_session_data)
        except:
            executed_user_session = False

        if executed_user_session:
            if not self.is_disable_url_to_log(path) and self.is_enable_url_to_log(path):
                self.user_session_repository.create_user_action(
                    adress=page_adress, session_unique_key=unique_key, text="перешёл на страницу"
                )"""

        return self.get_response(request)
