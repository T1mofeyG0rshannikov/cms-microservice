from application.usecases.user_activity.add_penalty import AddPenaltyLog
from domain.user_sessions.repositories.raw_session_repository import (
    RawSessionRepositoryInterface,
)
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.raw_session_repository import (
    get_raw_session_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


class BaseSessionMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()
    penalty_logger = AddPenaltyLog()
    raw_session_repository: RawSessionRepositoryInterface = get_raw_session_repository()
