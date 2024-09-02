from typing import Any, Protocol

from catalog.models.products import Product
from user.interfaces import UserInterface
from user.models.product import UserProduct


class ProductsServiceInterface(Protocol):
    @staticmethod
    def get_raw_enabled_products_to_create(user_id: int) -> list[Product]:
        raise NotImplementedError()

    def get_enabled_products_to_create(self, user_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError()

    def filter_enabled_products(self, organization_id: int, user: UserInterface) -> list[dict[str, Any]]:
        raise NotImplementedError()

    @staticmethod
    def filter_user_products(category_id: int, user: UserInterface) -> list[UserProduct]:
        raise NotImplementedError()
