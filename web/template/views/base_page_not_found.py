from django.shortcuts import render
from settings.views import SettingsMixin


class BaseNotFoundPage(SettingsMixin):
    template_name = "common/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)
