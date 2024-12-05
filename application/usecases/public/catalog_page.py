from application.adapters.page_adapter import PageAdapter, get_page_adapter
from domain.page_blocks.entities.base_block import (
    CatalogBlockInterface,
    PageBlockInterface,
)
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class GetCatalogPage:
    def __init__(
        self,
        page_adapter: PageAdapter,
        page_repository: PageRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.page_adapter = page_adapter
        self.page_repository = page_repository
        self.product_repository = product_repository

    def __call__(self, slug: str) -> PageInterface:
        page = self.page_repository.get_catalog_page_template()
        page = self.page_adapter(page)

        catalog = self.get_catalog_block(slug)
        page = self.set_catalog_block(page, catalog)

        cover = self.get_catalog_cover(slug)
        page = self.set_catalog_block(page, cover)
        page = self.set_page_title(page, slug)

        return page

    def set_catalog_block(self, page: PageInterface, block: PageBlockInterface) -> PageInterface:
        for ind, page_block in enumerate(page.blocks):
            if isinstance(page_block.content, type(block.content)):
                page.blocks[ind] = block

        return page

    def get_catalog_block(self, slug: str) -> CatalogBlockInterface:
        return self.page_adapter.block_adapter(self.page_repository.get_catalog_block(slug))

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        return self.page_adapter.block_adapter(self.page_repository.get_catalog_cover(slug))

    def set_page_title(self, page: PageInterface, slug: str) -> PageInterface:
        page.title = self.product_repository.get_product_type_name(slug)

        return page


def get_catalog_page(
    page_adapter: PageAdapter = get_page_adapter(),
    page_repository: PageRepositoryInterface = get_page_repository(),
    product_repository: ProductRepositoryInterface = get_product_repository(),
) -> GetCatalogPage:
    return GetCatalogPage(
        page_adapter=page_adapter, page_repository=page_repository, product_repository=product_repository
    )
