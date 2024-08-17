from account.models import Messanger, UserFont
from account.referrals_service.referrals_service import get_referral_service
from account.serializers import ReferralSerializer
from common.models import SocialNetwork
from domens.models import Domain
from settings.models import SiteSettings
from user.models import User

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

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]
        context["domains"] = Domain.objects.values("domain", "id").filter(is_partners=True)

        return context

    def get_change_socials_form_context(self, request):
        context = self.get_context(request)
        context["socials"] = SocialNetwork.objects.all()

        return context

    def get_referral_popup_context(self, request):
        context = self.get_context(request)

        user_id = request.GET.get("user_id")
        referral_service = get_referral_service()

        try:
            referral = User.objects.get(id=user_id)
            referral.level = referral_service.get_referral_level(referral, request.user)
        except User.DoesNotExist:
            pass

        referral = ReferralSerializer(referral).data
        print(referral)

        context["user"] = referral

        return context


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor()
