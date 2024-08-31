from django.db.models import Q

from catalog.models.products import Organization, Product
from user.interfaces import UserInterface
from user.models.product import UserProduct


class ProductsService:
    @staticmethod
    def get_enabled_products_to_create(user: UserInterface) -> list[Product]:
        user_products = user.products.values_list("product__id", flat=True).all()
        products = (
            Product.objects.select_related("category", "organization")
            .exclude(id__in=user_products)
            .filter(status="Опубликовано")
        )

        return products

    def filter_enabled_products(self, organization_id: int, user: UserInterface) -> list[Product]:
        products = self.get_enabled_products_to_create(user)

        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            products = products.filter(organization=organization)

        return products

    @staticmethod
    def filter_user_products(category_id: int, user: UserInterface) -> list[UserProduct]:
        filters = Q(user=user)

        if category_id:
            filters &= Q(product__category_id=category_id)

        return list(UserProduct.objects.filter(filters)) * 60


def get_products_service() -> ProductsService:
    return ProductsService()
