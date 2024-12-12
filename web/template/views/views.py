from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from application.sessions.add_session_action import (
    IncrementSessionCount,
    get_increment_session_count,
)
from application.texts.user_session import UserActions
from domain.products.repository import ProductRepositoryInterface
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.models.blocks.catalog_block import CatalogBlock
from infrastructure.persistence.models.blocks.common import Page
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.views.templates import Profile
from web.blocks.views import ShowPage
from web.catalog.views import ShowCatalogPage
from web.settings.views.mixins import SubdomainMixin
from web.template.profile_template_loader.profile_template_loader import (
    get_profile_template_loader,
)
from web.template.profile_template_loader.profile_template_loader_interface import (
    ProfileTemplateLoaderInterface,
)
from web.template.template_loader.template_loader import get_template_loader
from web.template.template_loader.template_loader_interface import (
    TemplateLoaderInterface,
)


def slug_router(request: HttpRequest, slug: str):
    if Page.objects.filter(url=slug).exists():
        return ShowPage.as_view()(request, page_url=slug)

    if CatalogBlock.objects.filter(product_type__slug=slug).exists():
        return ShowCatalogPage.as_view()(request, products_slug=slug)

    if slug == "my":
        return Profile.as_view()(request)

    return PageNotFound.as_view()(request)


class BaseTemplateLoadView(View):
    template_loader: TemplateLoaderInterface = get_template_loader()

    def get(self, request: HttpRequest) -> JsonResponse:
        template = self.get_content(request)
        return JsonResponse({"content": template})


class GetChangeUserFormTemplate(BaseTemplateLoadView):
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get_content(self, request: HttpRequest):
        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=UserActions.opened_profile_data)

        return self.template_loader.load_change_user_form(request)


class GetChangeSiteFormTemplate(BaseTemplateLoadView):
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get_content(self, request: HttpRequest):
        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=UserActions.opened_site_settings)

        return self.template_loader.load_change_site_form(request)


class GetChangeSocialsFormTemplate(BaseTemplateLoadView):
    def get_content(self, request):
        return self.template_loader.load_change_socials_form(request)


class PageNotFound(SubdomainMixin):
    template_name = "common/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


class BaseProfileTemplateView(View):
    template_loader: ProfileTemplateLoaderInterface = get_profile_template_loader()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest):
        try:
            template = self.get_template(request)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        self.create_user_session_log(
            request=request,
            text="Перешёл на страницу",
        )

        return JsonResponse(template)

    def get_template(self, request: HttpRequest):
        raise NotImplementedError


class ProfileTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_profile_template(request)


class RefsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_refs_template(request)


class IdeasTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_ideas_template(request)


class ManualsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_manuals_template(request)


class SiteTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_site_template(request)


class UserProductsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> str:
        return self.template_loader.load_products_template(request)


class GetChoiceProductForm(BaseTemplateLoadView):
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get_content(self, request: RequestInterface):
        self.create_user_session_log(request=request, text=UserActions.opened_products_list)

        return self.template_loader.load_choice_product_form(request)


class GetCreateUserProductForm(BaseTemplateLoadView):
    def get_content(self, request: HttpRequest):
        return self.template_loader.load_create_user_product_form(request)


class GetProductDescriptionPopup(BaseTemplateLoadView):
    product_repository: ProductRepositoryInterface = get_product_repository()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get_content(self, request: HttpRequest):
        product = int(request.GET.get("product"))

        product_name = self.product_repository.get(id=product)

        self.create_user_session_log(request=request, text=f'''Открыл описание продукта "{product_name}"''')

        return self.template_loader.load_product_description_popup(request)


class GetDeleteProductPopup(BaseTemplateLoadView):
    def get_content(self, request: HttpRequest):
        return self.template_loader.load_delete_product_popup(request)


class GetReferralPopupTemplate(BaseTemplateLoadView):
    def get_content(self, request: HttpRequest):
        return self.template_loader.load_referral_popup(request)


class GetCreateIdeaForm(BaseTemplateLoadView):
    def get_content(self, request: HttpRequest):
        return self.template_loader.load_create_idea_form(request)
