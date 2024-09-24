from typing import Protocol

from domain.page_blocks.page import PageInterface


class PageRepositoryInterface(Protocol):
    def get_page_by_id(self, id: int) -> PageInterface:
        raise NotImplementedError()

    def get_page_by_url(self, url: str) -> PageInterface:
        raise NotImplementedError()
