from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from domain.domains.domain_repository import DomainRepositoryInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser
from web.blocks.views import BasePageView


class LandingMiddleware:
    settings_repository: SettingsRepositoryInterface = get_settings_repository()
    domain_repository: DomainRepositoryInterface = get_domain_repository()
    page_repository: PageRepositoryInterface = get_page_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: RequestInterface):
        path = request.path
        if self.url_parser.is_source(path):
            return self.get_response(request)

        if self.domain_repository.landing_domain_exists(request.domain):
            request.landing = True
            landing_page = self.page_repository.get_landing(url=path[1::])
            if not landing_page:
                return HttpResponse(status=503)

            response = BasePageView.as_view()(request, page=landing_page)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            try:
                response.render()
            except:
                pass

            return response

        request.landing = False

        return self.get_response(request)
