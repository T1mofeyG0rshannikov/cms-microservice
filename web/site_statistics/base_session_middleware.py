from application.common.base_url_parser import UrlParserInterface
from application.usecases.user_activity.add_penalty import AddPenaltyLog
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.user_session_repository import get_user_session_repository
from infrastructure.url_parser import get_url_parser


class BaseSessionMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()
    penalty_logger = AddPenaltyLog()