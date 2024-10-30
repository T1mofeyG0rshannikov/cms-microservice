from django.http import HttpRequest, JsonResponse

from application.usecases.public.catalog_page import GetCatalogPage, get_catalog_page
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import (
    ExclusiveCard,
    Organization,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.blocks.serializers import PageSerializer
from web.catalog.serializers import CatalogProductSerializer, ProductsSerializer
from web.common.pagination import Pagination
from web.domens.views.mixins import SubdomainMixin
from web.user.serializers import UserProductsSerializer
from web.user.views.base_user_view import APIUserRequired, UserFormsView


class ShowCatalogPage(SubdomainMixin):
    template_name = "blocks/page.html"
    product_repository: ProductRepositoryInterface = get_product_repository()
    get_catalog_page_interactor: GetCatalogPage = get_catalog_page()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= UserFormsView.get_context_data()

        page = self.get_catalog_page_interactor(slug=kwargs["products_slug"])

        context["page"] = PageSerializer(page).data

        user_is_authenticated = self.request.user.is_authenticated

        if user_is_authenticated:
            products = self.product_repository.get_catalog_offers(self.kwargs["products_slug"])
        else:
            products = self.product_repository.get_unprivate_catalog_offers(self.kwargs["products_slug"])

        product_type = ProductType.objects.get(slug=self.kwargs["products_slug"])

        context["products"] = CatalogProductSerializer(products, context={"type": product_type}, many=True).data
        context["exclusive_card"] = ExclusiveCard.objects.first()

        return context


class GetProducts(APIUserRequired):
    def get(
        self, request: HttpRequest, products_repository: ProductRepositoryInterface = get_product_repository()
    ) -> JsonResponse:
        organization = request.GET.get("organization")

        try:
            products = ProductsSerializer(
                products_repository.filter_enabled_products(organization_id=organization, user_id=request.user.id),
                many=True,
            ).data
        except Organization.DoesNotExist:
            return JsonResponse({"error": f"no organization with id '{organization}'"})

        return JsonResponse({"products": products})


class GetUserProducts(APIUserRequired):
    def get(
        self, request: HttpRequest, product_repository: ProductRepositoryInterface = get_product_repository()
    ) -> JsonResponse:
        product_category = request.GET.get("category")

        products = product_repository.filter_user_products(category_id=product_category, user_id=request.user.id)

        pagination = Pagination(request)
        products = pagination.paginate(products, "products", UserProductsSerializer)

        return JsonResponse(products)
