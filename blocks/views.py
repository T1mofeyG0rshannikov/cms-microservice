import json

from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from blocks.clone_page import clone_page
from blocks.models.blocks import CatalogBlock
from blocks.models.common import Page, Template
from blocks.serializers import PageSerializer, TemplateSerializer
from catalog.models import CatalogPageTemplate
from common.views import BaseTemplateView
from user.forms import LoginForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = CatalogPageTemplate.objects.prefetch_related("blocks").first()
        serialized_page = PageSerializer(page).data

        catalog = CatalogBlock.objects.get(product_type__slug=kwargs["products_slug"])

        context["page"] = serialized_page
        context["catalog"] = catalog

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
    def post(self, request):
        data = json.loads(request.body)
        page_id = data.get("page_id")

        clone_page(page_id)

        return HttpResponse(status=201)
