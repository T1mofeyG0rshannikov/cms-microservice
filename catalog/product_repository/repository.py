from typing import Any

from django.db.models import Count, Q

from catalog.models.products import Organization, Product
from catalog.product_repository.repository_interface import ProductRepositoryInterface
from user.models.product import UserProduct


class ProductRepository(ProductRepositoryInterface):
    @staticmethod
    def get_enabled_products_to_create(user_id: int, organization_id: int) -> list[Product]:
        products = (
            Product.objects.select_related("category", "organization")
            .exclude(Q(user_products__user_id=user_id) & Q(user_products__deleted=False))
            .filter(status="Опубликовано")
        )

        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            products = products.filter(organization=organization)

        return products

    @staticmethod
    def get_enabled_organizations(user_id: int) -> dict[str, Any]:
        return (
            Organization.objects.annotate(
                count=Count("products", filter=Q(products__status="Опубликовано")),
                user_products_count=Count("products", filter=Q(products__user_products__user_id=user_id)),
            )
            .values("name", "id")
            .filter(count__gte=1, user_products_count__lte=0)
            .order_by("name")
        )

    @staticmethod
    def filter_user_products(category_id: int, user_id: int) -> list[UserProduct]:
        filters = Q(user_id=user_id, deleted=False)

        if category_id:
            filters &= Q(product__category_id=category_id)

        return UserProduct.objects.filter(filters)


def get_product_repository() -> ProductRepository:
    return ProductRepository()
