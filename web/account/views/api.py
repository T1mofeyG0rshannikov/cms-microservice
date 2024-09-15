import json

from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralSerializer, ReferralsSerializer
from common.pagination import Pagination
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from user.exceptions import InvalidReferalLevel, InvalidSortedByField
from user.models.user import User

from application.texts.errors import UserErrors


class GetReferals(View):
    referral_service: ReferralServiceInterface = get_referral_service()

    def get(self, request):
        level = self.request.GET.get("level")
        sorted_by = self.request.GET.get("sorted_by")

        try:
            referrals = self.referral_service.get_referrals(level=level, user=self.request.user, sorted_by=sorted_by)
        except (InvalidSortedByField, InvalidReferalLevel) as e:
            return JsonResponse({"error": str(e)}, status=400)

        pagination = Pagination(request)

        referrals = pagination.paginate(referrals, "referrals", ReferralsSerializer)

        return JsonResponse(referrals)


class GetReferral(View):
    def get(self, request, user_id):
        try:
            referral = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": UserErrors.user_does_not_exist.value}, status=400)

        referral = ReferralSerializer(referral).data

        return HttpResponse(json.dumps(referral))
