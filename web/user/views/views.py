from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.usecases.user_products.delete_user_product import DeleteUserProduct
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.user.serializers import UserSerializer


class GetUserInfo(View):
    def get(self, request):
        user_from_request = request.user
        user_from_header = request.user_from_header

        user = None
        if user_from_header:
            user = user_from_header
        if user_from_request.is_authenticated:
            user = user_from_request

        if user:
            user = UserSerializer(user).data
            return JsonResponse(user)
        else:
            return HttpResponse(status=401)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteUserProductView(View):
    delete_user_product_intercator = DeleteUserProduct(get_product_repository())

    def delete(self, request):
        product = request.GET.get("product")
        self.delete_user_product_intercator(product)
        return HttpResponse(status=204)
