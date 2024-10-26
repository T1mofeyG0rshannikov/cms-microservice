from typing import Protocol

from domain.domains.domain import DomainInterface, SiteInterface


class DomainRepositoryInterface(Protocol):
    def get_site(self, subdomain: str) -> SiteInterface:
        raise NotImplementedError

    def get_domain_string(self) -> str:
        raise NotImplementedError

    def get_site_name(self) -> str | None:
        raise NotImplementedError

    @classmethod
    def get_partners_domain_string(self) -> str:
        raise NotImplementedError

    def get_partner_domain_model(self) -> DomainInterface:
        raise NotImplementedError

    def get_domain(self, domain: str) -> DomainInterface:
        raise NotImplementedError

    def get_domain_model_by_id(self, id: int) -> DomainInterface:
        raise NotImplementedError

    def get_domain_model(self) -> DomainInterface:
        raise NotImplementedError

    def update_or_create_user_site(self, **kwargs) -> SiteInterface:
        raise NotImplementedError

    def site_adress_exists(self, site_id: int, site_url: str):
        raise NotImplementedError
