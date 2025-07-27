from django.db.models import QuerySet

from application.dto.blocks import (
    ContentBlockDTO,
    CoverDTO,
    FeaturesBlockDTO,
    FooterDTO,
    QuestionsBlockDTO,
    RegisterBlockDTO,
)
from application.dto_builders.blocks import (
    get_additional_catalog_assembler,
    get_catalog_assembler,
    get_main_page_catalog_assembler,
    get_promo_catalog_assembler,
)
from application.mappers.blocks import orm_to_navbar, orm_to_social_media_block
from domain.page_blocks.entities.base_block import PageBlockInterface
from domain.page_blocks.entities.page import PageInterface
from infrastructure.persistence.models.blocks.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Footer,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
)
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.blocks.common import BaseBlock, BasePageModel

DTOBUILDERS = {
    MainPageCatalogBlock: get_main_page_catalog_assembler().process,
    PromoCatalog: get_promo_catalog_assembler().process,
    AdditionalCatalogBlock: get_additional_catalog_assembler().process,
    CatalogBlock: get_catalog_assembler().process,
    Navbar: orm_to_navbar,
    Cover: CoverDTO.process,
    RegisterBlock: RegisterBlockDTO.process,
    SocialMediaBlock: orm_to_social_media_block,
    ContentBlock: ContentBlockDTO.process,
    FeaturesBlock: FeaturesBlockDTO.process,
    QuestionsBlock: QuestionsBlockDTO.process,
    Footer: FooterDTO.process,
}


def from_orm_to_block(
    block: BaseBlock,
) -> PageBlockInterface:
    if block is None:
        return PageBlockInterface(content=None, styles=None)

    if isinstance(block, tuple(DTOBUILDERS.keys())):
        content = DTOBUILDERS[type(block)](block)
        return PageBlockInterface(content=content, styles=block.get_styles())

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
