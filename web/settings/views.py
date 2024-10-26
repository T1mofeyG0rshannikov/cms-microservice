from django.views.generic import TemplateView

from application.services.domains.service import get_domain_service
from domain.domains.service import DomainServiceInterface
from infrastructure.persistence.models.materials import Document
from web.settings.get_settings import get_settings


class SettingsMixin(TemplateView):
    domain_service: DomainServiceInterface = get_domain_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        domain = self.domain_service.get_domain_string()

        if hasattr(self.request, "domain"):
            if self.request.domain == "localhost":
                domain = "localhost:8000"

        context["domain"] = domain
        context["settings"] = get_settings(
            domain=self.request.domain if hasattr(self.request, "domain") else None,
            subdomain=self.request.subdomain if hasattr(self.request, "subdomain") else None,
        )
        context["site_name"] = self.domain_service.get_site_name()
        context["partner_domain"] = self.domain_service.get_partners_domain_string()

        context["privacy"] = Document.objects.get(slug="privacypolicy")
        context["terms"] = Document.objects.get(slug="termsofservice")

        return context
