from collections.abc import Iterable
from typing import Protocol

from domain.domains.entities.site import DomainInterface, SiteInterface


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

    def get_domain_sites(self, domain: str) -> Iterable[SiteInterface]:
        raise NotImplementedError

    def get_user_site(self, user_id: int) -> SiteInterface:
        raise NotImplementedError

    def get_all_sites(self) -> Iterable[SiteInterface]:
        raise NotImplementedError
