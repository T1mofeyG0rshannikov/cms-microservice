from typing import Protocol

from domain.domains.site import DomainInterface, SiteInterface


class DomainServiceInterface(Protocol):
    def get_domain_model(self) -> DomainInterface | None:
        raise NotImplementedError

    def valid_subdomain(self, subdomain: str) -> bool:
        raise NotImplementedError

    def get_domain_string(self) -> str | None:
        raise NotImplementedError

    def get_partners_domain_string(self) -> str | None:
        raise NotImplementedError

    def get_partner_domain_model(self) -> DomainInterface | None:
        raise NotImplementedError

    def get_domain_from_host(self, host: str) -> str:
        raise NotImplementedError

    def get_site_name(self) -> str | None:
        raise NotImplementedError

    def get_site_from_url(self, url: str) -> SiteInterface:
        raise NotImplementedError

    def get_site_by_name(self, name: str) -> SiteInterface:
        raise NotImplementedError

    def get_random_site(self) -> SiteInterface:
        raise NotImplementedError
