from catalog.catalog_service.catalog_service import get_catalog_service
from catalog.catalog_service.catalog_service_interface import CatalogServiceInterface
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
