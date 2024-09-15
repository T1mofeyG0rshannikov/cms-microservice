from domens.domain_repository.repository_interface import DomainRepositoryInterface
from domens.interfaces import SiteInterface
from user.interfaces import UserInterface

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.domains.interfaces.domain_service_interface import DomainServiceInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)


class DomainService(DomainServiceInterface):
    def __init__(self, repository: DomainRepositoryInterface, url_parser: UrlParserInterface):
        self.repository = repository
        self.url_parser = url_parser

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

    def get_partner_domain_model(self):
        return self.repository.get_partner_domain_model()

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

    def get_domain_model_from_request(self, host: str):
        domain = self.url_parser.get_domain_from_host(host)
        return self.repository.get_domain(domain)


def get_domain_service() -> DomainService:
    return DomainService(get_domain_repository(), get_url_parser())
