from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.add_session_action import IncrementSessionCount
from infrastructure.persistence.sessions.service import get_raw_session_service
from infrastructure.requests.service import get_request_service
from web.settings.views import SettingsMixin


class OpenedProductPopupView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    url_parser: UrlParserInterface = get_url_parser()
    increment_session_profile_action = IncrementSessionCount(get_user_session_repository(), "profile_actions_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1

        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        self.increment_session_profile_action(
            request.user_session_id, adress, text=f'''Открыл описание "{product_name}"'''
        )

        return HttpResponse(status=201)


class OpenedProductLinkView(View):
    product_repository: ProductRepositoryInterface = get_product_repository()
    url_parser: UrlParserInterface = get_url_parser()
    increment_banks_count = IncrementSessionCount(get_user_session_repository(), "banks_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        self.increment_banks_count(request.user_session_id, adress, f'''Перешел по ссылке "{product_name}"''')

        return HttpResponse(status=201)


class OpenedProductPromoView(View):
    url_parser: UrlParserInterface = get_url_parser()
    product_repository: ProductRepositoryInterface = get_product_repository()
    increment_banks_count = IncrementSessionCount(get_user_session_repository(), "banks_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        product = int(request.GET.get("product_id")) - 1

        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_offers()[product]

        self.increment_banks_count(request.user_session_id, adress, f'''Перешел по баннеру "{product_name}"''')

        return HttpResponse(status=201)


class OpenedChangePasswordFormView(View):
    url_parser: UrlParserInterface = get_url_parser()
    increment_session_profile_action = IncrementSessionCount(get_user_session_repository(), "profile_actions_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        self.increment_session_profile_action(request.user_session_id, adress, text="""Открыл изменение пароля""")

        return HttpResponse(status=201)


class OpenedUpdateProductFormView(View):
    url_parser: UrlParserInterface = get_url_parser()
    product_repository: ProductRepositoryInterface = get_product_repository()
    increment_session_profile_action = IncrementSessionCount(get_user_session_repository(), "profile_actions_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_by_id(int(request.GET.get("product"))).name

        self.increment_session_profile_action(
            request.user_session_id, adress, text=f'''Открыл настройку продукта "{product_name}"'''
        )

        return HttpResponse(status=201)


class IncrementBanksCountView(View):
    increment_banks_count = IncrementSessionCount(get_user_session_repository(), "banks_count")

    def get(self, request: HttpRequest) -> HttpResponse:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        self.increment_banks_count(request.user_session_id, adress, f"""Открыл описание продукта""")

        return HttpResponse(status=200)


class CapchaView(SettingsMixin):
    template_name = "common/capcha.html"


class SubmitCapcha(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        session = request.raw_session
        if session:
            session_id = session.id

            raw_session_service = get_raw_session_service(get_request_service(request))
            raw_session_service.success_capcha(session_id)

        return HttpResponse(status=200)
