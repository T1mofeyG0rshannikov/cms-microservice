from dataclasses import dataclass

from domain.common.screen import ImageInterface


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

    '''
    cover
    end_promotion
    links
    profit
    organization
    private
    name
    category

    class Meta:
        model = Offer
        fields = (
            "organization",
            "links",
            "link",
            "cover",
            "description",
            "annotation",
            "name",
            "private",
            "promotion",
            "profit",
            "end_promotion",
            "category",'''


@dataclass
class ExclusiveCardInterface:
    button_text: str
    button_ref: str
    image: ImageInterface
    bonus: str

    annotation: str
