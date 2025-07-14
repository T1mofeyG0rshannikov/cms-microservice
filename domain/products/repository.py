from collections.abc import Iterable
from typing import Any, Protocol

from domain.products.product import (
    ExclusiveCardInterface,
    OfferInterface,
    ProductCategoryInterface,
    ProductInterface,
    ProductTypeInterface,
)


class ProductRepositoryInterface(Protocol):
    def get_exclusive_card(self) -> ExclusiveCardInterface:
        raise NotImplementedError

    def get_offer_type_relation(self, type_id: int, offer_id: int):
        raise NotImplementedError
    
    def get_enabled_products_to_create(self, user_id: int, organization_id: int) -> Iterable[ProductInterface]:
        raise NotImplementedError

    def get_enabled_organizations(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    def get_product_types_for_catalog(self, block_id: int) -> Iterable[ProductTypeInterface]:
        raise NotImplementedError

    def get_proudct_types_for_additional_catalog(self, block_id: int) -> Iterable[ProductTypeInterface]:
        raise NotImplementedError

    def get_offers(self) -> Iterable[OfferInterface]:
        raise NotImplementedError

    def get_product_offers(self, product_id: int) -> Iterable[OfferInterface]:
        raise NotImplementedError

    def get_type(self, slug: str) -> ProductTypeInterface:
        raise NotImplementedError

    def get_product_name_from_catalog(self, product_type_slug: str, product_index: int) -> str:
        raise NotImplementedError

    def get(self, id: int | None = None, user_product_id: int | None = None) -> ProductInterface | None:
        raise NotImplementedError

    def get_catalog_offers(self, products_slug: str, private: bool | None = None) -> Iterable[OfferInterface]:
        raise NotImplementedError

    def get_product_categories(self, user_id: int) -> Iterable[ProductCategoryInterface]:
        raise NotImplementedError

    def get_product_for_popup(self, product_id: int) -> ProductInterface:
        raise NotImplementedError

    def get_published_offers(self, product_type_id: int) -> Iterable[OfferInterface]:
        raise NotImplementedError
