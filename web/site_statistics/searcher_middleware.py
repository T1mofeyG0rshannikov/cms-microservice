from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.sessions.searcher_service import SearcherService
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.requests.service import get_request_service


class SearcherMiddleware:
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    admin_settings = get_admin_settings()
    cookie_name = settings.SEARCHER_COOKIE_NAME

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        searcher_service = SearcherService(get_request_service(request), self.user_session_repository)

        if searcher_service.is_searcher():
            path = request.get_full_path()
            site = request.get_host()
            page_adress = site + path

            cookie = request.COOKIES.get(self.cookie_name)

            # cookie = None
            session_id = None

            if not cookie or ("/" not in cookie):
                session_data = searcher_service.get_initial_searcher()
                session_db = self.user_session_repository.create_searcher(**session_data.__dict__)
                session_id = session_db.id
            else:
                session_id = int(cookie.split("/")[1])

            if not self.user_session_repository.is_searcher_exists_by_id(session_id):
                session_data = searcher_service.get_initial_searcher(site)
                session_db = self.user_session_repository.create_searcher(**session_data.__dict__)
                session_id = session_db.id

            request.searcher = True

            session_filters = self.user_session_repository.get_session_filters()
            if self.admin_settings.admin_domain in request.get_host() and session_filters.hide_admin:
                return HttpResponse(status=503)

            self.user_session_repository.create_searcher_log(searcher_id=session_id, adress=page_adress, time=now())

            return self.get_response(request)

        request.searcher = False
        return self.get_response(request)
