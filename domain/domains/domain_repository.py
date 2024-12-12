from typing import Protocol

from domain.domains.domain import DomainInterface


class DomainRepositoryInterface(Protocol):
    @classmethod
    def get_partners_domain_string(self) -> str:
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
