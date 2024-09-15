from typing import Protocol

from domens.interfaces import DomainInterface


class DomainServiceInterface(Protocol):
    def valid_subdomain(self, subdomain: str) -> bool:
        raise NotImplementedError()

    def get_domain_string(self) -> str | None:
        raise NotImplementedError()

    def get_partners_domain_string(self) -> str | None:
        raise NotImplementedError()

    def get_partner_domain_model(self) -> DomainInterface | None:
        raise NotImplementedError()

    def get_domain_from_host(self, host: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def get_domain_model_by_id(id: int) -> DomainInterface | None:
        raise NotImplementedError()

    @staticmethod
    def get_domain_model() -> DomainInterface | None:
        raise NotImplementedError()

    def get_site_name(self) -> str | None:
        raise NotImplementedError()
