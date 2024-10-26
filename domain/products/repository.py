from typing import Any, Protocol


class ProductRepositoryInterface(Protocol):
    def get_enabled_products_to_create(self, user_id: int, organization_id: int):
        raise NotImplementedError

    def get_enabled_organizations(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    def filter_user_products(self, category_id: int, user_id: int):
        raise NotImplementedError
