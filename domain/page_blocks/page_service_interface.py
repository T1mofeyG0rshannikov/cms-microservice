from typing import Protocol


class PageServiceInterface(Protocol):
    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError
