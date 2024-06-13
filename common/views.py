from django.http import HttpResponseNotFound
from django.views.generic import TemplateView

from domens.models import Site
from settings.get_settings import get_settings


class BaseTemplateView(TemplateView):
    def __init__(self):
        super().__init__()
        # self.settings = get_settings(self.get_subdomen())

    def get_subdomen(self):
        host = self.request.get_host()
        host = host.replace("127.0.0.1", "localhost")

        if "." not in host:
            return ""

        return host.split(".")[0]

    def valid_subdomen(self, subdomen: str) -> bool:
        if not subdomen:
            return True

        if Site.objects.filter(domen=subdomen).exists() and Site.objects.get(domen=subdomen).is_active:
            return True

        if subdomen == "www":
            return True

        return False

    def get(self, *args, **kwargs):
        subdomen = self.get_subdomen()
        print(subdomen, "subdomen")

        self.settings = get_settings(subdomen)

        if not self.valid_subdomen(subdomen):
            return HttpResponseNotFound("404 Subdomen not found")

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = self.settings

        return context
