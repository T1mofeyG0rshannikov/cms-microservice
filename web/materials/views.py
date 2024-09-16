from web.template.views.views import BaseTemplateLoadView


class GetPopup(BaseTemplateLoadView):
    def get_content(self, request):
        return self.template_loader.load_document_popup(request)
