from typing import Protocol


class UrlParserInterface(Protocol):
    @staticmethod
    def get_subdomain_from_host(host: str) -> str:
        raise NotImplementedError()

    def get_domain_from_host(self, host: str) -> str:
        raise NotImplementedError()
