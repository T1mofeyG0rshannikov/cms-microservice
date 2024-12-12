from django.shortcuts import render

from web.settings.views.settings_mixin import SettingsMixin


class BaseNotFoundPage(SettingsMixin):
    template_name = "common/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)
