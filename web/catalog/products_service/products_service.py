from typing import Any

from domain.products.repository import ProductRepositoryInterface
from domain.user.referral import UserInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.catalog.products_service.products_service_interface import (
    ProductsServiceInterface,
)
from web.catalog.serializers import ProductsSerializer


class ProductsService(ProductsServiceInterface):
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def get_enabled_products_to_create(self, user_id: int, organization_id: int) -> list[dict[str, Any]]:
        return ProductsSerializer(
            self.repository.get_enabled_products_to_create(user_id, organization_id), many=True
        ).data

    def filter_enabled_products(self, organization_id: int, user: UserInterface) -> list[dict[str, Any]]:
        products = self.repository.get_enabled_products_to_create(user.id, organization_id)

        return ProductsSerializer(products, many=True).data

    def filter_user_products(self, category_id: int, user: UserInterface):
        return self.repository.filter_user_products(category_id, user.id)

    def get_enabled_organizations(self, user_id: int) -> dict[str, Any]:
        return self.repository.get_enabled_organizations(user_id)


def get_products_service() -> ProductsService:
    return ProductsService(get_product_repository())
