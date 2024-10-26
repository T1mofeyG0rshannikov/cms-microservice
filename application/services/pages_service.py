from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.page_blocks.page_service_interface import PageServiceInterface
from infrastructure.persistence.repositories.page_repository import get_page_repository


class PageService(PageServiceInterface):
    def __init__(self, page_repository: PageRepositoryInterface) -> None:
        self.page_repository = page_repository

    def clone_page(self, page_id: int) -> None:
        self.page_repository.clone_page(page_id)


def get_page_service(page_repository: PageRepositoryInterface = get_page_repository()) -> PageServiceInterface:
    return PageService(page_repository=page_repository)
