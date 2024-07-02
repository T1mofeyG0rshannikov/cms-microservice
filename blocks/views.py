import json

from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from blocks.models.catalog_block import CatalogBlock
from blocks.models.common import Page, Template
from blocks.pages_service.page_service_interface import PageServiceInterface
from blocks.pages_service.pages_service import get_page_service
from blocks.serializers import PageSerializer, TemplateSerializer
from catalog.catalog_service.catalog_service import get_catalog_service
from catalog.catalog_service.catalog_service_interface import CatalogServiceInterface
from domens.models import Domain
from settings.models import SiteSettings
from user.forms import LoginForm


class IndexPage(TemplateView):
    template_name = "blocks/page.html"

    def get(self, *args, **kwargs):
        partner_domain = Domain.objects.filter(is_partners=True).first()

        if self.request.domain == partner_domain.domain and SiteSettings.objects.first().disable_partners_sites:
            return HttpResponse("<h1>Привет :)</h1>")

        if (
            self.request.domain == partner_domain.domain  # or self.request.domain == "localhost"
        ) and self.request.subdomain == "":
            form = LoginForm()

            return render(self.request, "blocks/login.html", {"form": form})

        if not Page.objects.filter(url=None).exists():
            return HttpResponseNotFound()

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = Page.objects.prefetch_related("blocks").get(url=None)

        serialized_page = PageSerializer(page).data

        context["page"] = serialized_page
        context["form"] = LoginForm()

        return context


class ShowPage(TemplateView):
    template_name = "blocks/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = Page.objects.prefetch_related("blocks").get(url=kwargs["page_url"])
        serialized_page = PageSerializer(page).data

        context["page"] = serialized_page
        context["form"] = LoginForm()

        return context


class ShowCatalogPage(TemplateView):
    template_name = "blocks/page.html"

    def __init__(self):
        super().__init__()
        self.catalog_service: CatalogServiceInterface = get_catalog_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.catalog_service.get_page(user=self.request.user, slug=kwargs["products_slug"])

        context["page"] = page
        context["form"] = LoginForm()

        return context


class ShowTemplates(View):
    def get(self, request):
        return JsonResponse(TemplateSerializer(Template.objects.all(), many=True).data)


def slug_router(request, slug):
    if Page.objects.filter(url=slug).exists():
        return ShowPage.as_view()(request, page_url=slug)

    if CatalogBlock.objects.filter(product_type__slug=slug).exists():
        return ShowCatalogPage.as_view()(request, products_slug=slug)

    return HttpResponseNotFound("404 Page not found")


@method_decorator(csrf_exempt, name="dispatch")
class ClonePage(View):
    def __init__(self):
        self.page_service: PageServiceInterface = get_page_service()

    def post(self, request):
        data = json.loads(request.body)
        page_id = data.get("page_id")

        self.page_service.clone_page(page_id)

        return HttpResponse(status=201)
