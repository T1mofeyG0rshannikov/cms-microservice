from django.http import JsonResponse

from application.usecases.formatters.format_document import (
    FormatDocument,
    get_format_document,
)
from application.usecases.public.get_settings import (
    GetSettings,
    get_get_settings_interactor,
)
from infrastructure.requests.request_interface import RequestInterface
from web.settings.views.mixins import SubdomainMixin
from web.template.views.views import BaseTemplateLoadView


class GetPopup(BaseTemplateLoadView, SubdomainMixin):
    def get(
        self,
        request: RequestInterface,
        *args,
        get_settings_interactor: GetSettings = get_get_settings_interactor(),
        document_formatter: FormatDocument = get_format_document(),
        **kwargs
    ) -> JsonResponse:
        document_slug = request.GET.get("document")

        document = document_formatter(document_slug)

        if document_slug == "aboutcompany":
            template_name = "document-popup-with-header"
        else:
            template_name = "document-popup"

        settings = get_settings_interactor(
            domain=request.domain if hasattr(request, "domain") else None,
            subdomain=request.subdomain if hasattr(request, "subdomain") else None,
        )

        site = self.domain_service.get_site_from_url(request.build_absolute_uri())

        context = {"document": document, "settings": settings, "site": site}

        return JsonResponse(
            {
                "content": self.template_loader.load_template(
                    app_name="materials", template_name=template_name, context=context
                )
            }
        )
