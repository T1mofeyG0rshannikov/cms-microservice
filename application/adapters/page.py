from domain.page_blocks.base_block import BaseBlockInterface
from domain.page_blocks.page import PageInterface
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.blocks.common import BaseBlock, Page
from infrastructure.persistence.models.common import BlockRelationship
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class BlockAdapter:
    repository = get_product_repository()

    def get_styles(self, block):
        if not block:
            return False

        return block.get_styles()

    def __call__(self, blocks_name: str) -> BaseBlockInterface:
        block = None

        blocks_name = BlockRelationship.objects.get(block_name=blocks_name)

        for f in blocks_name._meta.related_objects:
            if isinstance(f.related_model.objects.first(), BaseBlock):
                if f.field.model.objects.filter(block_relation=blocks_name).exists():
                    block = f.field.model.objects.select_related("styles").get(block_relation_id=blocks_name.id)
                    break

        if isinstance(block, MainPageCatalogBlock):
            block.products = self.repository.get_product_types_for_catalog(block.id)

        if isinstance(block, AdditionalCatalogBlock):
            block.products = self.repository.get_proudct_types_for_additional_catalog(block.id)

        if isinstance(block, PromoCatalog):
            block.products = self.repository.get_offers()

        if block is not None:
            block.template.file = "blocks/" + block.template.file

        styles = self.get_styles(block)

        return {"content": block, "styles": styles}


class PageAdapter:
    block_adapter = BlockAdapter()

    def get_page_block(self, blocks_name: str) -> BaseBlockInterface:
        block = None

        blocks_name = BlockRelationship.objects.get(block_name=blocks_name)

        for f in blocks_name._meta.related_objects:
            if isinstance(f.related_model.objects.first(), BaseBlock):
                if f.field.model.objects.filter(block_relation=blocks_name).exists():
                    block = f.field.model.objects.select_related("styles").get(block_relation_id=blocks_name.id)
                    break

        return block

    def __call__(self, page_model: Page) -> PageInterface:
        page_data = {
            "id": page_model.id,
            "title": page_model.title,
            "blocks": [self.block_adapter(block.name) for block in page_model.blocks.all()],
        }

        if hasattr(page_model, "url"):
            page_data["url"] = page_model.url

        return PageInterface(**page_data)
