from collections.abc import Iterable
from typing import Protocol

from domain.user.sites.site import SiteInterface


class SiteRepositoryInterface(Protocol):
    def update_or_create(self, **kwargs) -> SiteInterface:
        raise NotImplementedError

    def get(self, subdomain: str = None, user_id: int = None, domain: str = None) -> SiteInterface:
        raise NotImplementedError

    def all(self) -> Iterable[SiteInterface]:
        raise NotImplementedError
