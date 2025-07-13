from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)

from application.services.site_service import get_site_service
from web.site_statistics.middlewares.base import BaseSessionMiddleware
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.user.sites.site_service import SiteServiceInterface
from infrastructure.admin.admin_settings import AdminSettings, get_admin_settings
from infrastructure.persistence.models.settings import SiteSettings
from infrastructure.persistence.models.user.site import Site
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser
from web.settings.views.views import PartnerIndexPage
from web.template.views.base_page_not_found import BaseNotFoundPage


class DomainMiddleware(BaseSessionMiddleware):
    site_service: SiteServiceInterface = get_site_service()
    url_parser: UrlParserInterface = get_url_parser()
    admin_settings: AdminSettings = get_admin_settings()
    domain_repository: DomainRepositoryInterface = get_domain_repository()

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if self.url_parser.is_source(request.path):
            return self.get_response(request)

        host = request.get_host()
        path = request.path[1::]

        subdomain = self.url_parser.get_subdomain_from_host(host)
        domain = self.url_parser.get_domain_from_host(host)
        partner_domain = self.domain_repository.get_partners_domain_string()

        request.partner_domain = partner_domain
        request.domain = domain
        request.subdomain = subdomain
        request.landing = self.domain_repository.landing_domain_exists(domain)

        if self.admin_settings.admin_domain in host:
            valid_url = False
            for url in self.admin_settings.valid_admin_urls:
                if path.startswith(url):
                    valid_url = True
                    break

            if not valid_url:
                return HttpResponseNotFound()

        if not self.site_service.valid_subdomain(subdomain):
            return BaseNotFoundPage.as_view()(request)

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return BaseNotFoundPage.as_view()(request)

        if partner_domain:
            if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
                return HttpResponse("<h1>Привет :)</h1>")

            if domain == partner_domain and subdomain == "":
                uri = request.build_absolute_uri()
                if uri.endswith(partner_domain) or uri.endswith(partner_domain + "/"):
                    return PartnerIndexPage.as_view()(request)

                return BaseNotFoundPage.as_view()(request)

            if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
                return HttpResponseRedirect("/")

        return self.get_response(request)


# 63
