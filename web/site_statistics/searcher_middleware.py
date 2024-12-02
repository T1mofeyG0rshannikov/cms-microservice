from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.sessions.searcher_service import SearcherService
from application.usecases.user_activity.searchers import DetectSearcherSession
from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.requests.service import get_request_service
from web.site_statistics.base_session_middleware import BaseSessionMiddleware


class SearcherMiddleware(BaseSessionMiddleware):
    admin_settings = get_admin_settings()
    cookie_name = settings.SEARCHER_COOKIE_NAME
    
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        searcher_service = SearcherService(get_request_service(request), self.user_session_repository)
        detect_searcher_session = DetectSearcherSession(searcher_service)
        
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
            
        search_session = detect_searcher_session(request.COOKIES.get(self.cookie_name), site)
        if search_session:
            request.searcher = True

            session_filters = self.user_session_repository.get_session_filters()
            if self.admin_settings.admin_domain in request.get_host() and session_filters.hide_admin:
                return HttpResponse(status=503)

            self.user_session_repository.create_searcher_log(searcher_id=search_session, adress=page_adress, time=now())

            return self.get_response(request)

        request.searcher = False
        return self.get_response(request)
