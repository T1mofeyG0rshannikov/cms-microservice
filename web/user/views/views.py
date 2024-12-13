import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.texts.errors import ErrorsMessages
from application.usecases.user.send_submit_phone_code import (
    SendConfirmPhoneCode,
    get_send_confirm_phone_interactor,
)
from application.usecases.user.submit_phone import (
    ConfirmUserPhone,
    get_confirm_phone_interactor,
)
from application.usecases.user_products.delete_user_product import (
    DeleteUserProduct,
    get_delete_user_product_interactor,
)
from domain.user.exceptions import InvalidConfirmPhoneCode
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.requests.request_interface import RequestInterface
from web.user.views.base_user_view import APIUserRequired


class IsUserAuth(View):
    def get(self, request: RequestInterface) -> HttpResponse:
        status = 200 if (request.user.is_authenticated or request.user_from_header) else 401
        return HttpResponse(status=status)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteUserProductView(View):
    delete_user_product_intercator: DeleteUserProduct = get_delete_user_product_interactor()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def delete(self, request: RequestInterface) -> HttpResponse:
        product = request.GET.get("product")

        product_name = self.delete_user_product_intercator(product).product_name

        self.create_user_session_log(
            request=request,
            text=f'''Удалил продукт "{product_name}"''',
        )

        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name="dispatch")
class SendConfirmPhoneView(APIUserRequired):
    send_confirm_phone_interactor: SendConfirmPhoneCode = get_send_confirm_phone_interactor()

    def post(self, request: RequestInterface) -> HttpResponse:
        user = request.user
        self.send_confirm_phone_interactor(user_id=user.id, phone=user.phone)
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name="dispatch")
class SubmitPhoneView(APIUserRequired):
    submit_phone_interactor: ConfirmUserPhone = get_confirm_phone_interactor()

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        code = json.loads(request.body)

        code = code["code"]

        try:
            self.submit_phone_interactor(user_id=user.id, code=code)
        except InvalidConfirmPhoneCode as e:
            return JsonResponse({"errors": {"phone": [str(e)]}}, status=400)
        except:
            return JsonResponse({"errors": {"phone": [ErrorsMessages.something_went_wrong]}}, status=400)

        return HttpResponse(status=200)
