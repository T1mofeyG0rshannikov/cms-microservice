from collections.abc import Iterable
from typing import Protocol

from domain.referrals.referral import ReferralInterface


class ReferralRepositoryInterface(Protocol):
    def get(self, id: int) -> ReferralInterface | None:
        raise NotImplementedError

    def get_referrals(
        self, user_id: int, total_referal_level: int, level: int = None, sorted_by: str = None
    ) -> Iterable[ReferralInterface]:
        raise NotImplementedError
