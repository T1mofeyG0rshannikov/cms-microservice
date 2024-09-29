from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.user_activity.config import get_user_active_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.requests.get_ip import get_client_ip
from infrastructure.requests.service import RequestService


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    session_key = settings.RAW_SESSION_SESSION_KEY

    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = get_user_active_settings().exclude_urls
        self.enabled_adresses = get_user_active_settings().enable_adresses
        self.disable_user_session_urls_to_logg = get_user_active_settings().disable_user_session_urls_to_logg

    def __call__(self, request: HttpRequest):
        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key
        request_service = RequestService(request)

        ip = get_client_ip(request)
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        headers = request_service.get_all_headers_to_string()

        if self.session_key in request.session:
            hacking = request.session[self.session_key]["hacking"]
            hacking_reason = request.session[self.session_key]["hacking_reason"]
        else:
            hacking = False
            hacking_reason = None

        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        if self.session_key not in request.session:
            session_data = RawSessionDTO(
                unique_key=unique_key,
                ip=ip,
                start_time=now().isoformat(),
                end_time=now().isoformat(),
                site=site,
                device=request.user_agent.is_mobile,
                headers=headers,
                hacking=hacking,
                hacking_reason=hacking_reason,
            )

            session_filters = self.user_session_repository.get_session_filters()

            if session_filters:
                if host != "127.0.0.1" and host != "localhost":
                    if session_filters.disable_ip and self.url_parser.is_ip(host):
                        session_data.hacking = True
                        session_data.hacking_reason = "Запрос по IP"

                    if session_filters.disable_ports and port:
                        session_data.hacking = True
                        session_data.hacking_reason = "Запрос к порту"

                    for disable_url in session_filters.disable_urls.splitlines():
                        if disable_url in page_adress:
                            session_data.hacking = True
                            session_data.hacking_reason = "Запрещенный адрес"
                            break

            session_data = session_data.__dict__

            request.session[self.session_key] = session_data

        else:
            session_data = request.session[self.session_key]
            session_data["unique_key"] = unique_key

            session_filters = self.user_session_repository.get_session_filters()

            if session_filters:
                if host != "127.0.0.1" and host != "localhost":
                    if session_filters.disable_ip and self.url_parser.is_ip(host):
                        session_data["hacking"] = True
                        session_data["hacking_reason"] = "Запрос по IP"

                    if session_filters.disable_ports and port:
                        session_data["hacking"] = True
                        session_data["hacking_reason"] = "Запрос к порту"

                    for disable_url in session_filters.disable_urls.splitlines():
                        if disable_url in page_adress:
                            session_data["hacking"] = True
                            session_data["hacking_reason"] = "Запрещенный адрес"
                            break

        if self.url_parser.is_source(page_adress):
            if "source_count" not in request.session[self.session_key]:
                request.session[self.session_key]["source_count"] = 0

            request.session[self.session_key]["source_count"] += 1
        else:
            request.session[self.session_key]["pages_count"] += 1

        request.session[self.session_key]["end_time"] = now().isoformat()
        request.session[self.session_key]["unique_key"] = unique_key
        print(request.session[self.session_key], unique_key)
        request.session.save()

        session_data = request.session[self.session_key]

        self.user_session_repository.update_or_create_raw_session(unique_key=unique_key, session_data=session_data)
        self.user_session_repository.create_session_action(
            adress=page_adress,
            session_unique_key=unique_key,
        )

        if session_data["hacking"]:
            return HttpResponse(status=503)

        return self.get_response(request)
