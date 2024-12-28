from application.sessions.searcher_service import SearcherService
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)


class DetectSearcherSession:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()

    def __init__(self, searcher_service: SearcherService) -> None:
        self.service = searcher_service

    def __call__(self, session_cookie: str, site: str) -> bool | int:
        if self.service.is_searcher():
            session_id = None

            if not session_cookie or ("/" not in session_cookie):
                session_data = self.service.get_initial_searcher()
                session_id = self.user_session_repository.create_searcher(**session_data.__dict__)
            else:
                session_id = int(session_cookie.split("/")[1])

            if not self.user_session_repository.is_searcher_exists_by_id(session_id):
                session_data = self.service.get_initial_searcher()
                session_id = self.user_session_repository.create_searcher(**session_data.__dict__)

            return session_id

        return False
