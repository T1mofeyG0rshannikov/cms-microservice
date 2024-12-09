from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from application.sessions.add_session_action import (
    IncrementSessionCount,
    get_increment_session_count,
)
from application.sessions.raw_session_service import get_raw_session_service
from application.texts.user_session import UserActions
from domain.products.repository import ProductRepositoryInterface
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from infrastructure.requests.service import get_request_service
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser
from web.settings.views import SettingsMixin


class OpenedProductPopupView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    url_parser: UrlParserInterface = get_url_parser()
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=f'''Открыл описание "{product_name}"''')

        return HttpResponse(status=201)


class OpenedProductLinkView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    url_parser: UrlParserInterface = get_url_parser()
    increment_banks_count: IncrementSessionCount = get_increment_session_count("banks_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        self.increment_banks_count(request=request)
        self.create_user_session_log(request=request, text=f'''Перешел по ссылке "{product_name}"''')

        return HttpResponse(status=201)


class OpenedProductPromoView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    increment_banks_count: IncrementSessionCount = get_increment_session_count("banks_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1

        product_name = self.product_repository.get_offers()[product]

        self.increment_banks_count(request=request)
        self.create_user_session_log(request=request, text=f'''Перешел по баннеру "{product_name}"''')

        return HttpResponse(status=201)


class OpenedChangePasswordFormView(View):
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=UserActions.opened_password_change)

        return HttpResponse(status=201)


class OpenedUpdateProductFormView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        product_name = self.product_repository.get_product_by_id(int(request.GET.get("product"))).name

        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=f'''Открыл настройку продукта "{product_name}"''')

        return HttpResponse(status=201)


class IncrementBanksCountView(View):
    url_parser: UrlParserInterface = get_url_parser()
    increment_banks_count: IncrementSessionCount = get_increment_session_count("banks_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def get(self, request: HttpRequest) -> HttpResponse:
        self.increment_banks_count(request=request)
        self.create_user_session_log(request=request, text=UserActions.opened_product_description)

        return HttpResponse(status=200)


class CapchaView(SettingsMixin):
    template_name = "common/capcha.html"


class SubmitCapcha(View):
    def post(self, request: RequestInterface) -> HttpResponse:
        if request.raw_session_id:
            session_id = request.raw_session_id

            raw_session_service = get_raw_session_service(get_request_service(request))
            raw_session_service.success_capcha(session_id)

        return HttpResponse(status=200)
