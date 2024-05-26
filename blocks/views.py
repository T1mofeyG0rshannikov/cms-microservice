import json

from django.http import Http404, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from blocks.clone_page import clone_page
from blocks.models.common import Page, Template
from blocks.serializers import PageSerializer, TemplateSerializer
from common.views import BaseTemplateView
from user.forms import LoginForm


class ShowPage(BaseTemplateView):
    template_name = "blocks/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            page = Page.objects.prefetch_related("blocks").get(url=kwargs["page_url"])
            serialized_page = PageSerializer(page).data

            context["page"] = serialized_page
        except Page.DoesNotExist:
            raise Http404("Page does not exist")

        context["form"] = LoginForm()

        return context


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
