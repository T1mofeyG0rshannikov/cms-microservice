from collections.abc import Iterable

from django.db.models import (
    Case,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    Q,
    Value,
    When,
)

from domain.referrals.referral import ReferralInterface
from domain.referrals.repository import ReferralRepositoryInterface
from infrastructure.persistence.models.user.user import User


class ReferralRepository(ReferralRepositoryInterface):
    def get(self, id: int | None = None, sponsors_id: int | None = None) -> ReferralInterface | None:
        query = Q()
        if id:
            query &= Q(id=id)
        elif sponsors_id:
            query &= Q(sponsors__id=sponsors_id)

        try:
            return User.objects.get(query)
        except User.DoesNotExist:
            return None

    def filter(
        self, sponsor_id: int, total_levels_count: int, level: int | None = None, sorted_by: str | None = None
    ) -> Iterable[ReferralInterface]:
        levels = (level - 1, level) if level else (0, total_levels_count)

        referral_counts = dict()
        for ref_level in range(total_levels_count):
            referral_counts[f"count_level_{ref_level + 1}"] = Count(
                "sponsors__" * ref_level + "sponsors", distinct=True
            )

        level_queries = [(ref_level + 1, "sponsor__" * ref_level + "sponsor_id") for ref_level in range(*levels)]
        level_filter_query = Q()

        for query in level_queries:
            level_filter_query |= Q(**{query[1]: sponsor_id})

        return (
            User.objects.filter(level_filter_query)
            .annotate(
                **referral_counts,
                level=Case(
                    *(When(**{query: sponsor_id}, then=Value(ind)) for ind, query in level_queries),
                    output_field=IntegerField(),
                ),
                referrals=ExpressionWrapper(
                    sum([F(field) for field in referral_counts.keys()]), output_field=IntegerField()
                ),
            )
            .order_by(sorted_by)
        )


def get_referral_repository() -> ReferralRepositoryInterface:
    return ReferralRepository()
