from collections.abc import Iterable
from typing import Protocol

from domain.referrals.referral import ReferralInterface
from domain.user.user import UserInterface


class ReferralServiceInterface(Protocol):
    def get_referral_level(self, referral: UserInterface, user: UserInterface):
        raise NotImplementedError

    def get_referral(self, user_id: int, user: UserInterface) -> ReferralInterface:
        raise NotImplementedError

    def get_referrals(self, user_id: int, level=None, sorted_by=None) -> Iterable[ReferralInterface]:
        raise NotImplementedError
