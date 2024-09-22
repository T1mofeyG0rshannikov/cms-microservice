from typing import Any, Protocol


class CatalogServiceInterface(Protocol):
    def get_page(self, user_is_authenticated: bool, slug: str):
        raise NotImplementedError()

    def get_catalog_block(self, user_is_authenticated: bool, slug: str) -> dict[str, Any]:
        raise NotImplementedError()

    def get_catalog_cover(self, slug: str):
        raise NotImplementedError()

    def set_catalog_block(self, page, user_is_authenticated: bool, slug: str):
        raise NotImplementedError()

    def set_catalog_cover(self, serialized_page: dict[Any, Any], slug: str):
        raise NotImplementedError()
