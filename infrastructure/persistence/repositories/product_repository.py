from collections.abc import Iterable
from typing import Any

from django.db.models import Count, Q, QuerySet

from domain.products.product import (
    ExclusiveCardInterface,
    OfferInterface,
    ProductCategoryInterface,
    ProductInterface,
    ProductTypeInterface,
)
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.catalog.product_type import (
    ProductCategory,
    ProductType,
)
from infrastructure.persistence.models.catalog.products import (
    ExclusiveCard,
    Offer,
    OfferTypeRelation,
    Organization,
    Product,
)


class ProductRepository(ProductRepositoryInterface):
    def __get_offers_query(self) -> QuerySet[Offer]:
        return (
            Offer.objects.filter(
                status="Опубликовано", product__status="Опубликовано", types__type__status="Опубликовано"
            )
            .prefetch_related("links")
            .annotate(count=Count("id"))
        )

    def __get_published_types_query(self) -> QuerySet[ProductType]:
        return ProductType.objects.annotate(
            count=Count(
                "products",
                filter=Q(products__offer__product__status="Опубликовано", products__offer__status="Опубликовано"),
            )
        ).filter(status="Опубликовано", count__gte=1)

    def __get_catalog_offers_query(self, product_type_slug: str) -> QuerySet[Offer]:
        return (
            self.__get_offers_query()
            .prefetch_related("catalog_product")
            .select_related("product__category", "product__organization")
            .filter(types__type__slug=product_type_slug)
            .order_by("catalog_product__my_order")
        )
    
    def get_exclusive_card(self) -> ExclusiveCardInterface:
        return ExclusiveCard.objects.first()
    
    def get_offer_type_relation(self, type_id: int, offer_id: int):
        return OfferTypeRelation.objects.get(type_id=type_id, offer_id=offer_id)

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
                user_products_count=Count(
                    "products",
                    filter=Q(products__user_products__user_id=user_id) & Q(products__user_products__deleted=False),
                ),
            )
            .values("name", "id")
            .filter(count__gte=1, user_products_count__lte=0)
            .order_by("name")
        )

    def get_published_offers(self, type_id: int):
        return (
            self.__get_offers_query()
            .select_related("product")
            .filter(types__type_id=type_id)
            .order_by("product__organization__name")
        )

    def get_published_types(self) -> Iterable[ProductTypeInterface]:
        return self.__get_published_types_query()

    def get_product_types_for_catalog(self, block_id: int):
        return (
            self.__get_published_types_query()
            .filter(catalog_product_types__block=block_id)
            .order_by("catalog_product_types__my_order")
        )

    def get_proudct_types_for_additional_catalog(self, block_id: int):
        return (
            self.__get_published_types_query()
            .filter(additional_catalog_product_types__block_id=block_id)
            .order_by("additional_catalog_product_types__my_order")
        )

    def get(self, id: int | None = None, user_product_id: int | None = None) -> ProductInterface | None:
        query = Q()
        if id:
            query &= Q(id=id)
        elif user_product_id:
            query &= Q(user_products__id=user_product_id)

        try:
            return Product.objects.get(query)
        except Product.DoesNotExist:
            return None

    def get_product_offers(self, product_id: int) -> Iterable[OfferInterface]:
        return Offer.objects.filter(product_id=product_id)

    def get_catalog_offers(self, product_type_slug: str, private: bool | None = None) -> Iterable[OfferInterface]:
        query = self.__get_catalog_offers_query(product_type_slug)
        if private is not None:
            query = query.filter(product__private=private)

        return query

    def get_offers(self) -> Iterable[OfferInterface]:
        return self.__get_offers_query()

    def get_product_name_from_catalog(self, product_type_slug: str, product_index: int) -> str:
        return self.__get_catalog_offers_query(product_type_slug)[product_index].product.name

    def get_type(self, slug: str) -> ProductTypeInterface:
        return ProductType.objects.get(slug=slug)

    def get_product_categories(self, user_id: int) -> Iterable[ProductCategoryInterface]:
        return ProductCategory.objects.annotate(
            count=Count("products", filter=Q(products__user_products__user_id=user_id))
        ).filter(count__gte=1)

    def get_product_for_popup(self, product_id: int) -> ProductInterface:
        return (
            Product.objects.select_related("organization")
            .values("partner_description", "organization__partner_program")
            .get(id=product_id)
        )


def get_product_repository() -> ProductRepositoryInterface:
    return ProductRepository()
