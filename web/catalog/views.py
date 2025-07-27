from dataclasses import asdict

from django.http import HttpRequest, JsonResponse
from django.views import View

from application.usecases.catalog.get_organizations import get_organizations_interactor
from application.usecases.catalog.get_products import get_products_interactor
from domain.products.repository import (
    OrganizationFilterInterface,
    ProductFiltersInterface,
    ProductRepositoryInterface,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.catalog.serializers import ProductCategorySerializer
from web.common.get_filters_from_request import get_db_filters_from_request


class GetProductCategoriesView(View):
    def get(
        self, request: HttpRequest, products_repository: ProductRepositoryInterface = get_product_repository()
    ) -> JsonResponse:
        categories = products_repository.get_categories(request.GET.get("product_ids"))
        return JsonResponse({"categories": ProductCategorySerializer(categories, many=True).data})


class GetProductsView(View):
    interactor = get_products_interactor()

    def get(self, request: HttpRequest) -> JsonResponse:
        filters = get_db_filters_from_request(ProductFiltersInterface, request)
        products = self.interactor(filters)

        return JsonResponse({"products": [asdict(p) for p in products]})


class GetOrganizationsView(View):
    interactor = get_organizations_interactor()

    def get(self, request: HttpRequest) -> JsonResponse:
        filters = get_db_filters_from_request(OrganizationFilterInterface, request)
        organizations = self.interactor(filters)

        return JsonResponse({"organizations": [asdict(o) for o in organizations]})
