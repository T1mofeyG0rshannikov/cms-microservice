from dataclasses import asdict
import json
from django.http import HttpRequest, JsonResponse

from application.services.user.referrals_service import get_referral_service
from application.mappers.site import from_orm_to_site
from domain.referrals.service import ReferralServiceInterface
from web.account.serializers import ReferralsSerializer
from web.common.pagination import Pagination
from web.user.views.base_user_view import APIUserRequiredGenerics


class GetReferals(APIUserRequiredGenerics):
    referral_service: ReferralServiceInterface = get_referral_service()

    def get(self, request: HttpRequest) -> JsonResponse:
        level = self.request.GET.get("level")
        sorted_by = self.request.GET.get("sorted_by", "created_at")

        referrals = self.referral_service.get_referrals(level=level, user_id=self.request.user.id, sorted_by=sorted_by)

        pagination = Pagination(request)

        return JsonResponse(pagination.paginate(referrals, "referrals", ReferralsSerializer))


class GetUserSiteView(APIUserRequiredGenerics):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({
            "site": asdict(from_orm_to_site(request.user.site))
        })
