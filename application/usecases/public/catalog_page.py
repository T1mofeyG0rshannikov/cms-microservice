from application.mappers.page import from_orm_to_page
from infrastructure.persistence.models.blocks.common import BaseBlock
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.repositories.page_repository import get_page_repository


class GetCatalogPage:
    def __init__(
        self,
        page_repository: PageRepositoryInterface,
    ) -> None:
        self.page_repository = page_repository

    def __call__(self, slug: str, user_is_authenticated: bool) -> PageInterface | None:
        catalog = self.page_repository.get_catalog_block(slug)
        if catalog is None:
            return None

        catalog.user_is_authenticated = user_is_authenticated

        page, blocks = self.page_repository.get_catalog_page_template()

        cover = self.page_repository.get_catalog_cover(slug)
        
        self.set_catalog_block(blocks, catalog)
        self.set_catalog_block(blocks, cover)

        page.title = catalog.product_type.name

        return from_orm_to_page(page, blocks)

    def set_catalog_block(self, blocks, block: BaseBlock) -> None:
        for ind, page_block in enumerate(blocks):
            if isinstance(page_block, type(block)):
                blocks[ind] = block


def get_catalog_page(
    page_repository: PageRepositoryInterface = get_page_repository(),
) -> GetCatalogPage:
    return GetCatalogPage(page_repository=page_repository)
