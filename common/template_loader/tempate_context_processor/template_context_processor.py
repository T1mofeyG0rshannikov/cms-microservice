from account.models import Messanger, UserFont
from common.models import SocialNetwork
from settings.models import SiteSettings

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(TemplateContextProcessorInterface):
    @staticmethod
    def get_context(request):
        context = {"request": request, "user": request.user}
        return context

    def get_change_user_form_context(self, request):
        context = self.get_context(request)

        context["messangers"] = Messanger.objects.select_related("social_network").all()

        return context

    def get_change_site_form_context(self, request):
        context = self.get_context(request)

        context["fonts"] = UserFont.objects.all()
        context["socials"] = SocialNetwork.objects.all()

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]

        return context


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor()
