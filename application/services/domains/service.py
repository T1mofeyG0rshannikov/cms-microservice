from domain.domains.domain_repository import DomainRepositoryInterface
from domain.domains.domain_service import DomainServiceInterface
from domain.domains.site import DomainInterface, SiteInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from domain.referrals.referral import UserInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


class DomainService(DomainServiceInterface):
    def __init__(
        self,
        repository: DomainRepositoryInterface,
        url_parser: UrlParserInterface,
        settings_repository: SettingsRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.url_parser = url_parser
        self.settings_repository = settings_repository

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

    def get_partner_domain_model(self) -> DomainInterface:
        return self.repository.get_partner_domain_model()

    def get_domain_model(self) -> DomainInterface:
        return self.repository.get_domain_model()

    def get_register_on_site(self, user: UserInterface) -> str:
        if user.register_on_domain == self.repository.get_domain_model():
            return str(user.register_on_domain)

        if user.register_on_site:
            return ".".join([str(user.register_on_site), str(user.register_on_domain)])

        return ""

    def get_domain_model_from_request(self, host: str):
        return self.repository.get_domain(self.url_parser.get_domain_from_host(host))

    def get_site_from_url(self, url: str) -> SiteInterface:
        subdomain = self.url_parser.get_subdomain_from_host(url)

        if subdomain:
            site = self.get_site_by_name(subdomain)
            if site:
                return SiteInterface(
                    name=site.name,
                    domain=site.domain,
                    owner=site.owner,
                    contact_info=site.contact_info,
                    created_at=site.created_at.strftime("%d.%m.%Y"),
                    user=site.user,
                )

        domain = self.get_domain_model()
        settings = self.settings_repository.get_settings()

        return SiteInterface(
            name=domain.name,
            domain=domain,
            owner=settings.owner,
            contact_info=settings.contact_info,
            created_at=settings.created_at.strftime("%d.%m.%Y"),
        )

    def get_site_by_name(self, site_name: str) -> SiteInterface:
        return self.repository.get_site(site_name)


def get_domain_service(
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    url_parser: UrlParserInterface = get_url_parser(),
    settings_repository: SettingsRepositoryInterface = get_settings_repository(),
) -> DomainServiceInterface:
    return DomainService(repository=domain_repository, url_parser=url_parser, settings_repository=settings_repository)
