from django.utils.timezone import now

from application.services.request_service_interface import RequestServiceInterface
from application.sessions.dto import RawSessionDB
from application.usecases.user_activity.add_penalty import AddPenaltyLog
from domain.user_sessions.header_contain_enum import HeaderContainEnum
from domain.user_sessions.raw_session_service import RawSessionServiceInterface
from domain.user_sessions.repositories.raw_session_repository import (
    RawSessionRepositoryInterface,
)
from domain.user_sessions.repository import UserSessionRepositoryInterface
from domain.user_sessions.session import SessionInterface
from infrastructure.admin.admin_settings import AdminSettings, get_admin_settings
from infrastructure.persistence.repositories.raw_session_repository import (
    get_raw_session_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


class RawSessionService(RawSessionServiceInterface):
    def __init__(
        self,
        request_service: RequestServiceInterface,
        user_session_repository: UserSessionRepositoryInterface,
        raw_session_repository: RawSessionRepositoryInterface,
        url_parser: UrlParserInterface,
        penalty_logger: AddPenaltyLog,
        admin_settings: AdminSettings,
    ) -> None:
        self.request_service = request_service
        self.user_session_repository = user_session_repository
        self.raw_session_repository = raw_session_repository
        self.url_parser = url_parser
        self.penalty_logger = penalty_logger
        self.admin_settings = admin_settings

    def get_initial_raw_session(self, device: bool) -> RawSessionDB:
        return RawSessionDB(
            ip=self.request_service.get_client_ip(),
            start_time=now().isoformat(),
            site=self.request_service.get_host(),
            device=device,
            headers=self.request_service.get_all_headers_to_string(),
        )

    def check_headers(self) -> tuple[int, list[str]]:
        headers = self.request_service.get_all_headers()
        session_filter_headers = self.user_session_repository.get_session_filter_headers()
        ban_rate = 0
        penalty_logs = []

        for session_filter_header in session_filter_headers:
            contain = session_filter_header.contain
            session_header_name = session_filter_header.header
            session_header_content = session_filter_header.content
            penalty = session_filter_header.penalty

            for header_name, header_content in headers.items():
                if contain == HeaderContainEnum.have:
                    if header_name == session_header_name:
                        ban_rate += penalty

                        penalty_logs.append(
                            f"{contain}({session_header_content}) - {header_name}: {header_content}, {penalty}",
                        )

                if header_name == session_header_name:
                    if contain == HeaderContainEnum.contain:
                        for content in session_header_content.lower().split(","):
                            content = content.strip()
                            if content in header_content.lower():
                                ban_rate += penalty

                                penalty_logs.append(
                                    f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                )
                                break

                    if contain == HeaderContainEnum.not_contain:
                        for content in session_header_content.lower().split(","):
                            content = content.strip()
                            if content not in header_content.lower():
                                ban_rate += penalty

                                penalty_logs.append(
                                    f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                                )

                    if contain == HeaderContainEnum.not_match:
                        if session_header_content.lower() != header_content.lower():
                            ban_rate += penalty

                            penalty_logs.append(
                                f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                            )

                    if contain == HeaderContainEnum.match:
                        if session_header_content.lower() == header_content.lower():
                            ban_rate += penalty

                            penalty_logs.append(
                                f"{contain}({content}) - {header_name}: {header_content}, {penalty}",
                            )

            if contain == HeaderContainEnum.miss:
                if session_header_name not in headers.keys():
                    ban_rate += penalty

                    penalty_logs.append(
                        f"{contain} - {session_header_name}, {penalty}",
                    )

        return ban_rate, penalty_logs

    def filter_sessions(
        self, session_data: SessionInterface, host: str, path: str, port: str, session_id: int
    ) -> tuple[int, bool, bool]:
        session_filters = self.user_session_repository.get_session_filters()
        ban_rate = session_data.ban_rate
        hacking = session_data.hacking
        show_capcha = session_data.show_capcha

        if session_filters:
            if host != "127.0.0.1" and host != "localhost":
                if self.url_parser.is_ip(host):
                    ban_rate += session_filters.ip_penalty

                    self.penalty_logger(
                        session_id,
                        text=f"Запрос к ip, {session_filters.ip_penalty}",
                    )

                if port:
                    ban_rate += session_filters.ports_penalty

                    self.penalty_logger(
                        session_id,
                        text=f"Запрос к порту, {session_filters.ports_penalty}",
                    )

            for disable_url in session_filters.disable_urls.splitlines():
                disable_url = disable_url.strip()
                if disable_url in path:
                    ban_rate += session_filters.disable_urls_penalty

                    self.penalty_logger(
                        session_id,
                        text=f"Запрещенный адрес(для всех), {session_filters.disable_urls_penalty}",
                    )

                    break

            if host != self.admin_settings.admin_domain and session_filters.disable_urls_sites:
                for disable_url in session_filters.disable_urls_sites.splitlines():
                    disable_url = disable_url.strip()
                    if disable_url in path:
                        ban_rate += session_filters.disable_urls_penalty

                        self.penalty_logger(
                            session_id,
                            text=f"Запрещенный адрес(для сайтов), {session_filters.disable_urls_penalty}",
                        )

                        break

            if ban_rate >= session_filters.ban_limit:
                hacking = True

            if ban_rate >= session_filters.capcha_limit:
                show_capcha = True

        return ban_rate, hacking, show_capcha

    def success_capcha(self, session: SessionInterface) -> None:
        increase_value = -self.user_session_repository.get_success_capcha_increase()
        self.raw_session_repository.change_ban_rate(session.id, increase_value)
        session.show_capcha = False
        self.raw_session_repository.update(session)

        self.penalty_logger(session.id, text=f"Успешная капча, {-increase_value}")

    def create(self, device: bool) -> SessionInterface:
        session_initial_data = self.get_initial_raw_session(device)

        ban_rate, penalty_logs = self.check_headers()
        session_initial_data.ban_rate += ban_rate

        session_data = self.raw_session_repository.create(**session_initial_data.__dict__)
        for penalty_log in penalty_logs:
            self.penalty_logger(session_id=session_data.id, text=penalty_log)

        return session_data


def get_raw_session_service(
    request_service: RequestServiceInterface,
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository(),
    raw_session_repository: RawSessionRepositoryInterface = get_raw_session_repository(),
    url_parser: UrlParserInterface = get_url_parser(),
    penalty_logger=AddPenaltyLog(),
    admin_settings: AdminSettings = get_admin_settings(),
) -> RawSessionServiceInterface:
    return RawSessionService(
        request_service=request_service,
        user_session_repository=user_session_repository,
        raw_session_repository=raw_session_repository,
        url_parser=url_parser,
        penalty_logger=penalty_logger,
        admin_settings=admin_settings,
    )
