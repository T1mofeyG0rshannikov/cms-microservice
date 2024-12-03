from django.db.models import Case, When

from domain.page_blocks.base_block import (
    BaseBlockInterface,
    BlockStyles,
    CatalogBlockInterface,
    PageBlockInterface,
)
from domain.page_blocks.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from infrastructure.files.files import find_class_in_directory
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.blocks.common import Block, Page
from infrastructure.persistence.models.catalog.blocks import Block as CatalogPageBlock
from infrastructure.persistence.models.catalog.blocks import (
    BlockRelationship as CatalogBlockRelationship,
)
from infrastructure.persistence.models.catalog.blocks import CatalogPageTemplate
from infrastructure.persistence.models.common import BlockRelationship
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class BlockAdapter:
    def __init__(self, repository: ProductRepositoryInterface, page_repository: PageRepositoryInterface) -> None:
        self.repository = repository
        self.page_repository = page_repository

    # def __call__(self, blocks_name: str) -> PageBlockInterface:
    # block = self.page_repository.get_page_block(blocks_name)

    def __call__(self, block):
        if isinstance(block, MainPageCatalogBlock):
            block.products = self.repository.get_product_types_for_catalog(block.id)

        if isinstance(block, AdditionalCatalogBlock):
            block.products = self.repository.get_proudct_types_for_additional_catalog(block.id)

        if isinstance(block, PromoCatalog):
            block.products = self.repository.get_offers()

        try:
            if block is not None:
                block.template.file = "blocks/" + block.template.file
        except AttributeError:
            pass

        return PageBlockInterface(content=block, styles=self.get_styles(block))

    def get_styles(self, block: BaseBlockInterface) -> BlockStyles:
        try:
            if not block:
                return False

            return block.get_styles()
        except AttributeError:
            return False


class PageAdapter:
    def __init__(self, block_adapter: BlockAdapter) -> None:
        self.block_adapter = block_adapter

    def __call__(self, page_model: Page) -> PageInterface:
        if isinstance(page_model, Page):
            block_names = Block.objects.filter(page=page_model).order_by("my_order").values_list("name", flat=True)
            blocks = (
                BlockRelationship.objects.filter(id__in=block_names)
                .order_by(Case(*[When(id=id, then=pos) for pos, id in enumerate(block_names)]))
                .values("block_name", "block")
            )

            block_models = []
            for block in blocks:
                ind = len(block["block"])
                while block["block"][ind - 1].isdigit() and block["block"][ind - 2].isdigit():
                    ind -= 1

                block_class = find_class_in_directory(
                    "infrastructure/persistence/models/blocks", block["block"][0 : ind - 1]
                )
                block_id = int(block["block"][ind - 1 : :])

                block_models.append(block_class.objects.get(id=block_id))

            page_data = {
                "id": page_model.id,
                "title": page_model.title,
                "blocks": [self.block_adapter(block) for block in block_models],
            }

            if hasattr(page_model, "url"):
                page_data["url"] = page_model.url

            return PageInterface(**page_data)

        elif isinstance(page_model, CatalogPageTemplate):
            block_names = (
                CatalogPageBlock.objects.filter(page=page_model).order_by("my_order").values_list("name", flat=True)
            )
            blocks = (
                CatalogBlockRelationship.objects.filter(id__in=block_names)
                .order_by(Case(*[When(id=id, then=pos) for pos, id in enumerate(block_names)]))
                .values("block_name", "block")
            )

            block_models = []
            for block in blocks:
                ind = len(block["block"])
                while block["block"][ind - 1].isdigit() and block["block"][ind - 2].isdigit():
                    ind -= 1

                block_class = find_class_in_directory(
                    "infrastructure/persistence/models/blocks", block["block"][0 : ind - 1]
                )
                block_id = int(block["block"][ind - 1 : :])

                block_models.append(block_class.objects.get(id=block_id))

            page_data = {
                "id": page_model.id,
                "title": page_model.title,
                "blocks": [self.block_adapter(block) for block in block_models],
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
