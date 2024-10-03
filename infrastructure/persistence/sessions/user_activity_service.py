from django.utils.timezone import now

from application.sessions.dto import UserActivityDTO


class UserActivitySessionService:
    def __init__(self, request_service, user_session_repository):
        self.request_service = request_service
        self.user_session_repository = user_session_repository

    def get_initial_data(self, site, user_id, unique_key, device, utm_source):
        ip = self.request_service.get_client_ip()
        hacking = False
        hacking_reason = None
        auth = "login" if user_id else None

        user_session_data = UserActivityDTO(
            unique_key=unique_key,
            ip=ip,
            start_time=now().isoformat(),
            end_time=now().isoformat(),
            site=site,
            device=device,
            user_id=user_id,
            utm_source=utm_source,
            hacking=hacking,
            hacking_reason=hacking_reason,
            auth=auth,
        )

        return user_session_data
