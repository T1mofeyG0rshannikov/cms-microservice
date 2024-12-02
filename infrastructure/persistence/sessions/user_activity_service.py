from django.utils.timezone import now

from application.sessions.dto import UserActivityDTO


class UserActivitySessionService:
    def __init__(self, request_service, user_session_repository):
        self.request_service = request_service
        self.user_session_repository = user_session_repository

    def get_initial_data(self, session_id: int, user_id: int = None, device: str = None, utm_source: str = None, auth: str = None):
        ip = self.request_service.get_client_ip()

        if not auth:
            auth = "login" if user_id else None

        return UserActivityDTO(
            ip=ip,
            start_time=now().isoformat(),
            site=self.request_service.get_host(),
            device=device,
            user_id=user_id,
            utm_source=utm_source,
            auth=auth,
            session_id=session_id
        )
