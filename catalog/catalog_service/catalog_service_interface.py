from typing import Any, Protocol

from user.interfaces import UserInterface


class CatalogServiceInterface(Protocol):
    def get_page(self, user: UserInterface, slug: str):
        raise NotImplementedError()

    def get_catalog_block(self, user: UserInterface, slug: str) -> dict[str, Any]:
        raise NotImplementedError()

    def get_catalog_cover(self, slug: str):
        raise NotImplementedError()

    def set_catalog_block(self, page, user: UserInterface, slug: str):
        raise NotImplementedError()

    def set_catalog_cover(self, serialized_page: dict[Any, Any], slug: str):
        raise NotImplementedError()
