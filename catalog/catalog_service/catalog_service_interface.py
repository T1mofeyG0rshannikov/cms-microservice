from typing import Protocol


class CatalogServiceInterface(Protocol):
    def get_page(self, user, slug: str):
        raise NotImplementedError()

    def get_catalog_block(self, slug: str):
        raise NotImplementedError()

    def get_catalog_cover(self, slug: str):
        raise NotImplementedError()

    def set_catalog_block(self, page, slug: str):
        raise NotImplementedError()

    def set_catalog_cover(self, serialized_page, slug: str):
        raise NotImplementedError()
