from dataclasses import dataclass


@dataclass
class OrganizationInterface:
    name: str


@dataclass
class ProductCategoryInterface:
    name: str


@dataclass
class ProductTypeInterface:
    name: str


@dataclass
class ProductInterface:
    organization: OrganizationInterface

    name: str

    category: ProductCategoryInterface

    status: str

    private: bool

    partner_annotation: str
    partner_bonus: str
    partner_description: str


@dataclass
class OfferInterface:
    id: int
    name: str
    status: str
    product: ProductInterface
