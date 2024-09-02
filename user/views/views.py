from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from user.models.product import UserProduct
from user.serializers import UserSerializer


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
class DeleteUserProduct(View):
    def delete(self, request):
        delete = QueryDict(request.body)
        product = delete.get("product")
        print(delete)
        print(product)

        product = UserProduct.objects.get(id=product)
        product.deleted = True
        product.save()

        return HttpResponse(status=204)
