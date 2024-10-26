# import logging

from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.services.request_service import RequestServiceInterface
from application.sessions.dto import RawSessionDB, RawSessionDTO
from application.sessions.raw_session_service import RawSessionServiceInterface
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.persistence.models.site_statistics import PenaltyLog
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)

# logger = logging.getLogger("main")


class RawSessionService(RawSessionServiceInterface):
    def __init__(
        self,
        request_service: RequestServiceInterface,
        user_session_repository: UserSessionRepositoryInterface,
        url_parser: UrlParserInterface,
        admin_settings,
    ):
        self.request_service = request_service
        self.user_session_repository = user_session_repository
        self.url_parser = url_parser
        self.admin_settings = admin_settings

    def get_initial_raw_session(self, device):
        return RawSessionDB(
            ip=self.request_service.get_client_ip(),
            start_time=now().isoformat(),
            site=self.request_service.get_host(),
            device=device,
            headers=self.request_service.get_all_headers_to_string(),
        )

    def check_headers(self, session_data, headers: dict, session):
        session_filters = self.user_session_repository.get_session_filters()
        if session_filters:
            for session_filter_header in session_filters.headers.all():
                contain = session_filter_header.contain
                session_header_name = session_filter_header.header
                session_header_content = session_filter_header.content
                penalty = session_filter_header.penalty

                for header_name, header_content in headers.items():
                    if contain == "Присутствует":
                        if header_name == session_header_name:
                            session_data.ban_rate += penalty
                            PenaltyLog.objects.create(
                                session=session,
                                text=f"{contain}({session_header_content}) - {header_name}: {header_content}, {penalty}",
                            )
                    if header_name == session_header_name:
                        if contain == "Содержит":
                            for content in session_header_content.lower().split(","):
                                content = content.strip()
                                if content in header_content.lower():
                                    session_data.ban_rate += penalty
                                    PenaltyLog.objects.create(
                                        session=session,
                                        text=f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                    )

                        if contain == "Не содержит":
                            for content in session_header_content.lower().split(","):
                                content = content.strip()
                                if content not in header_content.lower():
                                    session_data.ban_rate += penalty
                                    PenaltyLog.objects.create(
                                        session=session,
                                        text=f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                    )

                        if contain == "Не совпадает":
                            if session_header_content.lower() != header_content.lower():
                                session_data.ban_rate += penalty
                                PenaltyLog.objects.create(
                                    session=session,
                                    text=f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                )
                        if contain == "Совпадает":
                            if session_header_content.lower() == header_content.lower():
                                session_data.ban_rate += penalty
                                PenaltyLog.objects.create(
                                    session=session,
                                    text=f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                )

                if contain == "Отсутствует":
                    if session_header_name not in headers.keys():
                        session_data.ban_rate += penalty
                        PenaltyLog.objects.create(
                            session=session,
                            text=f"{contain} - {session_header_name}, {penalty}",
                        )

        return session_data

    def filter_sessions(
        self, session_data: RawSessionDTO, host: str, path: str, port: str, headers: dict, session
    ) -> RawSessionDTO:
        session_filters = self.user_session_repository.get_session_filters()

        if session_filters:
            if host != "127.0.0.1" and host != "localhost":
                if self.url_parser.is_ip(host):
                    session_data.ban_rate += session_filters.ip_penalty
                    PenaltyLog.objects.create(
                        session=session,
                        text=f"Запрос к ip, {session_filters.ip_penalty}",
                    )

                if port:
                    session_data.ban_rate += session_filters.ports_penalty
                    PenaltyLog.objects.create(
                        session=session,
                        text=f"Запрос к порту, {session_filters.ports_penalty}",
                    )

            for disable_url in session_filters.disable_urls.splitlines():
                disable_url = disable_url.strip()
                if disable_url in path:
                    session_data.ban_rate += session_filters.disable_urls_penalty
                    PenaltyLog.objects.create(
                        session=session,
                        text=f"Запрещенный адрес(для всех), {session_filters.disable_urls_penalty}",
                    )
                    break

            if host != self.admin_settings.admin_domain and session_filters.disable_urls_sites:
                for disable_url in session_filters.disable_urls_sites.splitlines():
                    disable_url = disable_url.strip()
                    if disable_url in path:
                        session_data.ban_rate += session_filters.disable_urls_penalty
                        PenaltyLog.objects.create(
                            session=session,
                            text=f"Запрещенный адрес(для сайтов), {session_filters.session_filters.disable_urls_penalty}",
                        )
                        break

            if session_data.ban_rate >= session_filters.ban_limit:
                session_data.hacking = True

            if session_data.ban_rate >= session_filters.capcha_limit:
                session_data.show_capcha = True

        return session_data

    def success_capcha(self, session_id: int):
        increase_value = -self.user_session_repository.get_success_capcha_increase()
        self.user_session_repository.change_ban_rate(session_id, increase_value)
        self.user_session_repository.update_raw_session(session_id, show_capcha=False)
        PenaltyLog.objects.create(
            session_id=session_id,
            text=f"Успешная капча, {-increase_value}",
        )


def get_raw_session_service(
    request_service: RequestServiceInterface,
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository(),
    url_parser: UrlParserInterface = get_url_parser(),
    admin_settings=get_admin_settings(),
) -> RawSessionServiceInterface:
    return RawSessionService(
        request_service=request_service,
        user_session_repository=user_session_repository,
        url_parser=url_parser,
        admin_settings=admin_settings,
    )
