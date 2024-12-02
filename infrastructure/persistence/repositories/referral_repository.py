from typing import Iterable
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField, Value

from domain.referrals.referral import ReferralInterface
from domain.referrals.repository import ReferralRepositoryInterface
from infrastructure.persistence.models.user.user import User


class ReferralRepository(ReferralRepositoryInterface):
    def get_referral_by_id(self, id: int) -> ReferralInterface | None:
        return User.objects.get_user_by_id(id)

    def get_referrals_by_level(self, sponsor_id: int, total_levels_count: int, level: int) -> Iterable[ReferralInterface]:
        filters = Q(**{"sponsor__" * (level - 1) + "sponsor_id": sponsor_id })
        
        referral_counts = dict()
        for ref_level in range(total_levels_count):
            referral_counts[f"count_level_{ref_level + 1}"] = Count("sponsors__" * ref_level + "sponsors", distinct=True)

        return User.objects.annotate(**referral_counts, level=Value(level, output_field=IntegerField()), referrals=ExpressionWrapper(sum([F(field) for field in referral_counts.keys()]), output_field=IntegerField())).filter(filters)
        
    def get_referrals(self, sponsor_id: int, total_levels_count: int, level: int = None, sorted_by: str = None) -> Iterable[ReferralInterface]:
        if level:
            referrals = self.get_referrals_by_level(sponsor_id, total_levels_count, level)

        else:
            referrals = User.objects.none()
            
            for ref_level in range(total_levels_count):
                referrals |= self.get_referrals_by_level(sponsor_id, total_levels_count, ref_level+1)

        return referrals.order_by(sorted_by)

def get_referral_repository() -> ReferralRepositoryInterface:
    return ReferralRepository()
