import json

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .models import Page, Template
from .serializers import PageSerializer, TemplateSerializer


class ShowPage(View):
    def get(self, request, page_url):
        try:
            page = Page.objects.prefetch_related("blocks").get(url=page_url)
            serialized_page = PageSerializer(page).data
            return render(request, "cms/page.html", {"page": serialized_page})
        except Page.DoesNotExist:
            raise Http404("Page does not exist")


class ShowTemplates(View):
    def get(self, request):
        # print()
        return HttpResponse(json.dumps(TemplateSerializer(Template.objects.all(), many=True).data))
