from django.http import JsonResponse

from application.services.site_service import get_site_service
from application.usecases.formatters.format_document import (
    FormatDocument,
    get_format_document,
)
from application.usecases.public.get_settings import (
    GetSettings,
    get_get_settings_interactor,
)
from domain.user.sites.site_service import SiteServiceInterface
from infrastructure.requests.request_interface import RequestInterface
from web.settings.views.settings_mixin import SettingsMixin
from web.template.views.views import BaseTemplateLoadView


class GetPopup(BaseTemplateLoadView, SettingsMixin):
    site_service: SiteServiceInterface = get_site_service()

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
            domain=request.domain,
            subdomain=request.subdomain,
        )

        site = self.site_service.get_site_from_url(request.build_absolute_uri())

        context = {"document": document, "settings": settings, "site": site}

        return JsonResponse(
            {
                "content": self.template_loader.load_template(
                    app_name="materials", template_name=template_name, context=context
                )
            }
        )
