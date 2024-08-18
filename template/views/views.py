from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from account.views.templates import Profile
from blocks.models.catalog_block import CatalogBlock
from blocks.models.common import Page
from blocks.views import ShowPage
from catalog.views import ShowCatalogPage
from domens.domain_service.domain_service import DomainService
from domens.views.mixins import SubdomainMixin
from template.template_loader.template_loader import get_template_loader
from user.exceptions import InvalidReferalLevel, InvalidSortedByField


def slug_router(request, slug):
    if Page.objects.filter(url=slug).exists():
        return ShowPage.as_view()(request, page_url=slug)

    if CatalogBlock.objects.filter(product_type__slug=slug).exists():
        return ShowCatalogPage.as_view()(request, products_slug=slug)

    if slug == "my":
        return Profile.as_view()(request)

    return PageNotFound.as_view()(request)


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


class GetChangeSocialsFormTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        template = self.template_loader.load_change_socials_form(request)
        return JsonResponse({"content": template})


class PageNotFound(SubdomainMixin):
    template_name = "common/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


class ProfileTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        content = self.template_loader.load_profile_template(request)

        return JsonResponse({"content": content, "title": f"Обзор | {DomainService.get_site_name()}"})


class RefsTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        try:
            content = self.template_loader.load_refs_template(request)
        except InvalidSortedByField as e:
            return JsonResponse({"error": str(e)}, status=400)
        except InvalidReferalLevel as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"content": content, "title": f"Мои рефералы | {DomainService.get_site_name()}"})


class SiteTemplate(View):
    template_loader = get_template_loader()

    def get(self, request):
        content = self.template_loader.load_site_template(request)

        return JsonResponse({"content": content, "title": f"Мой сайт | {DomainService.get_site_name()}"})
