import os

from django.db.models import QuerySet

from application.dto_builders.blocks import get_catalog_assembler, get_main_page_catalog_assembler, get_promo_catalog_assembler, get_additional_catalog_assembler
from infrastructure.persistence.models.blocks.catalog_block import AdditionalCatalogBlock, CatalogBlock, MainPageCatalogBlock, PromoCatalog
from domain.page_blocks.entities.base_block import PageBlockInterface
from domain.page_blocks.entities.page import PageInterface
from infrastructure.persistence.models.blocks.common import BaseBlock, BasePageModel
from infrastructure.public.template_settings import (
    TemplateSettings,
    get_template_settings,
)

DTOBUILDERS = {
    MainPageCatalogBlock: get_main_page_catalog_assembler,
    PromoCatalog: get_promo_catalog_assembler,
    AdditionalCatalogBlock: get_additional_catalog_assembler,
    CatalogBlock: get_catalog_assembler
}

def from_orm_to_block(
    block: BaseBlock,
    config: TemplateSettings = get_template_settings()
) -> PageBlockInterface:
    if block is None:
        return PageBlockInterface(content=None, styles=None)
    
    print(block, type(block), type(block) in DTOBUILDERS)
    if type(block) in DTOBUILDERS:
        content = DTOBUILDERS[type(block)]().build_data(block)
        content.template.file = os.path.join(config.blocks_templates_folder, block.template.file)
        return PageBlockInterface(content=content, styles=block.get_styles())

    block.template.file = os.path.join(config.blocks_templates_folder, block.template.file)

    return PageBlockInterface(content=block, styles=block.get_styles())


def from_orm_to_page(page: BasePageModel, blocks: QuerySet[BaseBlock]) -> PageInterface:
    page_entity = PageInterface(
        id=page.id,
        title=page.title,
        blocks=[from_orm_to_block(block) for block in blocks],
    )

    if hasattr(page, "url"):
        page_entity.url = page.url

    return page_entity
