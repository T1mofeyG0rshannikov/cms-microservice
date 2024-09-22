from dataclasses import dataclass


@dataclass
class OrganizationInterface:
    name: str


@dataclass
class ProductCategoryInterface:
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
