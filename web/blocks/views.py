import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.usecases.public.clone_block import get_clone_block
from application.usecases.public.clone_page import get_clone_page
from application.usecases.public.get_page.get_page import GetPage, get_page
from infrastructure.persistence.repositories.page_repository import get_page_repository
from web.blocks.serializers import PageSerializer


class PageView(View):
    interactor: GetPage = get_page()

    def get(self, request: HttpRequest):
        page_repository = get_page_repository()
        page_url = request.GET.get("url")
        if page_url == "":
            page_url = None

        user_is_authenticated = request.user.is_authenticated
        print(page_url)

        page = self.interactor(url=page_url, user_is_authenticated=user_is_authenticated)

        return JsonResponse({"page": PageSerializer(page).data})


@method_decorator(csrf_exempt, name="dispatch")
class ClonePageView(View):
    clone_page_interactor = get_clone_page()

    def post(self, request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body)
        page_id = data.get("page_id")

        self.clone_page_interactor(page_id)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CloneBlock(View):
    clone_block_interactor = get_clone_block()

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        block_id = data.get("block_id")
        block_class = data.get("block_class")

        self.clone_block_interactor(block_id=block_id, block_class_name=block_class)

        return HttpResponse(status=201)
