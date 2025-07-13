from dataclasses import dataclass
from typing import Any, Iterable

from domain.products.product import OfferInterface, ProductTypeInterface


@dataclass
class BaseBlockDTO:
    name: str
    template: Any
    ancor: str


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