from domain.page_blocks.base_block import (
    BaseBlockInterface,
    BlockStyles,
    PageBlockInterface,
)
from domain.page_blocks.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.blocks.common import Page
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class BlockAdapter:
    def __init__(self, repository: ProductRepositoryInterface, page_repository: PageRepositoryInterface):
        self.repository = repository
        self.page_repository = page_repository

    def get_styles(self, block: BaseBlockInterface) -> BlockStyles:
        if not block:
            return False

        return block.get_styles()

    def __call__(self, blocks_name: str) -> PageBlockInterface:
        block = self.page_repository.get_page_block(blocks_name)

        if isinstance(block, MainPageCatalogBlock):
            block.products = self.repository.get_product_types_for_catalog(block.id)

        if isinstance(block, AdditionalCatalogBlock):
            block.products = self.repository.get_proudct_types_for_additional_catalog(block.id)

        if isinstance(block, PromoCatalog):
            block.products = self.repository.get_offers()

        if block is not None:
            block.template.file = "blocks/" + block.template.file

        return PageBlockInterface(content=block, styles=self.get_styles(block))


class PageAdapter:
    def __init__(self, block_adapter: BlockAdapter):
        self.block_adapter = block_adapter

    def __call__(self, page_model: Page) -> PageInterface:
        page_data = {
            "id": page_model.id,
            "title": page_model.title,
            "blocks": [self.block_adapter(block.name) for block in page_model.blocks.all()],
        }

        if hasattr(page_model, "url"):
            page_data["url"] = page_model.url

        return PageInterface(**page_data)


def get_block_adapter(
    repository: ProductRepositoryInterface = get_product_repository(),
    page_repository: PageRepositoryInterface = get_page_repository(),
) -> BlockAdapter:
    return BlockAdapter(repository=repository, page_repository=page_repository)


def get_page_adapter(block_adapter: BlockAdapter = get_block_adapter()) -> PageAdapter:
    return PageAdapter(block_adapter)
