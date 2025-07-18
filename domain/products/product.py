from dataclasses import dataclass
from datetime import datetime

from domain.common.screen import ImageInterface


@dataclass
class OrganizationInterface:
    name: str


@dataclass
class ProductCategoryInterface:
    name: str


@dataclass
class ProductTypeInterface:
    status: str
    name: str
    slug: str
    title: str
    image: str
    description: str
    profit: str


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

    annotation: str
    description: str

    banner: str
    promote: datetime

    promotion: bool

    start_promotion: datetime
    end_promotion: datetime

    created_at: datetime

    status: str

    terms_of_the_promotion: str

    partner_program: str
    verification_of_registration: str


@dataclass
class ExclusiveCardInterface:
    button_text: str
    button_ref: str
    image: ImageInterface
    bonus: str

    annotation: str
