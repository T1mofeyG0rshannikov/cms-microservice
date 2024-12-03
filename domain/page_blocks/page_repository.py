from typing import Protocol

from domain.page_blocks.base_block import BaseBlockInterface
from domain.page_blocks.page import PageInterface


class PageRepositoryInterface(Protocol):
    def get_page_by_id(self, id: int) -> PageInterface:
        raise NotImplementedError

    def get_page_by_url(self, url: str) -> PageInterface:
        raise NotImplementedError

    def get_page_block(self, blocks_name: str) -> BaseBlockInterface:
        raise NotImplementedError

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError
