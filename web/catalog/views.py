from django.http import HttpRequest, JsonResponse
from django.views import View

from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.catalog.products import (
    Organization,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.catalog.serializers import ProductsSerializer


class GetProducts(View):
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
