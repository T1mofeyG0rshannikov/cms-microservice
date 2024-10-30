from django.http import HttpRequest

from web.domens.views.mixins import SubdomainMixin
from web.template.views.views import BaseTemplateLoadView


class GetPopup(BaseTemplateLoadView, SubdomainMixin):
    def get_content(self, request: HttpRequest):
        return self.template_loader.load_document_popup(request)
