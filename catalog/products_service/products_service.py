from typing import Any

from django.db.models import Count, Q

from catalog.models.products import Organization, Product
from catalog.products_service.products_service_interface import ProductsServiceInterface
from catalog.serializers import ProductsSerializer
from user.interfaces import UserInterface
from user.models.product import UserProduct


class ProductsService(ProductsServiceInterface):
    @staticmethod
    def get_raw_enabled_products_to_create(user_id: int) -> list[Product]:
        products = (
            Product.objects.select_related("category", "organization")
            .exclude(Q(user_products__user_id=user_id) & Q(user_products__deleted=False))
            .filter(status="Опубликовано")
        )

        return products

    def get_enabled_products_to_create(self, user_id: int) -> list[dict[str, Any]]:
        return ProductsSerializer(self.get_raw_enabled_products_to_create(user_id), many=True).data

    def filter_enabled_products(self, organization_id: int, user: UserInterface) -> list[dict[str, Any]]:
        products = self.get_raw_enabled_products_to_create(user.id)

        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            products = products.filter(organization=organization)

        return ProductsSerializer(products, many=True).data

    @staticmethod
    def filter_user_products(category_id: int, user: UserInterface) -> list[UserProduct]:
        filters = Q(user=user, deleted=False)

        if category_id:
            filters &= Q(product__category_id=category_id)

        return UserProduct.objects.filter(filters)

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


def get_products_service() -> ProductsService:
    return ProductsService()
