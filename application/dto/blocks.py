from dataclasses import dataclass
from typing import Any, Iterable

from domain.products.product import ExclusiveCardInterface, OfferInterface, ProductTypeInterface


@dataclass
class BaseBlockDTO:
    name: str
    template: Any
    ancor: str


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


@dataclass
class PromoCatalogDTO(BaseBlockDTO):
    title: str
    products: Iterable[OfferInterface]
