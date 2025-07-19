from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.repositories.page_repository import get_page_repository


class ClonePage:
    def __init__(self, page_repository: PageRepositoryInterface) -> None:
        self.r = page_repository

    def __call__(self, page_id: int) -> None:
        self.r.clone_page(page_id)


def get_clone_page(page_repository: PageRepositoryInterface = get_page_repository()) -> ClonePage:
    return ClonePage(page_repository=page_repository)
