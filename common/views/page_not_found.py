from django.shortcuts import render
from django.views.generic import TemplateView

from domens.get_domain import get_domain_string, get_partners_domain_string
from settings.get_settings import get_settings


class BaseNotFoundPage(TemplateView):
    template_name = "common/404.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        settings = get_settings(self.request)

        if self.request.domain == "localhost":
            domain = "localhost:8000"
        else:
            domain = get_domain_string()

        partner_domain = get_partners_domain_string()

        context["settings"] = settings
        context["domain"] = domain
        context["partner_domain"] = partner_domain

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)
