from typing import Any, Protocol

from catalog.models.products import Product
from user.models.product import UserProduct


class ProductRepositoryInterface(Protocol):
    @staticmethod
    def get_enabled_products_to_create(user_id: int, organization_id: int) -> list[Product]:
        raise NotImplementedError()

    @staticmethod
    def get_enabled_organizations(user_id: int) -> dict[str, Any]:
        raise NotImplementedError()

    @staticmethod
    def filter_user_products(category_id: int, user_id: int) -> list[UserProduct]:
        raise NotImplementedError()
