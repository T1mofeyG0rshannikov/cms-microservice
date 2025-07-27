from dataclasses import dataclass, fields

from django.db.models import Q

from domain.common.db_filter import BaseDBFilters
from domain.products.repository import (
    OffersFilterInterface,
    OrganizationFilterInterface,
    ProductFiltersInterface,
    ProductTypeFilterInterface,
)


class BaseDjangoDBFilters(BaseDBFilters):
    def _build_query(self) -> Q:
        query = Q()
        filter_mappers = self.db_field_mappers()
        special_fields = self.get_special_queries()

        for field in fields(self):
            if getattr(self, field.name):
                if special_fields and field.name in special_fields:
                    query &= special_fields[field.name]
                else:
                    query &= Q(**{filter_mappers[field.name]: getattr(self, field.name)})

        return query


@dataclass
class OffersFilter(OffersFilterInterface, BaseDjangoDBFilters):
    @classmethod
    def db_field_mappers(cls):
        return {
            "status": "status",
            "product_status": "product__status",
            "type_status": "types__type__status",
            "product_type_slug": "types__type__slug",
            "type_id": "types__type_id",
            "product_id": "product_id",
            "private": "product__private",
        }


@dataclass
class ProductFilters(ProductFiltersInterface, BaseDjangoDBFilters):
    @classmethod
    def db_field_mappers(cls):
        return {
            "ids": "id__in",
            "category_ids": "category_id__in",
            "organization_id": "organization_id",
            "status": "status",
            "offer_status": "offers__status",
        }

    def get_special_queries(self):
        return {"exclude_ids": ~Q(id__in=self.exclude_ids)}


@dataclass
class OrganizationFilter(OrganizationFilterInterface, BaseDjangoDBFilters):
    def get_special_queries(self):
        return {"exclude_product_ids": ~Q(products__id__in=self.exclude_product_ids)}

    @classmethod
    def db_field_mappers(cls):
        return {
            "offer_status": "products__offers__status",
            "product_status": "products__status",
        }


@dataclass
class ProductTypeFilter(ProductTypeFilterInterface, BaseDjangoDBFilters):
    @classmethod
    def get_field_mappers(cls):
        return {
            "product_status": "products__offer__product__status",
            "offer_status": "products__offer__status",
            "status": "status",
        }
