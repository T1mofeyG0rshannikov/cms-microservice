from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.logging.tasks import create_raw_log
from infrastructure.persistence.models.site_statistics import SessionAction
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.requests.service import RequestService


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    session_key = settings.RAW_SESSION_SESSION_KEY
    actions = []

    def __init__(self, get_response):
        self.get_response = get_response

    def create_actions(self):
        """books = [
            Book(title='Book 1', author='Author 1', publish_date=date(2023, 1, 1)),
            Book(title='Book 2', author='Author 2', publish_date=date(2023, 1, 2)),
        ]"""

        SessionAction.objects.bulk_create(self.actions)

    def __call__(self, request: HttpRequest):
        # from infrastructure.logging.tasks import create_raw_log
        request_service = RequestService(request)

        unique_key = request.session.session_key
        if not unique_key:
            request.session.save()

        unique_key = request.session.session_key

        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None
        """ip = request_service.get_client_ip()

        if self.session_key in request.session:
            hacking = request.session[self.session_key]["hacking"]
            hacking_reason = request.session[self.session_key]["hacking_reason"]
        else:
            hacking = False
            hacking_reason = None


        if self.session_key not in request.session:
            headers = request_service.get_all_headers_to_string()

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
            print(unique_key, "new")

            request.session[self.session_key] = session_data

        else:
            request.session[self.session_key]["new"] = False
            session_data = request.session[self.session_key]
            if not "unique_key" in session_data:
                session_data["unique_key"] = unique_key

            #session_data["unique_key"] = unique_key

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
                            break"""

        if self.user_session_repository.is_raw_session_exists(unique_key):
            session_data = RawSessionDTO.from_dict(
                self.user_session_repository.get_raw_session(unique_key).__dict__
            ).__dict__

            request.session[self.session_key]["new"] = False
            session_data["new"] = False

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
        else:
            if self.session_key not in request.session:
                request.session[self.session_key] = {}

            request.session[self.session_key]["new"] = True

            headers = request_service.get_all_headers_to_string()
            ip = request_service.get_client_ip()

            hacking = False
            hacking_reason = None

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
            self.user_session_repository.update_or_create_raw_session(unique_key, session_data)
            print(unique_key, "new")

            # request.session[self.session_key] = session_data

        request.session.save()

        """if self.url_parser.is_source(path):
            #if "source_count" not in request.session[self.session_key]:
            #    request.session[self.session_key]["source_count"] = 0
            print(path, self.url_parser.is_source(path))
            session_data["source_count"] += 1
        else:
            session_data["pages_count"] += 1"""

        session_data["end_time"] = now().isoformat()
        # request.session[self.session_key]["unique_key"] = unique_key

        # session_data = request.session[self.session_key]
        if not self.user_session_repository.is_raw_session_exists(session_data["unique_key"]):
            request.session[self.session_key]["new"] = True
            # session_data = request.session[self.session_key]

        request.session.save()
        if "pages_count" in session_data:
            del session_data["pages_count"]
        if "source_count" in session_data:
            del session_data["source_count"]

        create_raw_log.delay(unique_key, session_data, page_adress, now(), path)
        """user_session_repository = get_user_session_repository()
        session = user_session_repository.update_or_create_raw_session(unique_key=unique_key, session_data=session_data)
        #print(session, session.unique_key, unique_key)
        if session:
            user_session_repository.create_session_action(
                adress=page_adress,
                session_unique_key=unique_key,
        )"""

        if session_data["hacking"]:
            return HttpResponse(status=503)

        return self.get_response(request)
