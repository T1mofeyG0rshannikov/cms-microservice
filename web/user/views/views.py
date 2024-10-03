from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.usecases.user_products.delete_user_product import DeleteUserProduct
from domain.products.repository import ProductRepositoryInterface
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)


class IsUserAuth(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        user_from_header = request.user_from_header

        auth = None
        if user.is_authenticated:
            auth = True
        if user_from_header:
            auth = True

        status = 200 if auth else 401
        return HttpResponse(status=status)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteUserProductView(View):
    delete_user_product_intercator = DeleteUserProduct(get_product_repository())
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    product_repository: ProductRepositoryInterface = get_product_repository()

    def delete(self, request: HttpRequest) -> HttpResponse:
        product = request.GET.get("product")
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        self.delete_user_product_intercator(product)

        product_name = self.product_repository.get_product_by_id(product).name

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f'''Удалил продукт "{product_name}"''',
            session_unique_key=request.session["user_activity"]["unique_key"],
        )

        return HttpResponse(status=204)
