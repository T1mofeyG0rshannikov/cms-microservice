from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.usecases.user_products.delete_user_product import (
    DeleteUserProduct,
    get_delete_user_product_interactor,
)
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.requests.request_interface import RequestInterface


class IsUserAuth(View):
    def get(self, request: RequestInterface) -> HttpResponse:
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
    delete_user_product_intercator: DeleteUserProduct = get_delete_user_product_interactor()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def delete(self, request: RequestInterface) -> HttpResponse:
        product = request.GET.get("product")

        product_name = self.delete_user_product_intercator(product)

        self.create_user_session_log(
            request=request,
            text=f'''Удалил продукт "{product_name}"''',
        )

        return HttpResponse(status=204)
