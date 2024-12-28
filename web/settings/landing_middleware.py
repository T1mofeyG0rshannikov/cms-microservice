from django.http import HttpResponse

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
from web.blocks.views import BasePageView
from web.site_statistics.base_session_middleware import BaseSessionMiddleware


class LandingMiddleware(BaseSessionMiddleware):
    settings_repository: SettingsRepositoryInterface = get_settings_repository()
    domain_repository: DomainRepositoryInterface = get_domain_repository()
    page_repository: PageRepositoryInterface = get_page_repository()

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: RequestInterface):
        if self.domain_repository.landing_domain_exists(request.domain):
            landing_page = self.page_repository.get_landing(url=request.path[1::])
            if not landing_page:
                return HttpResponse(status=503)

            return BasePageView.as_view(page=landing_page)

        return self.get_response(request)
