from collections.abc import Iterable
from typing import List

from django.db.models import Count, Q, QuerySet

from domain.products.product import (
    ExclusiveCardInterface,
    OfferInterface,
    OrganizationInterface,
    ProductCategoryInterface,
    ProductInterface,
    ProductTypeInterface,
)
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.db_filters.products import (
    OffersFilter,
    OrganizationFilter,
    ProductFilters,
)
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
    def __filter_offers(self, filters: OffersFilter = None, order_by: str = None) -> QuerySet[Offer]:
        query_f = filters._build_query() if filters else Q()

        query = Offer.objects.prefetch_related("links").select_related("product").filter(query_f)
        if order_by:
            query = query.order_by(order_by)

        return query

    def filter_offers(self, filters: OffersFilter = None) -> list[OfferInterface]:
        return self.__filter_offers(filters)

    def __get_catalog_offers_query(self, filters: OffersFilter) -> QuerySet[Offer]:
        return (
            self.__filter_offers(filters)
            .prefetch_related("catalog_product")
            .select_related("product__category", "product__organization")
            .order_by("catalog_product__my_order")
        )

    def filter(self, filters: ProductFilters) -> list[ProductInterface]:
        query = filters._build_query()
        return Product.objects.select_related("category", "organization").prefetch_related("offers").filter(query)

    def get_exclusive_card(self) -> ExclusiveCardInterface:
        return ExclusiveCard.objects.first()

    def filter_organizations(self, filters: OrganizationFilter) -> list[OrganizationInterface]:
        query = filters._build_query()

        return Organization.objects.filter(query).order_by("name")

    def __get_published_types_query(self) -> QuerySet[ProductType]:
        return ProductType.objects.annotate(
            count=Count(
                "products",
                filter=Q(products__offer__product__status="Опубликовано", products__offer__status="Опубликовано"),
            )
        ).filter(status="Опубликовано", count__gte=1)

    def get_offer_type_relation(self, type_id: int, offer_id: int) -> ProductTypeInterface:
        return OfferTypeRelation.objects.get(type_id=type_id, offer_id=offer_id)

    def get_published_types(self) -> list[ProductTypeInterface]:
        return self.__get_published_types_query()

    def get_product_types_for_catalog(self, block_id: int) -> list[ProductTypeInterface]:
        return (
            self.__get_published_types_query()
            .filter(catalog_product_types__block_id=block_id)
            .order_by("catalog_product_types__my_order")
        )

    def get_proudct_types_for_additional_catalog(self, block_id: int) -> list[ProductTypeInterface]:
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

    def get_catalog_offers(self, filters: OffersFilter) -> list[OfferInterface]:
        return self.__get_catalog_offers_query(filters)

    def get_categories(self, product_ids: list[int]) -> Iterable[ProductCategoryInterface]:
        return ProductCategory.objects.filter(products__id__in=product_ids)


def get_product_repository() -> ProductRepositoryInterface:
    return ProductRepository()
