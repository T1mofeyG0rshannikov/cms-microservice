from typing import Any, Iterable

from django.db.models import Count, Q

from domain.products.product import (
    OfferInterface,
    ProductInterface,
    ProductTypeInterface,
)
from domain.products.repository import ProductRepositoryInterface
from domain.user.product import UserProductInterface
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import (
    Offer,
    Organization,
    Product,
)
from infrastructure.persistence.models.user.product import UserOffer, UserProduct


class ProductRepository(ProductRepositoryInterface):
    def get_enabled_products_to_create(self, user_id: int, organization_id: int) -> Iterable[ProductInterface]:
        products = (
            Product.objects.select_related("category", "organization")
            .prefetch_related("user_products", "offers")
            .exclude(Q(user_products__user_id=user_id) & Q(user_products__deleted=False))
            .filter(status="Опубликовано", offers__status="Опубликовано")
        )

        if organization_id:
            products = products.filter(organization_id=organization_id)

        return products

    def get_enabled_organizations(self, user_id: int) -> dict[str, Any]:
        return (
            Organization.objects.annotate(
                count=Count("products", filter=Q(products__status="Опубликовано")),
                user_products_count=Count("products", filter=Q(products__user_products__user_id=user_id)),
            )
            .values("name", "id")
            .filter(count__gte=1, user_products_count__lte=0)
            .order_by("name")
        )

    def filter_user_products(self, category_id: int, user_id: int) -> list[UserProductInterface]:
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

    def get_published_types(self) -> Iterable[ProductTypeInterface]:
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

    def get_product_by_id(self, id: int) -> ProductInterface:
        return Product.objects.get(id=id)
    
    def get_product_name_by_user_products_id(self, user_product_id: int) -> str:
        return Product.objects.filter(user_products__id=user_product_id).values("name").first()["name"]

    def update_or_create_user_product(self, **kwargs) -> None:
        UserProduct.objects.update_or_create(
            user_id=kwargs.get("user_id"), product_id=kwargs.get("product_id"), defaults=kwargs
        )

    def get_product_offers(self, product_id: int) -> Iterable[OfferInterface]:
        return Offer.objects.filter(product_id=product_id)

    def update_or_create_user_offer(self, **kwargs) -> None:
        UserOffer.objects.update_or_create(
            user_id=kwargs.get("user_id"), offer_id=kwargs.get("offer_id"), defaults=kwargs
        )

    def delete_user_product(self, product_id: int) -> None:
        UserProduct.objects.filter(id=product_id).update(deleted=True)

    def get_unprivate_catalog_offers(self, product_type_slug: str) -> Iterable[OfferInterface]:
        return self.get_catalog_offers(product_type_slug).filter(product__private=False)

    def get_catalog_offers(self, product_type_slug: str) -> Iterable[OfferInterface]:
        return (
            self.get_offers()
            .prefetch_related("catalog_product")
            .select_related("product")
            .filter(types__type__slug=product_type_slug)
            .order_by("catalog_product__my_order")
        )

    def get_offers(self) -> list[OfferInterface]:
        return Offer.objects.filter(
            status="Опубликовано", product__status="Опубликовано", types__type__status="Опубликовано"
        ).annotate(count=Count("id"))

    def get_product_name_from_catalog(self, product_type_slug: str, product_index: int) -> str:
        return self.get_catalog_offers(product_type_slug)[product_index].product.name

    def user_product_exists(self, user_id: int, product_id: int) -> bool:
        return UserProduct.objects.filter(user_id=user_id, product_id=product_id).exists()


def get_product_repository() -> ProductRepositoryInterface:
    return ProductRepository()
