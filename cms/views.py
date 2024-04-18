from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from .models import Page
from .serializers import PageSerializer


class ShowPage(View):
    def get(self, request, page_url):
        try:
            page = Page.objects.prefetch_related("components").get(url=page_url)
            serialized_page = PageSerializer(page).data
            return render(request, "cms/page.html", {"page": serialized_page})
        except Page.DoesNotExist:
            raise Http404("Page does not exist")
