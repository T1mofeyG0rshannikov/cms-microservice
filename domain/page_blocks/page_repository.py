from typing import Protocol

from domain.common.screen import ImageInterface
from domain.page_blocks.entities.base_block import PageBlockInterface
from domain.page_blocks.entities.page import PageInterface


class PageRepositoryInterface(Protocol):
    def get_catalog_block(self, slug: str) -> PageBlockInterface | None:
        raise NotImplementedError

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        raise NotImplementedError

    def get(self, id: int | None = None, url: str | None = None) -> PageInterface | None:
        raise NotImplementedError

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError

    def clone_block(self, block_id: int, block_class: type) -> None:
        raise NotImplementedError

    def get_catalog_page_template(self) -> PageInterface:
        raise NotImplementedError

    def get_landing(self, url: str) -> PageInterface:
        raise NotImplementedError

    def get_landing_logo(self, url: str) -> ImageInterface | None:
        raise NotImplementedError
