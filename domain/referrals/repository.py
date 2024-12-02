from typing import Iterable, Protocol

from domain.referrals.referral import ReferralInterface


class ReferralRepositoryInterface(Protocol):
    def get_referral_by_id(self, id: int) -> ReferralInterface | None:
        raise NotImplementedError

    def get_referrals_by_level(self, sponsor_id: int, level: int) -> Iterable[ReferralInterface]:
        raise NotImplementedError
    
    def get_referrals(self, user_id: int, total_referal_level: int, level: int = None, sorted_by: str = None) -> Iterable[ReferralInterface]:
        raise NotImplementedError
