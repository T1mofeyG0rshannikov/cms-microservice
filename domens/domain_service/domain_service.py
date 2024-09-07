import re

from domens.domain_repository.repository import get_domain_repository
from domens.domain_repository.repository_interface import DomainRepositoryInterface
from domens.domain_service.domain_service_interface import DomainServiceInterface
from domens.interfaces import SiteInterface
from user.interfaces import UserInterface


class DomainService(DomainServiceInterface):
    def __init__(self, repository: DomainRepositoryInterface):
        self.repository = repository

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

    def valid_subdomain(self, subdomain: str) -> bool:
        if not subdomain:
            return True

        site = self.repository.get_site(subdomain)
        if site and site.is_active:
            return True

        if subdomain == "www":
            return True

        return False

    def get_domain_string(self) -> str | None:
        domain = self.repository.get_domain_string()
        if domain is None:
            return None

        return domain[0]

    def get_site_name(self) -> str | None:
        domain = self.repository.get_site_name()
        if domain is None:
            return None

        return domain[0]

    def get_partners_domain_string(self) -> str:
        return self.repository.get_partners_domain_string()

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

    def get_partner_domain_model(self):
        return self.repository.get_partner_domain_model()

    def get_domain_model_from_request(self, request):
        path = request.META.get("HTTP_ORIGIN")
        host = path.replace("http://", "")
        host = host.replace("https://", "")

        domain = self.get_domain_from_host(host)
        return self.repository.get_domain(domain)

    def get_site_model(self, request):
        path = request.META.get("HTTP_ORIGIN")
        host = path.replace("http://", "")
        host = host.replace("https://", "")

        subdomain = self.get_subdomain_from_host(host)

        return self.repository.get_site(subdomain)

    def get_domain_model_by_id(self, id: int):
        return self.repository.get_domain_model_by_id(id)

    def get_domain_model(self):
        return self.repository.get_domain_model()

    def get_register_on_site(self, user: UserInterface) -> str:
        if user.register_on_domain == self.repository.get_domain_model():
            return str(user.register_on_domain)

        if user.register_on_site:
            return ".".join([str(user.register_on_site), str(user.register_on_domain)])

        return ""

    def get_random_site(self) -> SiteInterface:
        return self.repository.get_random_site()


def get_domain_service() -> DomainService:
    return DomainService(get_domain_repository())
