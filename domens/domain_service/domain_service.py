import re

from django.db.utils import OperationalError

from domens.domain_service.domain_service_interface import DomainServiceInterface
from domens.models import Domain, Site


class DomainService(DomainServiceInterface):
    @staticmethod
    def get_subdomain_from_host(host: str) -> str:
        host = host.replace("127.0.0.1", "localhost")

        if "localhost" in host:
            if "." not in host:
                return ""

            return host.split(".")[0]

        if host.count(".") < 2:
            return ""

        return host.split(".")[0]

    @staticmethod
    def valid_subdomain(subdomain: str) -> bool:
        if not subdomain:
            return True

        if Site.objects.filter(subdomain=subdomain).exists() and Site.objects.get(subdomain=subdomain).is_active:
            return True

        if subdomain == "www":
            return True

        return False

    @classmethod
    def get_domain_string(self) -> str | None:
        try:
            domain = Domain.objects.values_list("domain").filter(is_partners=False).first()
            if domain is None:
                return None

            return domain[0]

        except OperationalError:
            return None

    @classmethod
    def get_partners_domain_string(self) -> str:
        return Domain.objects.values_list("domain").filter(is_partners=True).first()[0]

    def get_domain_from_host(self, host: str) -> str:
        host = host.replace("127.0.0.1", "localhost")
        if ":" in host:
            host = host.split(":")[0]

        subdomain = self.get_subdomain_from_host(host)
        first_domain = host.split(".")[-1]

        domain = re.findall(f"{subdomain}.*?{first_domain}", host)[0]
        domain = re.sub(subdomain, "", domain)
        if domain[0] == ".":
            domain = domain[1::]

        return domain

    def get_domain_model(self, request):
        path = request.META.get("HTTP_ORIGIN")
        path = path.replace("http://", "")
        path = path.replace("https://", "")

        domain = self.get_domain_from_host(request.get_host())
        if Domain.objects.filter(domain=domain).exists():
            return Domain.objects.get(domain=domain)

    def get_site_model(self, request):
        path = request.META.get("HTTP_ORIGIN")
        path = path.replace("http://", "")
        path = path.replace("https://", "")

        subdomain = self.get_subdomain_from_host(request.get_host())
        if Site.objects.filter(subdomain=subdomain).exists():
            return Site.objects.get(subdomain=subdomain)


def get_domain_service() -> DomainService:
    return DomainService()
