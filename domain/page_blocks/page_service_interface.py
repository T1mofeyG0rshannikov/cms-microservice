from typing import Protocol

from domain.page_blocks.base_block import BaseBlockInterface


class PageServiceInterface(Protocol):
    def get_page_block(self, blocks_name: str) -> BaseBlockInterface:
        raise NotImplementedError()

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError()
