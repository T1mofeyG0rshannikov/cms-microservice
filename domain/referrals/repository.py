from collections.abc import Iterable
from typing import Protocol

from domain.referrals.referral import ReferralInterface


class ReferralRepositoryInterface(Protocol):
    def get(self, id: int | None = None, sponsors_id: int | None = None) -> ReferralInterface | None:
        raise NotImplementedError

    def filter(
        self, user_id: int, total_referal_level: int, level: int | None = None, sorted_by: str | None = None
    ) -> Iterable[ReferralInterface]:
        raise NotImplementedError
