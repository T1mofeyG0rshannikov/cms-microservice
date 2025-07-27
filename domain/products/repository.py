from dataclasses import dataclass
from typing import List, Protocol

from domain.products.product import (
    ExclusiveCardInterface,
    OfferInterface,
    OrganizationInterface,
    ProductCategoryInterface,
    ProductInterface,
    ProductTypeInterface,
)


@dataclass
class ProductFiltersInterface:
    ids: list[int] | None = None
    category_ids: list[int] | None = None
    exclude_ids: list[int] | None = None
    organization_id: int | None = None
    status: str | None = None
    offer_status: str | None = None


@dataclass
class OffersFilterInterface:
    status: str = "Опубликовано"
    product_status: str = "Опубликовано"
    type_status: str = "Опубликовано"
    product_type_slug: str = None
    type_id: int = None
    product_id: int = None
    private: bool = None


@dataclass
class OrganizationFilterInterface:
    offer_status: str = "Опубликовано"
    product_status: str = "Опубликовано"
    exclude_product_ids: list[int] = None


@dataclass
class ProductTypeFilterInterface:
    product_status = "Опубликовано"
    offer_status = "Опубликовано"
    status = "Опубликовано"


class ProductRepositoryInterface(Protocol):
    def filter_offers(self, filters: OffersFilterInterface) -> list[OfferInterface]:
        raise NotImplementedError

    def filter(self, filters: ProductFiltersInterface) -> list[ProductInterface]:
        raise NotImplementedError

    def get_exclusive_card(self) -> ExclusiveCardInterface:
        raise NotImplementedError

    def get_offer_type_relation(self, type_id: int, offer_id: int):
        raise NotImplementedError

    def filter_organizations(self, filters: OrganizationFilterInterface) -> list[OrganizationInterface]:
        raise NotImplementedError

    def get_published_types(self) -> list[ProductTypeInterface]:
        raise NotImplementedError

    def get_product_types_for_catalog(self, block_id: int) -> list[ProductTypeInterface]:
        raise NotImplementedError

    def get_proudct_types_for_additional_catalog(self, block_id: int) -> list[ProductTypeInterface]:
        raise NotImplementedError

    def get(self, id: int | None = None, user_product_id: int | None = None) -> ProductInterface | None:
        raise NotImplementedError

    def get_product_name_from_catalog(self, product_type_slug: str, product_index: int) -> str:
        raise NotImplementedError

    def get_categories(self, product_ids: list[int]) -> list[ProductCategoryInterface]:
        raise NotImplementedError

    def get_product_for_popup(self, product_id: int) -> ProductInterface:
        raise NotImplementedError
