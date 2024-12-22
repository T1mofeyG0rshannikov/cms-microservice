from infrastructure.persistence.repositories.user_session_repository import (
    UserSessionRepository,
    get_user_session_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


class CreateUserSesssionLog:
    def __init__(self, repository: UserSessionRepository, url_parser: UrlParserInterface) -> None:
        self.repository = repository
        self.url_parser = url_parser

    def __call__(self, request: RequestInterface, text: str) -> None:
        path = request.META.get("HTTP_REFERER")
        if not path:
            path = request.build_absolute_uri()

        adress = self.url_parser.remove_protocol(path)

        self.repository.create_user_action(
            adress=adress,
            text=text,
            session_id=request.user_session_id,
        )


def get_create_user_session_log(
    repository: UserSessionRepository = get_user_session_repository(), url_parser: UrlParserInterface = get_url_parser()
) -> CreateUserSesssionLog:
    return CreateUserSesssionLog(repository, url_parser)
