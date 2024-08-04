from django.db.models import Q
from django.http import HttpResponseRedirect

from common.views.page_not_found import BaseNotFoundPage
from domens.domain_service.domain_service import DomainService, get_domain_service
from domens.domain_service.domain_service_interface import DomainServiceInterface
from domens.models import Domain, Site
from domens.views.views import PartnerIndexPage
from settings.models import SiteSettings
from settings.views import SettingsMixin


class SubdomainMixin(SettingsMixin):
    domain_service: DomainServiceInterface = get_domain_service()

    def dispatch(self, request, *args, **kwargs):
        subdomain = self.domain_service.get_subdomain_from_url(request)
        domain = self.domain_service.get_domain_from_url(request)

        if not self.domain_service.valid_subdomain(subdomain):
            return BaseNotFoundPage.as_view()(request)

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return BaseNotFoundPage.as_view()(request)

        if Domain.objects.filter(is_partners=True).exists():
            partner_domain = DomainService.get_partners_domain_string()

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
