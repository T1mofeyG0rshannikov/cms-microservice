from typing import Any

from application.adapters.page import PageAdapter, get_page_adapter
from domain.page_blocks.base_block import PageBlockInterface
from infrastructure.persistence.models.blocks.blocks import Cover
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.catalog.blocks import CatalogPageTemplate
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class GetCatalogPage:
    def __init__(self, page_adapter: PageAdapter) -> None:
        self.page_adapter = page_adapter

    def __call__(self, slug: str):
        page = CatalogPageTemplate.objects.prefetch_related("blocks").first()

        page = self.set_catalog_block(page, slug)
        page = self.set_catalog_cover(page, slug)
        page = self.set_page_title(page, slug)

        return page

    def set_catalog_block(self, page, slug: str):
        page = self.page_adapter(page)
        catalog = self.get_catalog_block(slug)

        print(page)
        print(catalog)
        for ind, block in enumerate(page.blocks):
            if isinstance(block.content, CatalogBlock):
                page.blocks[ind] = catalog
        print(page)
        return page

    def get_catalog_block(self, slug: str) -> PageBlockInterface:
        return self.page_adapter.block_adapter(CatalogBlock.objects.get(product_type__slug=slug))

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        return self.page_adapter.block_adapter(Cover.objects.get(producttype__slug=slug))

    def set_catalog_cover(self, serialized_page, slug: str):
        cover = self.get_catalog_cover(slug)

        for ind, block in enumerate(serialized_page.blocks):
            if isinstance(block.content, Cover):
                serialized_page.blocks[ind] = cover

        return serialized_page

    def set_page_title(self, serialized_page, slug: str):
        serialized_page.title = ProductType.objects.values("name").get(slug=slug)["name"]

        return serialized_page


def get_catalog_page(page_adapter: PageAdapter = get_page_adapter()) -> GetCatalogPage:
    return GetCatalogPage(page_adapter=page_adapter)
