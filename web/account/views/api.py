from django.http import HttpRequest, JsonResponse

from application.services.user.referrals_service import get_referral_service
from domain.referrals.service import ReferralServiceInterface
from domain.user.exceptions import InvalidReferalLevel, InvalidSortedByField
from web.account.serializers import ReferralsSerializer
from web.common.pagination import Pagination
from web.user.views.base_user_view import APIUserRequired


class GetReferals(APIUserRequired):
    referral_service: ReferralServiceInterface = get_referral_service()

    def get(self, request: HttpRequest) -> JsonResponse:
        level = self.request.GET.get("level")
        sorted_by = self.request.GET.get("sorted_by", "created_at")

        try:
            referrals = self.referral_service.get_referrals(
                level=level, user_id=self.request.user.id, sorted_by=sorted_by
            )
        except (InvalidSortedByField, InvalidReferalLevel) as e:
            return JsonResponse({"error": str(e)}, status=400)

        pagination = Pagination(request)

        return JsonResponse(pagination.paginate(referrals, "referrals", ReferralsSerializer))
