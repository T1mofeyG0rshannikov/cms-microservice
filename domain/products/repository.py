from typing import Any, Iterable, Protocol

from domain.products.product import OfferInterface, ProductInterface, ProductTypeInterface


class ProductRepositoryInterface(Protocol):
    def get_enabled_products_to_create(self, user_id: int, organization_id: int) -> Iterable[ProductInterface]:
        raise NotImplementedError

    def get_enabled_organizations(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    def filter_user_products(self, category_id: int, user_id: int):
        raise NotImplementedError
    
    def get_product_types_for_catalog(self, block_id: int) -> Iterable[ProductTypeInterface]:
        raise NotImplementedError
    
    def get_proudct_types_for_additional_catalog(self, block_id: int) -> Iterable[ProductTypeInterface]:
        raise NotImplementedError
    
    def get_offers(self) -> list[OfferInterface]:
        raise NotImplementedError
    
    def get_product_offers(self, product_id: int) -> Iterable[OfferInterface]:
        raise NotImplementedError
    
    def update_or_create_user_product(self, **kwargs) -> None:
        raise NotImplementedError
    
    def update_or_create_user_offer(self, offer_id: int, user_id: int, link: str) -> None:
        raise NotImplementedError
    
    def delete_user_product(self, product_id: int) -> None:
        raise NotImplementedError
