import json

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from blocks.models.catalog_block import CatalogBlock
from blocks.models.common import Page, Template
from blocks.pages_service.page_service_interface import PageServiceInterface
from blocks.pages_service.pages_service import get_page_service
from blocks.serializers import PageSerializer, TemplateSerializer
from catalog.catalog_service.catalog_service import get_catalog_service
from catalog.catalog_service.catalog_service_interface import CatalogServiceInterface
from common.views import BaseTemplateView
from user.forms import LoginForm
from django.shortcuts import render
from user.forms import LoginForm
from domens.models import Domain


class IndexPage(BaseTemplateView):
    template_name = "blocks/page.html"

    def get(self, *args, **kwargs):
        partner_domain = Domain.objects.filter(is_partners=True).first()
        
        if (self.get_domain() == partner_domain.domain or "localhost") and self.get_subdomain() == "":
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


class ShowPage(BaseTemplateView):
    template_name = "blocks/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = Page.objects.prefetch_related("blocks").get(url=kwargs["page_url"])
        serialized_page = PageSerializer(page).data

        context["page"] = serialized_page
        context["form"] = LoginForm()

        return context


class ShowCatalogPage(BaseTemplateView):
    template_name = "blocks/page.html"

    def __init__(self):
        super().__init__()
        self.catalog_service: CatalogServiceInterface = get_catalog_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.catalog_service.get_page(kwargs["products_slug"])

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
