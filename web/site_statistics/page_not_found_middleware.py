from django.http import HttpRequest

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)


class PageNotFoundMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        if response.status_code == 404 and not self.url_parser.is_source(request.path) and "null" not in request.path:
            session_id = request.raw_session.id
            page_not_found_penalty = self.user_session_repository.get_page_not_found_penalty()
            self.user_session_repository.change_ban_rate(session_id, page_not_found_penalty)
            print("page not found")
        return response
