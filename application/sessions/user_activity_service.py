from django.utils.timezone import now

from application.services.request_service_interface import RequestServiceInterface
from application.sessions.dto import UserSessionDB


class UserActivitySessionService:
    def __init__(self, request_service: RequestServiceInterface) -> None:
        self.request_service = request_service

    def get_initial_data(
        self, session_id: int, user_id: int = None, device: str = None, auth: str = None
    ) -> UserSessionDB:
        ip = self.request_service.get_client_ip()

        if not auth:
            auth = "login" if user_id else None

        return UserSessionDB(
            ip=ip,
            start_time=now().isoformat(),
            site=self.request_service.get_host(),
            device=device,
            user_id=user_id,
            auth=auth,
            session_id=session_id,
        )
