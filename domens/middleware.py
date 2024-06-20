import re

from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect

from domens.models import Domain, Site
from settings.models import SiteSettings


class DomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_domain(self, request):
        host = request.get_host()
        host = host.replace("127.0.0.1", "localhost")
        if ":" in host:
            host = host.split(":")[0]

        subdomain = self.get_subdomain(request)
        first_domain = host.split(".")[-1]
        #print(first_domain)

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

    def __call__(self, request):
        partner_domain = Domain.objects.filter(is_partners=True).first().domain

        subdomain = self.get_subdomain(request)
        domain = self.get_domain(request)

        #print(domain, "domain")
        #print(subdomain, "subdomain")

        if not self.valid_subdomain(subdomain):
            return HttpResponseNotFound("404 Subdomen not found")

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return HttpResponseNotFound("404 Subdomen not found")

        partner_domain = Domain.objects.filter(is_partners=True).first().domain
        if domain == partner_domain and not subdomain and self.request.path != "":
            return HttpResponseNotFound("404 Page not found")

        if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
            return HttpResponseRedirect("/")

        if request.path.startswith("/admin/") and partner_domain in request.get_host():
            return HttpResponseNotFound("404 Page not found")

        request.domain = domain
        request.subdomain = subdomain

        return self.get_response(request)
