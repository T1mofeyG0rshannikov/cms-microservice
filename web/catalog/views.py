from django.http import HttpRequest, JsonResponse

from domain.products.repository import ProductRepositoryInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.models.catalog.products import (
    Organization,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)
from web.catalog.serializers import ProductsSerializer
from web.common.pagination import Pagination
from web.user.serializers import UserProductsSerializer
from web.user.views.base_user_view import APIUserRequired


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
