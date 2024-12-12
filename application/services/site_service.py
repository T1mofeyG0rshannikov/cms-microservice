from domain.domains.domain_repository import DomainRepositoryInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from domain.referrals.referral import UserInterface
from domain.user.sites.site import SiteInterface
from domain.user.sites.site_repository import SiteRepositoryInterface
from domain.user.sites.site_service import SiteServiceInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)
from infrastructure.persistence.repositories.site_repository import get_site_repository
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


class SiteService(SiteServiceInterface):
    def __init__(
        self,
        domain_repository: DomainRepositoryInterface,
        site_repository: SiteRepositoryInterface,
        url_parser: UrlParserInterface,
        settings_repository: SettingsRepositoryInterface,
    ) -> None:
        self.domain_repository = domain_repository
        self.site_repository = site_repository
        self.url_parser = url_parser
        self.settings_repository = settings_repository

    def valid_subdomain(self, subdomain: str) -> bool:
        if not subdomain:
            return True

        site = self.site_repository.get(subdomain=subdomain)
        if site and site.is_active:
            return True

        if subdomain == "www":
            return True

        return False

    def get_register_on_site(self, user: UserInterface) -> str:
        if user.register_on_domain == self.domain_repository.get_domain_model():
            return str(user.register_on_domain)

        if user.register_on_site:
            return ".".join([str(user.register_on_site), str(user.register_on_domain)])

        return ""

    def get_site_from_url(self, url: str) -> SiteInterface:
        subdomain = self.url_parser.get_subdomain_from_host(url)

        if subdomain:
            site = self.site_repository.get(subdomain=subdomain)
            if site:
                return SiteInterface(
                    name=site.name,
                    domain=site.domain,
                    owner=site.owner,
                    contact_info=site.contact_info,
                    created_at=site.created_at.strftime("%d.%m.%Y"),
                    user=site.user,
                )

        domain = self.domain_repository.get_domain_model()
        settings = self.settings_repository.get_settings()

        return SiteInterface(
            name=domain.name,
            domain=domain,
            owner=settings.owner,
            contact_info=settings.contact_info,
            created_at=settings.created_at.strftime("%d.%m.%Y"),
        )


def get_domain_service(
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    site_repository: SiteRepositoryInterface = get_site_repository(),
    url_parser: UrlParserInterface = get_url_parser(),
    settings_repository: SettingsRepositoryInterface = get_settings_repository(),
) -> SiteServiceInterface:
    return SiteService(
        domain_repository=domain_repository,
        site_repository=site_repository,
        url_parser=url_parser,
        settings_repository=settings_repository,
    )
