from typing import Protocol

from django.http.request import HttpRequest

from domens.models import Domain, Site


class DomainServiceInterface(Protocol):
    @staticmethod
    def get_subdomain_from_host(host: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def valid_subdomain(subdomain: str) -> bool:
        raise NotImplementedError()

    @classmethod
    def get_domain_string(self) -> str | None:
        raise NotImplementedError()

    @classmethod
    def get_partners_domain_string(self) -> str | None:
        raise NotImplementedError()

    def get_partner_domain_model(self) -> Domain | None:
        raise NotImplementedError()

    def get_domain_from_host(self, host: str) -> str:
        raise NotImplementedError()

    def get_domain_model_from_request(self, request: HttpRequest) -> Domain | None:
        raise NotImplementedError()

    def get_site_model(self, request: HttpRequest) -> Site | None:
        raise NotImplementedError()
