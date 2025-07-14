from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from application.sessions.add_session_action import (
    IncrementSessionCount,
    get_increment_session_count,
)
from application.texts.user_session import UserActions
from application.usecases.public.catalog_page import GetCatalogPage, get_catalog_page
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.views.templates import Profile
from web.blocks.views import BasePageView
from web.settings.views.settings_mixin import SettingsMixin
from web.template.profile_template_loader.profile_template_loader import (
    get_profile_template_loader,
)
from web.template.profile_template_loader.profile_template_loader_interface import (
    ProfileTemplateLoaderInterface,
    ProfileTemplateLoaderResponse,
)
from web.template.template_loader.template_loader import get_template_loader
from web.template.template_loader.template_loader_interface import (
    TemplateLoaderInterface,
)


def slug_router(
    request: HttpRequest,
    slug: str,
    page_repository: PageRepositoryInterface = get_page_repository(),
    get_catalog_page: GetCatalogPage = get_catalog_page(),
) -> HttpResponse:
    page = page_repository.get(url=slug)
    if page:
        return BasePageView.as_view()(request, page=page)

    user_is_authenticated = request.user.is_authenticated
    page = get_catalog_page(slug=slug, user_is_authenticated=user_is_authenticated)
    if page:
        return BasePageView.as_view()(request, page=page)

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


class PageNotFound(SettingsMixin):
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
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_profile_template(request)


class RefsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_refs_template(request)


class IdeasTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_ideas_template(request)


class MessangerTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_messanger_template(request)


class ManualsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_manuals_template(request)


class SiteTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
        return self.template_loader.load_site_template(request)


class UserProductsTemplate(BaseProfileTemplateView):
    def get_template(self, request: HttpRequest) -> ProfileTemplateLoaderResponse:
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


class GetChatBody(BaseTemplateLoadView):
    def get_content(self, request: RequestInterface):
        return self.template_loader.load_chat_body(request)
