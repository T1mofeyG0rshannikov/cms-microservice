from account.models import Messanger, UserFont
from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralsSerializer
from common.models import SocialNetwork
from common.pagination import Pagination
from domens.models import Domain
from settings.models import SiteSettings

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(TemplateContextProcessorInterface):
    def __init__(self, referral_service: ReferralServiceInterface):
        self.referral_service = referral_service

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

        context["user"] = self.referral_service.get_referral(user_id, request.user)

        return context

    def get_profile_template_context(self, request):
        context = self.get_context(request)

        return context

    def get_site_template_context(self, request):
        context = self.get_context(request)

        return context

    def get_refs_template_context(self, request):
        context = self.get_context(request)

        level = request.GET.get("level")
        sorted_by = request.GET.get("sorted_by")

        referrals = self.referral_service.get_referrals(level=level, user=request.user, sorted_by=sorted_by)

        pagination = Pagination(request)

        referrals = pagination.paginate(referrals, "referrals", ReferralsSerializer)

        context = {**context, **referrals}

        return context


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor(get_referral_service())
