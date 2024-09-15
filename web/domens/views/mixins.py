from django.db.models import Q
from django.http import HttpResponseRedirect
from domens.views.views import PartnerIndexPage
from settings.models import Domain, SiteSettings
from settings.views import SettingsMixin
from template.views.base_page_not_found import BaseNotFoundPage
from user.models.site import Site

from application.services.domains.service import get_domain_service
from application.services.domains.url_parser import get_url_parser
from domain.domains.interfaces.domain_service_interface import DomainServiceInterface


class SubdomainMixin(SettingsMixin):
    domain_service: DomainServiceInterface = get_domain_service()
    url_parser = get_url_parser()

    def dispatch(self, request, *args, **kwargs):
        subdomain = self.url_parser.get_subdomain_from_host(request.get_host())
        domain = self.url_parser.get_domain_from_host(request.get_host())

        if not self.domain_service.valid_subdomain(subdomain):
            return BaseNotFoundPage.as_view()(request)

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return BaseNotFoundPage.as_view()(request)

        if Domain.objects.filter(is_partners=True).exists():
            partner_domain = self.domain_service.get_partners_domain_string()

            if domain == partner_domain and subdomain == "":
                if request.build_absolute_uri().endswith(partner_domain) or request.build_absolute_uri().endswith(
                    partner_domain + "/"
                ):
                    return PartnerIndexPage.as_view()(request)

                return BaseNotFoundPage.as_view()(request)

            if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
                return HttpResponseRedirect("/")

            if request.path.startswith("/admin/") and partner_domain in request.get_host():
                return BaseNotFoundPage.as_view()(request)

        request.domain = domain
        request.subdomain = subdomain

        return super().dispatch(request, *args, **kwargs)
