from application.sessions.detetc_single_page_session import DetectSinglePageSession
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)

if __name__ == "__main__":
    detect_single_page_session = DetectSinglePageSession(get_user_session_repository())
    detect_single_page_session()
