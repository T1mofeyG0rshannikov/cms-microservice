from typing import Protocol, Iterable

from domain.domains.site import DomainInterface, SiteInterface


class DomainRepositoryInterface(Protocol):
    @classmethod
    def get_partners_domain_string(self) -> str:
        raise NotImplementedError

    def get_site(self, subdomain: str) -> SiteInterface:
        raise NotImplementedError

    def get_domain_string(self) -> str:
        raise NotImplementedError

    def get_site_name(self) -> str | None:
        raise NotImplementedError

    def get_partner_domain_model(self) -> DomainInterface:
        raise NotImplementedError

    def get_domain(self, domain: str) -> DomainInterface:
        raise NotImplementedError

    def get_domain_model(self) -> DomainInterface:
        raise NotImplementedError

    def update_or_create_user_site(self, **kwargs) -> SiteInterface:
        raise NotImplementedError

    def site_adress_exists(self, site_id: int, site_url: str) -> bool:
        raise NotImplementedError
    
    def get_random_site(self) -> SiteInterface:
        raise NotImplementedError
    
    def get_domain_sites(self, domain: str) -> Iterable[SiteInterface]:
        raise NotImplementedError
