from datetime import datetime

from django.views.generic import TemplateView

from application.services.domains.service import get_domain_service
from application.usecases.public.get_settings import (
    GetSettings,
    get_get_settings_interactor,
)
from domain.domains.service import DomainServiceInterface
from domain.materials.repository import DocumentRepositoryInterface
from infrastructure.persistence.repositories.document_repository import get_document_repository


class SettingsMixin(TemplateView):
    domain_service: DomainServiceInterface = get_domain_service()
    get_settings_interactor: GetSettings = get_get_settings_interactor()
    document_repository: DocumentRepositoryInterface = get_document_repository()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        domain = self.domain_service.get_domain_string()

        if hasattr(self.request, "domain"):
            if self.request.domain == "localhost":
                domain = "localhost:8000"

        context["domain"] = domain

        context["settings"] = self.get_settings_interactor(
            domain=self.request.domain if hasattr(self.request, "domain") else None,
            subdomain=self.request.subdomain if hasattr(self.request, "subdomain") else None,
        )
        context["site_name"] = self.domain_service.get_site_name()
        context["partner_domain"] = self.domain_service.get_partners_domain_string()

        context["privacy"] = self.document_repository.get_document(slug="privacypolicy").first()
        context["terms"] = self.document_repository.get_document(slug="termsofservice").first()
        context["year"] = str(datetime.now().year)

        return context
