from django.http import JsonResponse

from application.services.products_service import get_products_service
from application.usecases.public.catalog_page import GetCatalogPage
from domain.products.service import ProductsServiceInterface
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import (
    ExclusiveCard,
    Organization,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.blocks.serializers import PageSerializer
from web.catalog.serializers import CatalogProductSerializer
from web.common.pagination import Pagination
from web.domens.views.mixins import SubdomainMixin
from web.user.serializers import UserProductsSerializer
from web.user.views.base_user_view import APIUserRequired, UserFormsView


class ShowCatalogPage(SubdomainMixin):
    template_name = "blocks/page.html"
    product_repository = get_product_repository()
    get_catalog_page = GetCatalogPage()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= UserFormsView.get_context_data()

        page = self.get_catalog_page(slug=kwargs["products_slug"])

        context["page"] = PageSerializer(page).data

        exclusive_card = ExclusiveCard.objects.first()

        user_is_authenticated = self.request.user.is_authenticated

        if user_is_authenticated:
            products = self.product_repository.get_catalog_offers(self.kwargs["products_slug"])
        else:
            products = self.product_repository.get_unprivate_catalog_offers(self.kwargs["products_slug"])

        product_type = ProductType.objects.get(slug=self.kwargs["products_slug"])

        products = CatalogProductSerializer(products, context={"type": product_type}, many=True).data
        context["products"] = products
        context["exclusive_card"] = exclusive_card

        return context


class GetProducts(APIUserRequired):
    products_service: ProductsServiceInterface = get_products_service(get_product_repository())

    def get(self, request):
        organization = request.GET.get("organization")

        try:
            products = self.products_service.filter_enabled_products(
                organization_id=organization, user_id=request.user.id
            )
        except Organization.DoesNotExist:
            return JsonResponse({"error": f"no organization with id '{organization}'"})

        return JsonResponse({"products": products})


class GetUserProducts(APIUserRequired):
    products_service: ProductsServiceInterface = get_products_service(get_product_repository())

    def get(self, request):
        product_category = request.GET.get("category")

        products = self.products_service.filter_user_products(category_id=product_category, user_id=request.user.id)

        pagination = Pagination(request)
        products = pagination.paginate(products, "products", UserProductsSerializer)

        return JsonResponse(products)
