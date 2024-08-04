import re

from django.db.models import Q
from django.http import HttpResponseRedirect

from common.views.page_not_found import BaseNotFoundPage
from domens.get_domain import get_partners_domain_string
from domens.models import Domain, Site
from domens.views.views import PartnerIndexPage
from settings.models import SiteSettings
from settings.views import SettingsMixin


class SubdomainMixin(SettingsMixin):
    def get_domain(self, request):
        host = request.get_host()
        host = host.replace("127.0.0.1", "localhost")
        if ":" in host:
            host = host.split(":")[0]

        subdomain = self.get_subdomain(request)
        first_domain = host.split(".")[-1]

        domain = re.findall(f"{subdomain}.*?{first_domain}", host)[0]
        domain = re.sub(subdomain, "", domain)
        if domain[0] == ".":
            domain = domain[1::]

        return domain

    def get_subdomain(self, request):
        host = request.get_host()
        host = host.replace("127.0.0.1", "localhost")

        if "localhost" in host:
            if "." not in host:
                return ""

            return host.split(".")[0]

        if host.count(".") < 2:
            return ""

        return host.split(".")[0]

    def valid_subdomain(self, subdomain: str) -> bool:
        if not subdomain:
            return True

        if Site.objects.filter(subdomain=subdomain).exists() and Site.objects.get(subdomain=subdomain).is_active:
            return True

        if subdomain == "www":
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        subdomain = self.get_subdomain(request)
        domain = self.get_domain(request)

        if not self.valid_subdomain(subdomain):
            return BaseNotFoundPage.as_view()(request)

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return BaseNotFoundPage.as_view()(request)

        if Domain.objects.filter(is_partners=True).exists():
            partner_domain = get_partners_domain_string()

            if domain == partner_domain and subdomain == "":
                if request.path == "":
                    return PartnerIndexPage.as_view()(request)

                return BaseNotFoundPage.as_view()(request)

            if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
                return HttpResponseRedirect("/")

            if request.path.startswith("/admin/") and partner_domain in request.get_host():
                return BaseNotFoundPage.as_view()(request)

        request.domain = domain
        request.subdomain = subdomain

        return super().dispatch(request, *args, **kwargs)
