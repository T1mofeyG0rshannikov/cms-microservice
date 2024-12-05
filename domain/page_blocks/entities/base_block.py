from collections.abc import Iterable
from dataclasses import dataclass

from domain.products.product import ProductInterface


@dataclass
class TemplateInterface:
    name: str
    template: str
    file: str


@dataclass
class BaseBlockInterface:
    id: int
    name: str
    template: TemplateInterface
    ancor: str | None

    def get_styles():
        pass


@dataclass
class CatalogBlockInterface(BaseBlockInterface):
    products: Iterable[ProductInterface]


@dataclass
class BlockStyles:
    pass


@dataclass
class PageBlockInterface:
    content: BaseBlockInterface
    styles: BlockStyles
