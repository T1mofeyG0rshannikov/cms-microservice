from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from account.views import Profile
from blocks.models.catalog_block import CatalogBlock
from blocks.models.common import Page
from blocks.views import ShowPage
from catalog.views import ShowCatalogPage
from common.security import LinkEncryptor
from common.template_loader.template_loader import get_template_loader
from domens.views.mixins import SubdomainMixin


class RedirectToLink(View):
    link_encryptor = LinkEncryptor()

    def get(self, request):
        tracker = self.request.GET.get("product")
        if tracker:
            link = self.link_encryptor.decrypt(tracker)

            if link:
                return HttpResponseRedirect(link)

        return HttpResponse(status=400)


class GetChangeUserFormTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        template = self.template_loader.load_change_user_form(request)
        return JsonResponse({"content": template})


class GetChangeSiteFormTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        template = self.template_loader.load_change_site_form(request)
        return JsonResponse({"content": template})


class PageNotFound(SubdomainMixin):
    template_name = "common/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


def slug_router(request, slug):
    if Page.objects.filter(url=slug).exists():
        return ShowPage.as_view()(request, page_url=slug)

    if CatalogBlock.objects.filter(product_type__slug=slug).exists():
        return ShowCatalogPage.as_view()(request, products_slug=slug)

    if slug == "my":
        return Profile.as_view()(request)

    return PageNotFound.as_view()(request)
