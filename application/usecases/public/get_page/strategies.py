from abc import abstractmethod

from application.mappers.page import from_orm_to_page
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.blocks.common import BaseBlock


class GetPageStrategy:
    @abstractmethod
    def execute(self, url: str | None = None, user_is_authenticated: bool = False) -> PageInterface | None:
        ...


class GetCatalogPageStrategy(GetPageStrategy):
    def __init__(
        self,
        page_repository: PageRepositoryInterface,
    ) -> None:
        self.r = page_repository

    def execute(self, url: str, user_is_authenticated: bool) -> PageInterface | None:
        catalog = self.r.get_catalog_block(url)
        if catalog is None:
            return None

        catalog.user_is_authenticated = user_is_authenticated

        page, blocks = self.r.get_catalog_page_template()

        cover = self.r.get_catalog_cover(url)

        self.set_block(blocks, catalog)
        self.set_block(blocks, cover)

        page.title = catalog.product_type.name

        return from_orm_to_page(page, blocks)

    def set_block(self, blocks, block: BaseBlock) -> None:
        for ind, page_block in enumerate(blocks):
            if isinstance(page_block, type(block)):
                blocks[ind] = block


class GetDefaultPageStrategy(GetPageStrategy):
    def __init__(
        self,
        page_repository: PageRepositoryInterface,
    ) -> None:
        self.r = page_repository

    def execute(self, url: str | None = None, **kwargs) -> PageInterface | None:
        return self.r.get(url=url)
