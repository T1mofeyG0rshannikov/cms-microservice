from typing import Protocol

from domain.domains.domain import DomainInterface, SiteInterface


class DomainRepositoryInterface(Protocol):
    @staticmethod
    def get_site(subdomain: str) -> SiteInterface:
        raise NotImplementedError()

    def get_domain_string(self) -> str:
        raise NotImplementedError()

    def get_site_name(self) -> str | None:
        raise NotImplementedError()

    @classmethod
    def get_partners_domain_string(self) -> str:
        raise NotImplementedError()

    def get_partner_domain_model(self) -> DomainInterface:
        raise NotImplementedError()

    @staticmethod
    def get_domain(domain: str) -> DomainInterface:
        raise NotImplementedError()

    @staticmethod
    def get_domain_model_by_id(id: int) -> DomainInterface:
        raise NotImplementedError()

    @staticmethod
    def get_domain_model() -> DomainInterface:
        raise NotImplementedError()

    def update_or_create_user_site(self, **kwargs) -> SiteInterface:
        raise NotImplementedError()

    @staticmethod
    def site_adress_exists(site_id: int, site_url: str):
        raise NotImplementedError()
