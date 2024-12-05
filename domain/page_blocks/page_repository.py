from collections.abc import Iterable
from typing import Protocol

from domain.page_blocks.entities.base_block import (
    BaseBlockInterface,
    CatalogBlockInterface,
)
from domain.page_blocks.entities.page import PageInterface


class PageRepositoryInterface(Protocol):
    def get_catalog_block(self, slug: str) -> CatalogBlockInterface:
        raise NotImplementedError

    def get_catalog_cover(self, slug: str) -> BaseBlockInterface:
        raise NotImplementedError

    def get_page_by_id(self, id: int) -> PageInterface:
        raise NotImplementedError

    def get_page_by_url(self, url: str) -> PageInterface:
        raise NotImplementedError

    def get_page_blocks(self, page: PageInterface) -> Iterable[BaseBlockInterface]:
        raise NotImplementedError

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError

    def get_catalog_page_template(self) -> PageInterface:
        raise NotImplementedError
