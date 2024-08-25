from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from catalog.catalog_service.catalog_service import get_catalog_service
from catalog.catalog_service.catalog_service_interface import CatalogServiceInterface
from catalog.models.products import Organization, Product
from catalog.serializers import ProductsSerializer
from domens.views.mixins import SubdomainMixin
from user.views.base_user_view import UserFormsView


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
    def get(self, request):
        organization = request.GET.get("organization")

        filters = Q()

        if organization:
            try:
                organization = Organization.objects.get(id=organization)

                filters |= Q(organization=organization)
            except Organization.DoesNotExist:
                return JsonResponse({"error": f"no organization with id '{organization}'"})

        user_products = request.user.products.values_list("product__id", flat=True).all()
        products = (
            Product.objects.select_related("category", "organization").filter(filters).exclude(id__in=user_products)
        )

        products = ProductsSerializer(products, many=True).data
        return JsonResponse({"products": products})
