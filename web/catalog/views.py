from django.http import HttpRequest, JsonResponse

from domain.page_blocks.entities.page import PageInterface
from domain.products.repository import ProductRepositoryInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import (
    ExclusiveCard,
    Organization,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)
from web.blocks.views import BasePageView
from web.catalog.serializers import CatalogProductSerializer, ProductsSerializer
from web.common.pagination import Pagination
from web.user.serializers import UserProductsSerializer
from web.user.views.base_user_view import APIUserRequired


class ShowCatalogPageView(BasePageView):
    product_repository: ProductRepositoryInterface = get_product_repository()

    def get_context_data(self, page: PageInterface, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        user_is_authenticated = self.request.user.is_authenticated

        products_slug = self.request.path[1::]

        if user_is_authenticated:
            products = self.product_repository.get_catalog_offers(products_slug)
        else:
            products = self.product_repository.get_catalog_offers(products_slug, private=False)

        product_type = ProductType.objects.get(slug=products_slug)

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
                products_repository.get_enabled_products_to_create(
                    organization_id=organization, user_id=request.user.id
                ),
                many=True,
            ).data
        except Organization.DoesNotExist:
            return JsonResponse({"error": f"no organization with id '{organization}'"})

        return JsonResponse({"products": products})


class GetUserProducts(APIUserRequired):
    def get(
        self,
        request: HttpRequest,
        user_product_repository: UserProductRepositoryInterface = get_user_product_repository(),
    ) -> JsonResponse:
        product_category = request.GET.get("category")

        pagination = Pagination(request)
        products = pagination.paginate(
            user_product_repository.filter(category_id=product_category, user_id=request.user.id),
            "products",
            UserProductsSerializer,
        )

        return JsonResponse(products)
