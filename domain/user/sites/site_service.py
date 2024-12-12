from typing import Protocol

from domain.user.sites.site import SiteInterface
from domain.user.user import UserInterface


class SiteServiceInterface(Protocol):
    def valid_subdomain(self, subdomain: str) -> bool:
        raise NotImplementedError

    def get_site_from_url(self, url: str) -> SiteInterface:
        raise NotImplementedError

    def get_register_on_site(self, user: UserInterface) -> str:
        raise NotImplementedError
