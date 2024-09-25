from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.products.repository import ProductRepositoryInterface
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from web.site_statistics.models import UserAction, UserActivity


class OpenedProductPopupView(View):
    repository = get_product_repository()

    def get(self, request: HttpRequest):
        product = int(request.GET.get("product_id")) - 1

        adress = request.META.get("HTTP_REFERER")
        adress = adress.replace("https://", "")
        adress = adress.replace("http://", "")

        product_name = self.repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        UserAction.objects.create(
            adress=adress,
            text=f'''Открыл описание "{product_name}"''',
            session=UserActivity.objects.get(unique_key=request.session["user_activity"]["unique_key"]),
        )

        return HttpResponse(status=201)


class OpenedProductLinkView(View):
    repository = get_product_repository()

    def get(self, request: HttpRequest):
        product = int(request.GET.get("product_id")) - 1

        adress = request.META.get("HTTP_REFERER")
        adress = adress.replace("https://", "")
        adress = adress.replace("http://", "")

        product_name = self.repository.get_product_name_from_catalog(
            product_type_slug=adress.split("/")[1], product_index=product
        )

        UserAction.objects.create(
            adress=adress,
            text=f'''Перешел по ссылке "{product_name}"''',
            session=UserActivity.objects.get(unique_key=request.session["user_activity"]["unique_key"]),
        )

        return HttpResponse(status=201)


class OpenedProductPromoView(View):
    repository = get_product_repository()

    def get(self, request: HttpRequest):
        product = int(request.GET.get("product_id")) - 1

        adress = request.META.get("HTTP_REFERER")
        adress = adress.replace("https://", "")
        adress = adress.replace("http://", "")

        product_name = self.repository.get_offers()[product]

        UserAction.objects.create(
            adress=adress,
            text=f'''Перешел по баннеру "{product_name}"''',
            session=UserActivity.objects.get(unique_key=request.session["user_activity"]["unique_key"]),
        )

        return HttpResponse(status=201)


class OpenedChangePasswordFormView(View):
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()

    def get(self, request: HttpRequest):
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f"""Открыл изменение пароля""",
            session_unique_key=request.session["user_activity"]["unique_key"],
        )

        return HttpResponse(status=201)


class OpenedUpdateProductFormView(View):
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    product_repository: ProductRepositoryInterface = get_product_repository()

    def get(self, request: HttpRequest):
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_name = self.product_repository.get_product_by_id(int(request.GET.get("product"))).name

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f'''Открыл настройку продукта "{product_name}"''',
            session_unique_key=request.session["user_activity"]["unique_key"],
        )

        return HttpResponse(status=201)
