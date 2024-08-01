from typing import Any

from django.template import loader

from account.models import Messanger, UserFont
from blocks.template_exist import is_template_exists
from common.models import SocialNetwork
from settings.models import SiteSettings


class TemplateLoader:
    @staticmethod
    def load_template(app_name: str, template_name: str, request=None, context: dict[Any, Any] = None):
        if is_template_exists(f"{app_name}/{template_name}.html"):
            return loader.render_to_string(f"{app_name}/{template_name}.html", context, request, None)
        return None

    def load_change_user_form(self, request):
        context = {"request": request, "user": request.user}

        context["messangers"] = Messanger.objects.select_related("social_network").all()

        return self.load_template(app_name="common", template_name="change-user-form", request=request, context=context)

    def load_change_site_form(self, request):
        context = {"request": request}

        context["fonts"] = UserFont.objects.all()
        context["socials"] = SocialNetwork.objects.all()

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]

        return self.load_template(app_name="account", template_name="site-form", request=request, context=context)


def get_template_loader() -> TemplateLoader:
    return TemplateLoader()
