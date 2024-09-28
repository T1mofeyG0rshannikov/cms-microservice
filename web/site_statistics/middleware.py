from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.sessions.dto import RawSessionDTO, UserActivityDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.requests.get_ip import get_client_ip
from infrastructure.requests.valid_ip import is_valid_ip
from web.site_statistics.models import SessionFilters


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = get_user_active_settings().exclude_urls
        self.enabled_adresses = get_user_active_settings().enable_adresses
        self.session_key = settings.USER_ACTIVITY_SESSION_KEY
        self.user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()

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
        # del request.session[self.session_key]
        # request.session.save()
        # return self.get_response(request)

        # del request.session[self.session_key]["user"]
        # request.session.save()

        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key
        print(unique_key, "unique_key")
        # if not unique_key:
        #    return self.get_response(request)
        ip = get_client_ip(request)
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path

        session_data = RawSessionDTO(
            unique_key=unique_key,
            ip=ip,
            start_time=now().isoformat(),
            end_time=now().isoformat(),
            site=site,
            device=request.user_agent.is_pc,
        )

        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        session_filters = SessionFilters.objects.first()
        print(host)
        if session_filters:
            if host != "127.0.0.1" and host != "localhost":
                if session_filters.disable_ip and is_valid_ip(host):
                    session_data.hacking = True
                    session_data.hacking_reason = "Запрос по IP"

                if session_filters.disable_ports and port:
                    session_data.hacking = True
                    session_data.hacking_reason = "Запрос к порту"

                for disable_url in session_filters.disable_urls.splitlines():
                    if disable_url in page_adress:
                        print(disable_url, "disable_url")
                        session_data.hacking = True
                        session_data.hacking_reason = "Запрещенный адрес"
                        break

        session_data = session_data.__dict__

        self.user_session_repository.update_or_create_raw_session(unique_key=unique_key, session_data=session_data)

        self.user_session_repository.create_session_action(
            adress=page_adress,
            session_unique_key=unique_key,
        )

        if self.is_enable_adress_to_log(path):
            return self.get_response(request)

        user_id = request.user.id if request.user.is_authenticated else None

        user_session_data = UserActivityDTO(
            unique_key=unique_key,
            ip=ip,
            start_time=now().isoformat(),
            end_time=now().isoformat(),
            site=site,
            device=request.user_agent.is_pc,
            user_id=user_id,
            utm_source=request.GET.get("utm_source"),
        ).__dict__

        if self.session_key not in request.session:
            request.session[self.session_key] = user_session_data
            request.session[self.session_key]["pages_count"] += 1

            request.session.save()

            self.user_session_repository.get_or_create_user_session(
                unique_key=unique_key, session_data=user_session_data
            )

            self.user_session_repository.create_user_action(
                adress=page_adress, session_unique_key=unique_key, text="перешёл на страницу"
            )

            return self.get_response(request)

        if not self.is_enable_url_to_log(path):  # or response.status_code != 200:
            return self.get_response(request)

        self.user_session_repository.get_or_create_user_session(unique_key=unique_key, session_data=user_session_data)

        if "profile_actions_cocunt" not in request.session[self.session_key]:
            request.session[self.session_key]["profile_actions_count"] = 0
            request.session.save()

        if request.user.is_authenticated:
            request.session[self.session_key]["auth"] = "login"
            request.session[self.session_key]["user_id"] = user_id

        request.session[self.session_key]["pages_count"] += 1
        request.session[self.session_key]["end_time"] = now().isoformat()

        if host == "127.0.0.1" or host == "localhost":
            request.session[self.session_key]["hacking"] = False

        request.session.save()

        if "popups_count" in request.session[self.session_key]:
            del request.session[self.session_key]["popups_count"]

        user_session_data = request.session[self.session_key]
        user_session_data["unique_key"] = unique_key

        self.user_session_repository.update_or_create_user_session(
            unique_key=unique_key, session_data=user_session_data
        )

        self.user_session_repository.create_user_action(
            adress=page_adress, session_unique_key=unique_key, text="перешёл на страницу"
        )

        session_data = request.session[self.session_key]
        session_data["unique_key"] = unique_key
        print(session_data)

        if session_data["hacking"]:
            return HttpResponse(status=503)

        return self.get_response(request)
