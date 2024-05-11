import json

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .clone_page import clone_page
from .models.common import Page, Template
from .serializers import PageSerializer, TemplateSerializer
from settings.get_settings import get_settings


class ShowPage(View):
    def get(self, request, page_url):
        try:
            page = Page.objects.prefetch_related("blocks").get(url=page_url)
            serialized_page = PageSerializer(page).data
            
            settings = get_settings()

            return render(request, "blocks/page.html", {"page": serialized_page, "settings": settings})
        except Page.DoesNotExist:
            raise Http404("Page does not exist")


class ShowTemplates(View):
    def get(self, request):
        return JsonResponse(TemplateSerializer(Template.objects.all(), many=True).data)


@method_decorator(csrf_exempt, name="dispatch")
class ClonePage(View):
    def post(self, request):
        data = json.loads(request.body)
        page_id = data.get("page_id")

        clone_page(page_id)

        return HttpResponse(status=201)
