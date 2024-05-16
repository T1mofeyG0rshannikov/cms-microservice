from django.views.generic import TemplateView

from settings.get_settings import get_settings


class BaseTemplateView(TemplateView):
    def __init__(self):
        self.settings = get_settings()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = self.settings

        return context
