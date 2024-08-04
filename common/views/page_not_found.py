from django.shortcuts import render
from django.views.generic import TemplateView

from domens.domain_service.domain_service import DomainService
from settings.get_settings import get_settings


class BaseNotFoundPage(TemplateView):
    template_name = "common/404.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["settings"] = get_settings(self.request)
        context["domain"] = DomainService.get_domain_string()
        context["partner_domain"] = DomainService.get_partners_domain_string()

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)
