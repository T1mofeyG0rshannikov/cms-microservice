import os
from collections.abc import Iterable
from dataclasses import dataclass

from ckeditor.fields import RichTextField
from django.db import models

from domain.page_blocks.entities.social import SocialNetworkInterface
from domain.products.product import (
    ExclusiveCardInterface,
    OfferInterface,
    ProductTypeInterface,
)
from infrastructure.persistence.models.blocks.common import BaseBlock
from infrastructure.persistence.models.catalog.products import Offer
from infrastructure.public.template_settings import (
    TemplateSettings,
    get_template_settings,
)


@dataclass
class BaseDTO:
    @classmethod
    def process(cls, obj: models.Model):
        data = {}
        for field in obj._meta.fields:
            if isinstance(field, models.CharField) or isinstance(field, RichTextField):
                data[field.name] = getattr(obj, field.name)
            elif isinstance(field, models.ImageField):
                data[field.name] = getattr(obj, field.name).url
            elif isinstance(field, models.DateTimeField):
                data[field.name] = getattr(obj, field.name)

        return cls(**data)


@dataclass
class BaseBlockDTO:
    name: str
    template: str
    ancor: str

    @classmethod
    def process(cls, block: BaseBlock, config: TemplateSettings = get_template_settings()):
        data = {}
        for field in block._meta.fields:
            if isinstance(field, models.CharField) or isinstance(field, RichTextField):
                data[field.name] = getattr(block, field.name)
            elif isinstance(field, models.ImageField):
                data[field.name] = getattr(block, field.name).url
            elif field.name == "template":
                data["template"] = os.path.join(config.blocks_templates_folder, block.template.file)

        return cls(**data)


@dataclass
class SocialMediaButtonDTO:
    ref: str

    social_network: SocialNetworkInterface


@dataclass
class SocialMediaBlockDTO(BaseBlockDTO):
    text: str
    title: str
    socials: Iterable[SocialMediaButtonDTO]


@dataclass
class CatalogOfferPresenterDTO:
    cover: str
    end_promotion: str
    links: str
    organization: str
    private: str
    name: str
    link: str
    description: str
    annotation: str
    promotion: str
    profit: str
    category: str


@dataclass
class CatalogDTO(BaseBlockDTO):
    button_text: str
    button_ref: str
    title: str

    introductory_text: str

    add_category: bool
    products: Iterable[CatalogOfferPresenterDTO]
    exclusive_card: ExclusiveCardInterface = None


@dataclass
class MainPageCatalogBlockDTO(BaseBlockDTO):
    title: str
    introductory_text: str

    button_text: str

    products: Iterable[ProductTypeInterface]


@dataclass
class AdditionalCatalogBlockDTO(BaseBlockDTO):
    button_text: str

    add_annotation: bool
    add_button: bool

    products: Iterable[ProductTypeInterface]


class OfferDTO(OfferInterface, BaseDTO):
    pass


def orm_to_offer(offer: Offer):
    return OfferDTO.process(offer)


@dataclass
class PromoCatalogDTO(BaseBlockDTO):
    title: str
    products: Iterable[OfferDTO]


@dataclass
class NavItemDTO:
    button_text: str
    button_ref: str


@dataclass
class NavbarDTO(BaseBlockDTO):
    register_button_text: str
    register_button_href: str

    login_button_text: str

    items: Iterable[NavItemDTO]


@dataclass
class CoverDTO(BaseBlockDTO):
    image_desctop: str
    image_mobile: str
    second_button_text: str
    second_button_ref: str

    button_text: str
    button_ref: str

    title: str

    text: str


@dataclass
class RegisterBlockDTO(BaseBlockDTO):
    title: str
    warning_text: str
    explanation_text: str = None


@dataclass
class ContentBlockDTO(BaseBlockDTO):
    button_text: str
    button_ref: str
    title: str
    text: str
    image1: str
    image2: str


@dataclass
class FeaturesBlockDTO(BaseBlockDTO):
    button_text: str
    button_ref: str
    title: str
    introductory_text: str


@dataclass
class QuestionsBlockDTO(BaseBlockDTO):
    pass


@dataclass
class FooterDTO(BaseBlockDTO):
    text1: str
    text2: str
    text3: str
