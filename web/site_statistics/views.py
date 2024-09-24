from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
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
