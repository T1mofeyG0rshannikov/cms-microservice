import os

from application.dto.blocks import (
    NavbarDTO,
    NavItemDTO,
    SocialMediaBlockDTO,
    SocialMediaButtonDTO,
)
from domain.page_blocks.entities.social import SocialNetworkInterface
from infrastructure.persistence.models.blocks.blocks import Navbar, SocialMediaBlock
from infrastructure.persistence.models.blocks.blocks_components import SocialMediaButton
from infrastructure.persistence.models.settings import SocialNetwork
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
            NavItemDTO(button_ref=item.button_ref, button_text=item.button_text) for item in navbar.menu_items.all()
        ],
    )


def orm_to_social(social: SocialNetwork):
    return SocialNetworkInterface(
        name=social.name, domain=social.domain, icon=social.icon, button_color=social.button_color
    )


def orm_to_social_button(social: SocialMediaButton):
    return SocialMediaButtonDTO(
        ref=social.ref, social_network=orm_to_social(social.social_network) if social.social_network else None
    )


def orm_to_social_media_block(block: SocialMediaBlock, config: TemplateSettings = get_template_settings()):
    return SocialMediaBlockDTO(
        name=block.name,
        template=os.path.join(config.blocks_templates_folder, block.template.file),
        ancor=block.ancor,
        text=block.text,
        title=block.title,
        socials=[orm_to_social_button(social) for social in block.socials.select_related("social_network").all()],
    )
