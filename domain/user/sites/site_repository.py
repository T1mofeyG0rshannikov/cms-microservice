from collections.abc import Iterable
from typing import Protocol

from domain.common.screen import FileInterface
from domain.user.entities import SiteInterface


class SiteRepositoryInterface(Protocol):
    def update_or_create(
        self,
        user_id: int,
        subdomain: str,
        name: str,
        owner: str | None = None,
        logo: FileInterface | None = None,
        **kwargs
    ) -> tuple[SiteInterface, bool]:
        raise NotImplementedError

    def get(
        self, subdomain: str | None = None, user_id: int | None = None, domain: str | None = None
    ) -> SiteInterface | None:
        raise NotImplementedError

    def all(self) -> Iterable[SiteInterface]:
        raise NotImplementedError
