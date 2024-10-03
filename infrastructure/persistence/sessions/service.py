from django.utils.timezone import now

from application.sessions.dto import RawSessionDTO


class RawSessionService:
    def __init__(self, request_service, user_session_repository):
        self.request_service = request_service
        self.user_session_repository = user_session_repository

    def get_initial_raw_session(self, unique_key, path, site, device):
        headers = self.request_service.get_all_headers_to_string()
        ip = self.request_service.get_client_ip()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None

        session_data = RawSessionDTO(
            unique_key=unique_key,
            ip=ip,
            start_time=now().isoformat(),
            end_time=now().isoformat(),
            site=site,
            device=device,
            headers=headers,
        )

        session_data = self.filter_sessions(session_data, host, page_adress, port)

        return session_data

    def filter_sessions(self, session_data: RawSessionDTO, host: str, page_adress: str, port: str) -> RawSessionDTO:
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

        return session_data
