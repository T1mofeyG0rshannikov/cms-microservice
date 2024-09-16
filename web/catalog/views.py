from django.http import JsonResponse
from django.views import View

from web.catalog.catalog_service.catalog_service import get_catalog_service
from web.catalog.catalog_service.catalog_service_interface import (
    CatalogServiceInterface,
)
from web.catalog.models.products import Organization
from web.catalog.products_service.products_service import get_products_service
from web.catalog.products_service.products_service_interface import (
    ProductsServiceInterface,
)
from web.common.pagination import Pagination
from web.domens.views.mixins import SubdomainMixin
from web.user.serializers import UserProductsSerializer
from web.user.views.base_user_view import UserFormsView


class ShowCatalogPage(SubdomainMixin):
    template_name = "blocks/page.html"
    catalog_service: CatalogServiceInterface = get_catalog_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= UserFormsView.get_context_data()
        page = self.catalog_service.get_page(user=self.request.user, slug=kwargs["products_slug"])

        context["page"] = page

        return context


class GetProducts(View):
    products_service: ProductsServiceInterface = get_products_service()

    def get(self, request):
        organization = request.GET.get("organization")

        try:
            products = self.products_service.filter_enabled_products(organization_id=organization, user=request.user)
        except Organization.DoesNotExist:
            return JsonResponse({"error": f"no organization with id '{organization}'"})

        return JsonResponse({"products": products})


class GetUserProducts(View):
    products_service: ProductsServiceInterface = get_products_service()

    def get(self, request):
        product_category = request.GET.get("category")

        products = self.products_service.filter_user_products(category_id=product_category, user=request.user)

        pagination = Pagination(request)
        products = pagination.paginate(products, "products", UserProductsSerializer)

        return JsonResponse(products)
