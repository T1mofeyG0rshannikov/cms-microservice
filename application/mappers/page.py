import os

from django.db.models import QuerySet

from application.dto_builders.blocks import get_catalog_assembler, get_main_page_catalog_assembler, get_promo_catalog_assembler, get_additional_catalog_assembler
from application.dto.blocks import ContentBlockDTO, CoverDTO, FeaturesBlockDTO, FooterDTO, NavItemDTO, NavbarDTO, QuestionsBlockDTO, RegisterBlockDTO, SocialMediaBlockDTO, SocialMediaButtonDTO
from domain.page_blocks.entities.social import SocialNetworkInterface
from infrastructure.persistence.models.settings import SocialNetwork
from infrastructure.persistence.models.blocks.blocks_components import SocialMediaButton
from infrastructure.persistence.models.blocks.blocks import ContentBlock, Cover, FeaturesBlock, Footer, Navbar, QuestionsBlock, RegisterBlock, SocialMediaBlock
from infrastructure.persistence.models.blocks.catalog_block import AdditionalCatalogBlock, CatalogBlock, MainPageCatalogBlock, PromoCatalog
from domain.page_blocks.entities.base_block import PageBlockInterface
from domain.page_blocks.entities.page import PageInterface
from infrastructure.persistence.models.blocks.common import BaseBlock, BasePageModel
from infrastructure.public.template_settings import (
    TemplateSettings,
    get_template_settings,
)

def orm_to_navbar(navbar: Navbar, config: TemplateSettings = get_template_settings()):
    return NavbarDTO(
        name=navbar.name,
        template=os.path.join(config.blocks_templates_folder, navbar.template.file),
        ancor=navbar.ancor,
        register_button_text=navbar.register_button_text,
        register_button_href=navbar.register_button_href,
        login_button_text=navbar.login_button_text,
        items=[
            NavItemDTO(
                button_ref=item.button_ref,
                button_text=item.button_text
            ) for item in navbar.menu_items.all()
        ]
    )

def orm_to_cover(block: Cover, config: TemplateSettings = get_template_settings()):
    return CoverDTO.process(block, config)

def orm_to_social(social: SocialNetwork):
    return SocialNetworkInterface(
        name=social.name,
        domain=social.domain,
        icon=social.icon,
        button_color=social.button_color
    )

def orm_to_social_button(social: SocialMediaButton):
    return SocialMediaButtonDTO(
        ref=social.ref,
        social_network=orm_to_social(social.social_network) if social.social_network else None
    )

def orm_to_social_media_block(block: SocialMediaBlock, config: TemplateSettings = get_template_settings()):
    return SocialMediaBlockDTO(
        name=block.name,
        template=os.path.join(config.blocks_templates_folder, block.template.file),
        ancor=block.ancor,
        text=block.text,
        title=block.title,
        socials=[
            orm_to_social_button(social) for social in block.socials.select_related("social_network").all()
        ]
    )

DTOBUILDERS = {
    MainPageCatalogBlock: get_main_page_catalog_assembler().build_data,
    PromoCatalog: get_promo_catalog_assembler().build_data,
    AdditionalCatalogBlock: get_additional_catalog_assembler().build_data,
    CatalogBlock: get_catalog_assembler().build_data,
    Navbar: orm_to_navbar,
    Cover: orm_to_cover,
    RegisterBlock: RegisterBlockDTO.process,
    SocialMediaBlock: orm_to_social_media_block,
    ContentBlock: ContentBlockDTO.process,
    FeaturesBlock: FeaturesBlockDTO.process,
    QuestionsBlock: QuestionsBlockDTO.process,
    Footer: FooterDTO.process
}

def from_orm_to_block(
    block: BaseBlock,
    config: TemplateSettings = get_template_settings()
) -> PageBlockInterface:
    if block is None:
        return PageBlockInterface(content=None, styles=None)
    
    print(block, type(block), type(block) in DTOBUILDERS)
    if type(block) in DTOBUILDERS:
        content = DTOBUILDERS[type(block)](block)
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
