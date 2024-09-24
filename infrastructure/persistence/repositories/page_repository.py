from domain.page_blocks.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.blocks.common import Page


class PageRepository(PageRepositoryInterface):
    def get_page_by_id(self, id: int) -> PageInterface:
        return Page.objects.get(id=id)

    def get_page_by_url(self, url: str) -> PageInterface:
        try:
            return Page.objects.prefetch_related("blocks").get(url=url)
        except Page.DoesNotExist:
            return None


def get_page_repository() -> PageRepositoryInterface:
    return PageRepository()
