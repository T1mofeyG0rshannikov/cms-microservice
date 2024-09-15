from typing import Any

from catalog.models.product_type import ProductType
from catalog.models.products import Offer, Organization, Product
from catalog.product_repository.repository_interface import ProductRepositoryInterface
from django.db.models import Count, Q
from user.models.product import UserOffer, UserProduct


class ProductRepository(ProductRepositoryInterface):
    @staticmethod
    def get_enabled_products_to_create(user_id: int, organization_id: int) -> list[Product]:
        products = (
            Product.objects.select_related("category", "organization")
            .prefetch_related("user_products", "offers")
            .exclude(Q(user_products__user_id=user_id) & Q(user_products__deleted=False))
            .filter(status="Опубликовано", offers__status="Опубликовано")
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

    def get_published_offers(self, type_id: int):
        return (
            self.get_offers()
            .select_related("product")
            .filter(types__type_id=type_id)
            .order_by("product__organization__name")
        )

    @staticmethod
    def get_published_types():
        return ProductType.objects.annotate(
            count=Count(
                "products",
                filter=Q(products__offer__product__status="Опубликовано", products__offer__status="Опубликовано"),
            )
        ).filter(status="Опубликовано", count__gte=1)

    def get_product_types_for_catalog(self, block_id: int):
        return (
            self.get_published_types()
            .filter(catalog_product_types__block=block_id)
            .order_by("catalog_product_types__my_order")
        )

    def get_proudct_types_for_additional_catalog(self, block_id: int):
        return (
            self.get_published_types()
            .filter(additional_catalog_product_types__block_id=block_id)
            .order_by("additional_catalog_product_types__my_order")
        )

    @staticmethod
    def get_product_by_id(id: int):
        return Product.objects.get(id=id)

    @staticmethod
    def update_or_create_user_product(**kwargs) -> None:
        UserProduct.objects.update_or_create(
            user=kwargs.get("user"), product_id=kwargs.get("product_id"), defaults=kwargs
        )

    @staticmethod
    def get_product_offers(product_id: int):
        return Offer.objects.filter(product_id=product_id)

    @staticmethod
    def update_or_create_user_offer(**kwargs) -> None:
        UserOffer.objects.update_or_create(
            user_id=kwargs.get("user_id"), offer_id=kwargs.get("offer_id"), defaults=kwargs
        )

    @staticmethod
    def delete_user_product(product_id: int) -> None:
        product = UserProduct.objects.get(id=product_id)
        product.deleted = True
        product.save()

    def get_unprivate_catalog_offers(self, catalog_id: int):
        return self.get_catalog_offers(catalog_id).filter(product__private=False)

    def get_catalog_offers(self, catalog_id: int):
        return (
            self.get_offers()
            .prefetch_related("catalog_product")
            .filter(catalog_product__block=catalog_id)
            .order_by("catalog_product__my_order")
        )

    @staticmethod
    def get_offers():
        return Offer.objects.filter(
            status="Опубликовано", product__status="Опубликовано", types__type__status="Опубликовано"
        )


def get_product_repository() -> ProductRepository:
    return ProductRepository()
